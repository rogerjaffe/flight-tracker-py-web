const getAltitudeColor = (value: number) => {
  // Define the custom anchor points and their RGB colors
  const anchors = [
    {val: 0, r: 180, g: 0, b: 0},       // Dark Red
    {val: 1500, r: 185, g: 100, b: 0},  // Dark Orange
    {val: 5000, r: 130, g: 130, b: 0},  // Dark Yellow / Olive
    {val: 8000, r: 0, g: 125, b: 0},    // Dark Green
    {val: 20000, r: 0, g: 110, b: 150}, // Dark Light Blue
    {val: 30000, r: 0, g: 0, b: 180},   // Dark Blue
    {val: 40000, r: 90, g: 0, b: 170},  // Dark Violet
  ];
  // Handle edge cases outside the range
  if (value <= anchors[0].val)
    return `rgb(${anchors[0].r}, ${anchors[0].g}, ${anchors[0].b})`;
  if (value >= anchors[anchors.length - 1].val) {
    const last = anchors[anchors.length - 1];
    return `rgb(${last.r}, ${last.g}, ${last.b})`;
  }

  // Find the two bounding anchors
  for (let i = 0; i < anchors.length - 1; i++) {
    const c0 = anchors[i];
    const c1 = anchors[i + 1];

    if (value >= c0.val && value <= c1.val) {
      // Linear interpolation factor (0.0 to 1.0)
      const t = (value - c0.val) / (c1.val - c0.val);

      // Calculate intermediate RGB values
      const r = Math.round(c0.r + (c1.r - c0.r) * t);
      const g = Math.round(c0.g + (c1.g - c0.g) * t);
      const b = Math.round(c0.b + (c1.b - c0.b) * t);

      return `rgb(${r}, ${g}, ${b})`;
    }
  }
};

export default getAltitudeColor;
