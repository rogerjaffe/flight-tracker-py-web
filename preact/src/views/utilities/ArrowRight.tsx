const ArrowRight = ({size = 24, color = "currentColor"}: { size?: number, color?: string }) => {
  return (
    <svg
      xmlns="http://w3.org"
      viewBox="0 0 24 24"
      width={size}
      height={size}
      fill={color}
      style={{display: 'inline-block', verticalAlign: 'middle'}}
    >
      <path d="M2 9.5h12v-4.5l8 7-8 7v-4.5h-12z"/>
    </svg>
  );
}

export default ArrowRight;