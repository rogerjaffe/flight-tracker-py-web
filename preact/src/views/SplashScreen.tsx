// src/components/SplashScreen.tsx
import { type FunctionalComponent } from "preact";

export const SplashScreen: FunctionalComponent = () => {
  return (
    <div className="w-5xl h-150 flex flex-col items-center justify-center bg-slate-900 text-white select-none overflow-hidden">
      {/* Flight Icon Graphic Container */}
      <div className="mb-6 relative flex items-center justify-center">
        {/* Modern Spinning Ring Loader */}
        <div className="w-20 h-20 border-4 border-slate-700 border-t-sky-500 rounded-full animate-spin" />

        {/* Static Center Icon (Aircraft Silhouette) */}
        <svg
          className="w-8 h-8 text-sky-400 absolute"
          fill="currentColor"
          viewBox="0 0 24 24"
        >
          <path d="M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z" />
        </svg>
      </div>

      {/* Brand Branding */}
      <h1 className="text-6xl font-extrabold tracking-wider text-slate-100 mb-2 drop-shadow-sm">
        Flight Tracker
      </h1>

      {/* Subtext Status */}
      <div className="flex items-center gap-2 text-lg text-slate-400 font-medium">
        <span>Loading systems</span>
        <span className="flex gap-0.5">
          <span className="animate-bounce [animation-delay:-0.3s]">.</span>
          <span className="animate-bounce [animation-delay:-0.15s]">.</span>
          <span className="animate-bounce">.</span>
        </span>
      </div>
    </div>
  );
};
