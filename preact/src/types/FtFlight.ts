import type { FtPosition } from "./FtPosition.ts";
import type { ADSB } from "./ADSB.ts";
import type { Flight } from "./Flight.ts";

export interface FtFlight {
  flight: Flight;
  hex: string;
  adsb: ADSB[];
  position: FtPosition;
}
