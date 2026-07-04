type Direction = 'inc' | 'dec' | '';

export interface FtPosition {
  altitude: number;
  altitude_dir: Direction;

  ground_speed: number;
  ground_speed_dir: Direction;

  heading: number;
  heading_dir: Direction;

  vertical_speed: number;
  vertical_speed_dir: Direction;

  latitude: number;
  longitude: number;
  time: number;
}