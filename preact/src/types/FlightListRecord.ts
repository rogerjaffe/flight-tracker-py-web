import type { BriefFlight } from "./BriefFlight.ts";
import type { Position } from "./Position.tsx";

export interface FlightListRecord {
  flight: BriefFlight;
  hex: string;
  position: Position[];
}
