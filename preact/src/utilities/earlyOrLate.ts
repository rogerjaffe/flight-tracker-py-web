const earlyOrLate = (time: number, compareTo: number) =>
  time < compareTo ? "text-green-500" : "text-red-500";

export default earlyOrLate;
