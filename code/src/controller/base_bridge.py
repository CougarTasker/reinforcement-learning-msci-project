from enum import Enum
from multiprocessing import Manager
from typing import Any

from zmq import NOBLOCK, PAIR, Again, Context


class BridgeState(Enum):
    """Enumerates the possible connection states of the bridge."""

    none = 0
    port_bound = 1
    connected = 2


class BaseBridge(object):
    """Bases class that represents a bridge between two processes."""

    def __init__(self) -> None:
        """Initialise a bridge."""
        manager = Manager()
        self.state_lock = manager.Lock()
        self.port = manager.Value(int, 0)
        self.state = manager.Value(BridgeState, BridgeState.none)
        self.socket = None

    def add_item(self, queue_item: Any):
        """Add item to the queue, not blocking.

        Args:
            queue_item (Any): The item to be added.
        """
        self.__get_socket().send_pyobj(queue_item)

    def get_item_blocking(self) -> Any:
        """Get the next item in the queue while blocking.

        Returns:
            Any: the next item.
        """
        return self.__get_socket().recv_pyobj()

    def get_item_non_blocking(self) -> Any:
        """Get the latest item on the queue.

        Returns:
            Any: the latest item. None if the queue is empty
        """
        try:
            return self.__get_socket().recv_pyobj(NOBLOCK)
        except Again:
            return None

    def __get_socket(self):
        if self.socket is not None:
            return self.socket

        with self.state_lock:
            match self.state.get():
                case BridgeState.none:
                    self.socket = Context().socket(PAIR)
                    port = self.socket.bind_to_random_port("tcp://*")
                    self.port.set(port)
                    self.state.set(BridgeState.port_bound)
                case BridgeState.port_bound:
                    self.socket = Context().socket(PAIR)
                    self.socket.connect(f"tcp://localhost:{self.port.get()}")
                    self.state.set(BridgeState.connected)
                case BridgeState.connected:
                    raise RuntimeError("connected while missing bridge end")

        return self.socket
