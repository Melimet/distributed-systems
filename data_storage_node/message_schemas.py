from enum import Enum
from typing import Optional


class MessageType(Enum):
    INVALID = -1
    ELECTION = 0


class Message:
    """
    Base class for all messages. Format for data string is as follows:

    ```
    MESSAGE_TYPE
    ARBITRARY_DATA
    ```

    where MESSAGE_TYPE is an integer representing the type of message (eg. 0 for election),
    and ARBITRARY_DATA is a multi-line string representing the arbitrary data of the message.
    """

    data: str

    def __init__(self, data: str = ""):
        self.data = data

    def get_type(self) -> MessageType:
        try:
            splitted = self.data.split("\n")
            print("splitted: ", splitted)
            return MessageType(int(splitted[0]))
        except:
            return MessageType.INVALID


class ElectionMessage(Message):
    """
    Message used for leader election. Message format for election message is as follows:

    ```
    0
    ID
    ```

    where ID is the suggested leader node id or -1 for HALT.
    """

    def from_id(self, id: int) -> "ElectionMessage":
        self.data = f"{MessageType.ELECTION.value}\n{id}"
        return ElectionMessage(f"{MessageType.ELECTION.value}\n{id}")

    def get_id(self) -> int:
        return int(self.data.split("\n")[1])
