"""
LeetCode #146 - LRU Cache
https://leetcode.com/problems/lru-cache/

Design a data structure that follows the Least Recently Used (LRU) cache eviction policy.

Constraints:
- get(key) and put(key, value) must both run in O(1) average time
- 1 <= capacity <= 3000
- 0 <= key, value <= 10^4
- At most 2 * 10^5 calls will be made to get and put

Approach:
    Combine a doubly linked list with a hashmap.
    - The hashmap gives O(1) access to any node by key.
    - The doubly linked list maintains usage order; most recent at the tail,
      least recent at the head.
    - Two sentinel nodes (head and tail) eliminate edge cases for
      insertion and removal at the boundaries.
"""


class Node:
    """A node in the doubly linked list storing a key-value pair."""

    def __init__(self, key: int = 0, value: int = 0):
        self.key = key
        self.value = value
        self.prev: "Node | None" = None
        self.next: "Node | None" = None


class LRUCache:
    """
    LRU Cache with O(1) get and put operations.

    Uses a doubly linked list to track usage order and a hashmap
    for constant-time node lookup.

    Args:
        capacity: Maximum number of key-value pairs the cache can hold.

    Example:
        >>> cache = LRUCache(2)
        >>> cache.put(1, 1)
        >>> cache.put(2, 2)
        >>> cache.get(1)   # returns 1
        1
        >>> cache.put(3, 3)  # evicts key 2 (least recently used)
        >>> cache.get(2)   # returns -1 (not found)
        -1
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: dict[int, Node] = {}

        self.head = Node()  # least recently used side
        self.tail = Node()  # most recently used side
        self.head.next = self.tail
        self.tail.prev = self.head

    # ------------------------------------------------------------------
    # interface
    # ------------------------------------------------------------------

    def get(self, key: int) -> int:
        """
        Return the value for key if it exists, otherwise -1.
        Moves the accessed node to the most-recently-used position.
        """
        if key not in self.cache:
            return -1

        node = self.cache[key]
        self._move_to_tail(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        """
        Insert or update the value for key.
        If the cache is at capacity, evict the least recently used entry first.
        """
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._move_to_tail(node)
        else:
            if len(self.cache) == self.capacity:
                self._evict_lru()
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._insert_before_tail(new_node)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _remove(self, node: Node) -> None:
        """Unlink a node from the list. O(1)."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert_before_tail(self, node: Node) -> None:
        """Insert a node just before the tail sentinel (MRU position). O(1)."""
        node.prev = self.tail.prev
        node.next = self.tail
        self.tail.prev.next = node
        self.tail.prev = node

    def _move_to_tail(self, node: Node) -> None:
        """Move an existing node to the MRU position. O(1)."""
        self._remove(node)
        self._insert_before_tail(node)

    def _evict_lru(self) -> None:
        """Remove the least recently used node (just after head sentinel). O(1)."""
        lru_node = self.head.next
        self._remove(lru_node)
        del self.cache[lru_node.key]


# ------------------------------------------------------------------
# Quick test (remove before submitting to LeetCode)
# ------------------------------------------------------------------
if __name__ == "__main__":
    cache = LRUCache(2)

    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1        # returns 1; 1 is now MRU

    cache.put(3, 3)                 # evicts key 2
    assert cache.get(2) == -1       # key 2 was evicted

    cache.put(4, 4)                 # evicts key 1
    assert cache.get(1) == -1       # key 1 was evicted
    assert cache.get(3) == 3        # returns 3
    assert cache.get(4) == 4        # returns 4

    print("All assertions passed.")
