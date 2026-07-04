arrows = {
  "up": "▲",
  "right": "▶",
  "ud-flat": "",
  "down": "▼",
  "left": "◀",
  "lr-flat": ""
};


def get_arrow_and_class(sign: int, direction: str) -> tuple[str, str]:
  if direction == 'ud':
    if sign > 0:
      return arrows['up'], 'inc'
    elif sign < 0:
      return arrows['down'], 'dec'
    else:
      return arrows['ud-flat'], ''
  elif direction == 'lr':
    if sign > 0:
      return arrows['right'], 'inc'
    elif sign < 0:
      return arrows['left'], 'dec'
    else:
      return arrows['lr-flat'], ''
  else:
    return '', ''


def get_value_arrow_class(adsb, key: str, direction: str) -> tuple[str, str, str]:
  val = ''
  arrow = ''
  class_name = ''

  length = len(adsb)
  if length == 1:
    last_adsb = adsb[0]
    val = last_adsb.get(key, '')
  else:
    adsb0 = adsb[-1]
    adsb1 = adsb[-2]
    val = adsb0.get(key, 0)
    val1 = adsb1.get(key, 0)
    arrow, class_name = get_arrow_and_class(val - val1, direction)
  return f"{round(val):,}", arrow, class_name
