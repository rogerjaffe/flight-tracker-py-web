import "./Flag.css";

const Flag = ({country}: { country: string }) => {
  return <img src={`https://flagcdn.com/w320/${country}.png`} alt={country}
              className="flag pr-1"/>
  // return <span className={`fi fi-${country}`} />;
};

export default Flag;
