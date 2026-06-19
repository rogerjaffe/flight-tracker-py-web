import formatSecondsToHMS from "../../utilities/formatSecondsToHMS.ts";

const EarlyLate = ({ t, t0 }: { t: number; t0: number }) => {
  const tDiff = t - t0;
  const absDiff = Math.abs(tDiff);
  const className = tDiff >= 60 ? "text-red-500" : "text-green-500";

  return <span className={className}>{formatSecondsToHMS(absDiff)}</span>;
};

export default EarlyLate;
