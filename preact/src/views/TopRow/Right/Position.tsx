const Position = ({
  lat,
  lon,
}: {
  lat: number | undefined;
  lon: number | undefined;
}) => {
  if (!lat || !lon) return null;
  const latText = Math.abs(lat).toFixed(4);
  const latDir = lat >= 0 ? "N" : "S";
  const lonText = Math.abs(lon).toFixed(4);
  const lonDir = lon >= 0 ? "E" : "W";
  return (
    <>
      <span className="pr-2">
        {latText}
        {latDir}
      </span>
      <span>
        {lonText}
        {lonDir}
      </span>
    </>
  );
};

export default Position;
