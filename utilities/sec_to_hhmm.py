def sec_to_hhmm(sec):
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
  return f"{hr_str} {min_str}"
