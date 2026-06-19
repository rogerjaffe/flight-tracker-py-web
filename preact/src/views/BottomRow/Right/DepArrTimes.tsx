import earlyOrLate from "../../../utilities/earlyOrLate.ts";
import { formatInTimeZone } from "date-fns-tz";

const DepArrTimes = ({
  dep,
  depTz,
  depTzText,
  arr,
  arrTz,
  arrTzText,
  dep0,
  arr0,
}: {
  dep: number;
  depTz: string;
  depTzText: string;
  arr: number;
  arrTz: string;
  arrTzText: string;
  dep0?: number;
  arr0?: number;
}) => {
  let depClass = dep0 ? earlyOrLate(dep, dep0) : "";
  let arrClass = arr0 ? earlyOrLate(arr, arr0) : "";
  const _dep = formatInTimeZone(new Date(dep * 1000), depTz, "HH:mm");
  const _arr = formatInTimeZone(new Date(arr * 1000), arrTz, "HH:mm");
  return (
    <div>
      <span className={depClass}>{`${_dep} ${depTzText}`}</span> -{" "}
      <span className={arrClass}>{`${_arr} ${arrTzText}`}</span>
    </div>
  );
};

export default DepArrTimes;
