def sec_to_hhmmss(sec):
  sec = abs(sec)
  hr_ = int(sec / 3600)
  hr_str = f"{hr_}h" if hr_ > 0 else ""
  min_ = int((sec - (hr_ * 3600)) / 60)
  if hr_ > 0:
    if min_ < 10:
      min_str = f"0{min_}m"
    else:
      min_str = f"{min_}m"
  else:
    min_str = f"{min_}m"
  sec = int(sec % 60)
  sec_str = f"0{sec}s" if sec < 10 else f"{sec}s"
  return f"{hr_str} {min_str} {sec_str}"
