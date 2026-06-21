import {useEffect, useRef} from 'preact/hooks';

type Delay = number | null;
type Callback = () => void;

export function useInterval(callback: Callback, delay: Delay = null): void {
  const savedCallback = useRef<Callback>(callback);

  // Remember the latest callback if it changes
  useEffect(() => {
    savedCallback.current = callback;
  }, [callback]);

  // Set up the interval
  useEffect(() => {
    // Skip setting interval if delay is null
    if (delay === null) return;

    const tick = () => savedCallback.current();
    const id = setInterval(tick, delay);

    // Clean up interval on unmount or delay change
    return () => clearInterval(id);
  }, [delay]);
}