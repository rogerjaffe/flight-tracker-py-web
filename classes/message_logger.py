import logging


class MessageLogger:
  def __init__(self, logger: logging.Logger):
    self.logger = logger
    self._proxies = []  # Keep strong references to prevent garbage collection

  def connect_and_log(self, signal, slot, signal_name: str, slot_name: str):
    """Automatically intercepts any PySide6 signal and prints its payloads to the log."""

    def proxy(*args):
      # Format the arguments beautifully for debugging
      # payload_preview = [f"{type(a).__name__} (len={len(a)})" if hasattr(a, '__len__') else a for a in args]
      self.logger.info(f"[{signal_name}] -> [{slot_name}]")

      # Call the original slot destination
      slot(*args)

    # Keep a strong reference so the proxy isn't garbage collected
    self._proxies.append(proxy)

    # Connect the signal to our new dynamic proxy worker instead of the raw slot
    signal.connect(proxy)
