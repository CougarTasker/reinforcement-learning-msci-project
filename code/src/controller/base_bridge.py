from multiprocessing import Manager
from typing import Any


class BaseBridge(object):
    """Bases class that represents a bridge between two processes."""

    capacity = 1000

    def __init__(self) -> None:
        """Initialise a bridge."""
        manager = Manager()
        self.queue = manager.Queue(self.capacity)
        self.count_lock = manager.Lock()
        self.count = manager.Value(int, 0)

    def get_count(self) -> int:
        """Get the current count of items in the queue.

        Returns:
            int: the number of items on the queue
        """
        return self.count.get()

    def has_capacity(self) -> bool:
        """Check the queue has capacity to add more items.

        Returns:
            bool: true if it is safe to add more to the queue.
        """
        return self.get_count() < self.capacity

    def add_item(self, queue_item: Any):
        """Add item to the queue, not blocking.

        Args:
            queue_item (Any): The item to be added.
        """
        with self.count_lock:
            self.count.set(self.count.get() + 1)
            self.queue.put_nowait(queue_item)

    def get_item_blocking(self) -> Any:
        """Get the next item in the queue while blocking.

        Returns:
            Any: the next item.
        """
        queue_item = self.queue.get()
        with self.count_lock:
            self.count.set(self.count.get() - 1)
        return queue_item

    def get_latest_item(self) -> Any:
        """Get the latest item on the queue.

        Returns:
            Any: the latest item. None if the queue is empty
        """
        if self.get_count() == 0:
            return None
        last_queue_item = None
        # hold onto the lock so not competing with other end to add states
        with self.count_lock:
            count = self.count.get()
            while count > 0:
                last_queue_item = self.queue.get_nowait()
                count -= 1
            self.count.set(count)
        return last_queue_item
