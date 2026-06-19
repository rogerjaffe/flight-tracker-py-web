import LeftSide from "./Left";
import Middle from "./Middle";
import Right from "./Right";

const TopRow = () => {
  return (
    <div className="grid grid-cols-14 gap-2 text-center border-black border-b-2">
      <LeftSide />
      <Middle />
      <Right />
    </div>
  );
};

export default TopRow;
