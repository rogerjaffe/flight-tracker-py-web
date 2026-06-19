import logging

SUPPRESS_TEXT = "failed to decode Content-Encoding='gzip'"


class TextSuppressionFilter(logging.Filter):
  def __init__(self):
    super().__init__()
    self.forbidden_text = SUPPRESS_TEXT

  def filter(self, record):
    # Return False to suppress the log, True to keep it
    return self.forbidden_text not in record.getMessage()
