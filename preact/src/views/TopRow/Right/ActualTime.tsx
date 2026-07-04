import useFlightData from "../../../hooks/useFlightData";

const ActualTime = () => {
  const {detail} = useFlightData();
  const secondsScheduled =
    (detail.time.scheduled.arrival ?? 0) -
    (detail.time.scheduled.departure ?? 0);
  const secondsActual =
    (detail.time.estimated.arrival ?? 0) -
    (detail.time.real.departure ?? 0);
  const diff = secondsScheduled - secondsActual;
  const hoursActual = Math.floor(secondsActual / 3600);
  const minutesActual = Math.floor((secondsActual % 3600) / 60);
  const hoursDiff = Math.floor(diff / 3600);
  const minutesDiff = Math.floor((diff % 3600) / 60);
  const classNameDiff = diff > 0 ? "text-green-500" : "text-red-500";
  if (secondsActual === 0) {
    return <div>&nbsp;</div>;
  } else {
    return (
      <div>
        <span>{hoursActual}hr {minutesActual}mi</span>
        <span className={classNameDiff}>
          {" "}({hoursDiff === 0 ? '' : hoursDiff + 'hr '}{minutesDiff + 'mi'})
        </span>
      </div>
    );
  }
};

export default ActualTime;
