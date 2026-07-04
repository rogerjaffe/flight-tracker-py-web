def has_late(t0: int, t1: int) -> str:
  if t0 - t1 < 0:
    return 'late'
  elif t0 - t1 > 0:
    return 'early'
  else:
    return ''
