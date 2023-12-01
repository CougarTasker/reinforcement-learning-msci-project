from multiprocessing import Queue
from typing import Any


class BaseBridge(object):
    """Bases class that represents a bridge between two processes."""

    def __init__(self) -> None:
        """Initialise a bridge."""
        self.queue: Queue[Any] = Queue()
