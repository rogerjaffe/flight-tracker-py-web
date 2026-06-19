import { formatInTimeZone } from "date-fns-tz";

const FlightTime = ({
  seconds,
  tz,
  tzText,
}: {
  seconds: number;
  tz: string;
  tzText: string;
}) => {
  const date = new Date(seconds * 1000);
  const text = formatInTimeZone(date, tz, "HH:mm");
  return (
    <span>
      {text} {tzText}
    </span>
  );
};

export default FlightTime;
