import logging
import threading


class Worker:
  def __init__(self, service, delay: int = 1, name: str = "anonymous"):
    self.service = service
    self.delay = delay
    self.name = 'WKR:' + name
    self._should_continue = True
    self._timer = None
    self.logger = logging.getLogger(__name__)
    self.run_cycle()

  def run_cycle(self):
    if not self._should_continue:
      return

    self.service.process()

    # 2. Schedule the next cycle in delay seconds
    self._timer = threading.Timer(self.delay, self.run_cycle)
    self._timer.daemon = True
    self._timer.start()

  def stop(self):
    self._should_continue = False
    if self._timer is not None:
      self._timer.cancel()
      self._timer = None

  def start(self):
    if self._should_continue:
      return

    self._should_continue = True
    self.run_cycle()
