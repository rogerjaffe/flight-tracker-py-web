import Left from "./Left";
import Right from "./Right";

const BottomRow = () => {
  return (
    <div class="grid grid-cols-4 gap-2 text-center border-black border-b rotating-content-container">
      <Left />
      <Right />
    </div>
  );
};

export default BottomRow;
