from collections import deque


class DisplayQueue:
  def __init__(self):
    self.queue = deque()

  def clear(self):
    self.queue.clear()

  def add(self, item: str):
    self.queue.appendleft(item)

  def get_display_hex(self) -> str:
    hex_ = self.queue.pop()
    self.add(hex_)
    return hex_

  def move_to_end(self, hex_code: str):
    self.queue.remove(hex_code)
    self.add(hex_code)

  def process_new_data(self, data: list[str]):
    # Find the hex codes that are not in the queue
    to_be_added = [hex_ for hex_ in data if hex_ not in self.queue]
    # Find the hex codes that are in the queue but not in the data
    to_be_removed = [hex_ for hex_ in self.queue if hex_ not in data]
    self._add_new_hex_list(to_be_added)
    self._remove_hex_list(to_be_removed)

  def _add_new_hex_list(self, hex_list: list[str]):
    for hex_ in hex_list:
      self.add(hex_)

  def _remove_hex_list(self, hex_list: list[str]):
    for hex_ in hex_list:
      self.queue.remove(hex_)
