export const briefAirlineName = (name: string | undefined) => {
  return name
    ? name
        .replaceAll(/([aA])irlines/g, "")
        .replaceAll(/([aA])irways/g, "")
        .replaceAll(/Air Lines/g, "")
        .trim()
    : "";
};
