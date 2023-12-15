from messaging_client import MessagingClient
from leader_election import LeaderElection
from message_schemas import (
    Message,
    AckMessage,
    ErrorMessage,
    FileMessage,
    FileOperation,
    SyncMessage,
)

# How many messages leader stores for synchronization purposes
WRITE_BUFFER_LIMIT = 10


class FileStorage:
    sequence_number: int
    files: dict
    write_buffer: list[FileMessage]
    messaging_client: MessagingClient

    def __init__(self):
        self.sequence_number = 0
        self.files = {}
        self.write_buffer = []
        self.messaging_client = MessagingClient()

    async def process_file_message(
        self, message: FileMessage, leader_election: LeaderElection
    ) -> Message:
        operation = message.get_operation()
        is_mutating_operation = operation != FileOperation.SELECT
        is_leader = leader_election.is_leader()

        if not leader_election.leader_elected:
            return ErrorMessage.from_error_message("Leader not elected yet")

        if not is_leader and is_mutating_operation:
            return ErrorMessage.from_error_message(
                "Mutating operations only allowed on leader"
            )

        if is_mutating_operation:
            self.update_write_buffer(message)
            self.sequence_number += 1

        sync_done = await self.synchronize_self(leader_election)
        if not sync_done:
            return ErrorMessage.from_error_message("Synchronization failed")

        return self.handle_file_operation(message)

    def handle_file_operation(self, message: FileMessage) -> Message:
        operation = message.get_operation()

        if operation == FileOperation.SELECT:
            return FileMessage.from_operation(
                FileOperation.SELECT,
                message.get_file_name(),
                self.files.get(message.get_file_name(), ""),
            )
        elif operation == FileOperation.UPSERT:
            self.files[message.get_file_name()] = message.get_file_content()
            return AckMessage.from_ack_message()
        elif operation == FileOperation.DELETE:
            self.files.pop(message.get_file_name(), None)
            return AckMessage.from_ack_message()

    def update_write_buffer(self, message: FileMessage):
        self.write_buffer.append(message)
        if len(self.write_buffer) > WRITE_BUFFER_LIMIT:
            self.write_buffer.pop(0)

    def full_sync_needed(self, sequence_number: int, target_sequence_number):
        return (
            target_sequence_number - sequence_number > WRITE_BUFFER_LIMIT
            or sequence_number > target_sequence_number
        )

    async def synchronize_self(self, leader_election: LeaderElection) -> bool:
        if leader_election.is_leader():
            return True

        leader = leader_election.get_leader()
        message = SyncMessage.from_sequence_number(self.sequence_number, [])
        response = await self.messaging_client.send(
            leader.ip, leader.port, message.data
        )

        if not response.is_ok():
            return False

        sync_response = SyncMessage(response.data)

        if self.full_sync_needed(
            self.sequence_number, sync_response.get_sequence_number()
        ):
            self.files = {}
            self.sequence_number = 0

        for file_message in sync_response.get_file_messages():
            self.handle_file_operation(file_message)

        self.sequence_number = sync_response.get_sequence_number()

        return True

    def synchronize_follower(
        self, message: SyncMessage, leader_election: LeaderElection
    ) -> Message:
        if not leader_election.is_leader():
            return ErrorMessage.from_error_message("Only leader can synchronize")

        follower_up_to_date = message.get_sequence_number() == self.sequence_number
        full_sync_needed = self.full_sync_needed(
            message.get_sequence_number(), self.sequence_number
        )

        if follower_up_to_date:
            return SyncMessage.from_sequence_number(self.sequence_number, [])

        elif full_sync_needed:
            file_messages = [
                FileMessage.from_operation(
                    FileOperation.UPSERT,
                    key,
                    self.files[key],
                )
                for key in self.files
            ]
            return SyncMessage.from_sequence_number(self.sequence_number, file_messages)

        else:
            return SyncMessage.from_sequence_number(
                self.sequence_number, self.write_buffer
            )
