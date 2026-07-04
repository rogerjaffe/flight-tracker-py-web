def decode_position(adsb: list, direc: str) -> tuple[str, str]:
  val = ''
  direction = ''
  if len(adsb) > 0:
    last_adsb = adsb[-1]
    val = last_adsb.get(direc, None)
    if val is not None:
      if val > 0 and direc == 'lat':
        direction = 'N'
      elif val < 0 and direc == 'lat':
        direction = 'S'
      elif val > 0 and direc == 'lon':
        direction = 'E'
      elif val < 0 and direc == 'lon':
        direction = 'W'
      val = abs(val)
    else:
      val = ''
  return val, direction
