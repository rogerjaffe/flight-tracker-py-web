import time
from PySide6.QtCore import Slot, QTimer, Signal
from managers import Mgr
from utilities import http_request


def filter_func(rec: dict):
  hex_ = rec.get('hex', '')
  if hex_ == '' or hex_.startswith('~'):
    return False
  alt = rec.get('alt_baro', None)
  if alt is None or alt == 'ground':
    return False
  return True


class ADSBMgr(Mgr):
  timer: QTimer
  send_adsb_data = Signal(dict)

  def __init__(self, logger, config, adsb_server_config):
    super().__init__(logger, name=f"{adsb_server_config.name}-{adsb_server_config.server_number}", config=config)
    self.server_config = adsb_server_config
    self.adsb_data: dict[str, list[dict]] = {}

  @Slot()
  def activate(self):
    if self.server_config.is_enabled:
      self.timer = QTimer(self)
      self.timer.singleShot(self.server_config.interval * 1000, self.get_adsb_data)

  def get_adsb_data(self):
    adsb_list = {}
    res = http_request(self.server_config.url, 'GET')
    if res is not None:
      data = res[self.server_config.data_path]
      data = list(filter(filter_func, data))
      for rec in data:
        rec['time'] = time.time()
        adsb_list[rec['hex']] = rec
      self.send_adsb_data.emit(adsb_list)

    self.timer.singleShot(self.server_config.interval * 1000, self.get_adsb_data)
