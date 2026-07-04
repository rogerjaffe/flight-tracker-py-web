import Left from "./Left";
// import Right from "./Right";

const BottomRow = () => {
  return (
    <div class="col-span-6 row-start-2 row-span-5 gap-2 text-center border-black border-b rotating-content-container">
      <Left />
      {/*<Right />*/}
    </div>
  );
};

export default BottomRow;
