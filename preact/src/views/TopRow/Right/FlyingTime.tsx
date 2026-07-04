import useFlightData from "../../../hooks/useFlightData";

const FlyingTime = () => {
  const { detail } = useFlightData();
  const seconds =
    (detail.time.scheduled.arrival ?? 0) -
    (detail.time.scheduled.departure ?? 0);
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  if (seconds === 0) {
    return <div>&nbsp;</div>;
  } else {
    return (
      <div>
        {hours}hr {minutes}mi
      </div>
    );
  }
};

export default FlyingTime;
