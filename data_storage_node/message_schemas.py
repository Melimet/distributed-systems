from enum import Enum
from typing import Optional
from itertools import groupby


class MessageType(Enum):
    ERROR = -1
    ACK = 0
    ELECTION = 1
    FILE = 2
    SYNC = 3
    HEARTBEAT = 4


class Message:
    """
    Base class for all messages. Format for data string is as follows:

    ```
    <MESSAGE_TYPE>
    <ARBITRARY_DATA>
    ```

    where
        MESSAGE_TYPE   = integer representing the type of message (eg. 0 for election)
        ARBITRARY_DATA = a multi-line string representing the arbitrary data of the message
    """

    data: str

    def __init__(self, data: str = ""):
        self.data = data

    def get_type(self) -> MessageType:
        return MessageType(int(self.get_line(0)))

    def is_ok(self) -> bool:
        return self.get_type() != MessageType.ERROR

    def get_lines(self) -> list:
        return self.data.strip().split("\n")

    def get_line(self, index: int) -> Optional[str]:
        lines = self.get_lines()
        if index >= len(lines):
            return None
        return lines[index]


class ErrorMessage(Message):
    """
    Message used for error handling. Message format for error message is as follows:

    ```
    -1
    <ERROR_MESSAGE>
    ```

    where
        ERROR_MESSAGE = error message
    """

    def from_error_message(error_message: str) -> "ErrorMessage":
        data = f"""
        {MessageType.ERROR.value}
        {error_message}
        """
        return ErrorMessage(data)

    def get_error_message(self) -> str:
        return self.get_line(1)


class AckMessage(Message):
    """
    Message used for acknowledging messages. Message format for ack message is as follows:

    ```
    0
    <ACK_MESSAGE>
    ```

    where
        ACK_MESSAGE = ack message (might be empty)
    """

    def from_ack_message(message: Optional[str] = "") -> "AckMessage":
        data = f"{MessageType.ACK.value}\n{message}"
        return AckMessage(data)


class ElectionMessage(Message):
    """
    Message used for leader election. Message format for election message is as follows:

    ```
    1
    <ID>
    ```

    where
        ID = suggested leader node id or -1 for HALT
    """

    def from_id(id: int) -> "ElectionMessage":
        data = f"{MessageType.ELECTION.value}\n{id}"
        return ElectionMessage(data)

    def get_id(self) -> int:
        return int(self.get_line(1))


class FileOperation(Enum):
    SELECT = 0
    UPSERT = 1
    DELETE = 2


class FileMessage(Message):
    """
    Message used for file operations. Message format for file message is as follows:

    ```
    2
    <OPERATION>
    <FILE_NAME>
    <FILE_CONTENT>
    ```

    where
        OPERATION       = SELECT | UPSERT | DELETE
        FILE_NAME       = name of the file to be operated on
        FILE_CONTENT    = content of the file to be operated on (might be empty)
    """

    def from_operation(
        file_operation: FileOperation,
        file_name: str,
        file_content: str,
    ) -> "FileMessage":
        data = f"""
        {MessageType.FILE.value}
        {file_operation.value}
        {file_name}
        {file_content}
        """
        return FileMessage(data)

    def get_operation(self) -> FileOperation:
        return FileOperation(int(self.get_line(1)))

    def get_file_name(self) -> str:
        return self.get_line(2).strip()

    def get_file_content(self) -> str:
        return self.get_line(3).strip()


class SyncMessage(Message):
    """
    Message used for synchronization of files. Nodes store a sequence number
    that acts as a logical clock. The sequence number is incremented every time
    a file is mutated. Message format for sync message is as follows:

    ```
    3
    <SEQUENCE_NUMBER>
    <FILE_MESSAGES>
    ```

    where
        SEQUENCE_NUMBER = sequence number acts as a logical clock (Lamport timestamp)
        FILE_MESSAGES   = a multi-line string representing the file messages
                          empty line is used as a separator between messages
    """

    def from_sequence_number(
        sequence_number: int, file_messages: list[FileMessage]
    ) -> "SyncMessage":
        messages = [file_message.data for file_message in file_messages]
        messages = "\n\n".join(messages)

        data = f"""
        {MessageType.SYNC.value}
        {sequence_number}
        {messages}
        """
        return SyncMessage(data)

    def get_sequence_number(self) -> int:
        return int(self.get_line(1))

    def get_file_messages(self) -> list[FileMessage]:
        file_messages = self.get_lines()[2:]
        file_messages = [
            "\n".join(group)
            for key, group in groupby(file_messages, lambda x: x != "")
            if key
        ]
        return [FileMessage(file_message) for file_message in file_messages]


class HeartbeatMessage(Message):
    """
    Message used for heartbeat.

    ```
    4
    ```
    """

    def create() -> "HeartbeatMessage":
        data = f"{MessageType.HEARTBEAT.value}"
        return HeartbeatMessage(data)
