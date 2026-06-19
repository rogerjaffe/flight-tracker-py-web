import { intervalToDuration, type Duration } from "date-fns";

/**
 * Converts a total number of seconds into a formatted time string.
 * Returns "mm:ss" if hours are 0, or "HH:mm:ss" if hours are greater than 0.
 *
 * @param totalSeconds - The total duration in seconds.
 * @returns Formatted time string (e.g., "05:12" or "02:05:12").
 */
function formatSecondsToHMS(totalSeconds: number): string {
  if (totalSeconds === 0) return "0m 00s";
  const duration: Duration = intervalToDuration({
    start: new Date(0),
    end: new Date(totalSeconds * 1000),
  });

  const zeroPad = (num: number | undefined): string =>
    String(num ?? 0).padStart(2, "0");

  const hrs: number = duration.hours ?? 0;
  const mins: string =
    hrs > 0 ? zeroPad(duration.minutes) : duration.minutes + "";
  const secs: string = zeroPad(duration.seconds);

  // Omit hours if 0, otherwise include zero-padded hours
  return hrs === 0 ? `${mins}:${secs}` : `${zeroPad(hrs)}:${mins}:${secs}`;
}

export default formatSecondsToHMS;
