import {useState, useEffect} from 'preact/hooks';
import {useAppDispatch} from "../../../store";
import {setRotate, setRotateInterval} from "../../../store/appSlice.ts";

// import {toggleRotate} from "../../../store/appSlice.ts";

interface ViewSettingsModalProps {
  isOpen: boolean;
  onClose: () => void;
  displayRotate: boolean;
  displayRotateInterval: number;
}

export function ViewSettingsModal({isOpen, onClose, displayRotate, displayRotateInterval}: ViewSettingsModalProps) {
  const [enableSwitching, setEnableSwitching] = useState<boolean>(displayRotate);
  const [switchDelay, setSwitchDelay] = useState<number>(displayRotateInterval);
  const dispatch = useAppDispatch();

  const enableSwitchingChange = (e: Event) => {
    const target = e.currentTarget as HTMLInputElement
    setEnableSwitching(Boolean(target.checked));
  }

  const switchDelayChange = (e: Event) => {
    const target = e.currentTarget as HTMLInputElement
    setSwitchDelay(Number(parseInt(target.value ?? 0)));
  }

  const onSave = () => {
    dispatch(setRotate(enableSwitching));
    dispatch(setRotateInterval(switchDelay));
    const jsonString = JSON.stringify({displayRotate: enableSwitching, displayRotateInterval: switchDelay});
    localStorage.setItem("flight-tracker", jsonString);
    onClose();
  }

  useEffect(() => {
    setEnableSwitching(displayRotate);
    setSwitchDelay(displayRotateInterval);
  }, [displayRotate, displayRotateInterval])

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
      {/* Modal Card */}
      <div className="w-full max-w-md overflow-hidden bg-white rounded-xl shadow-2xl border border-gray-100">

        {/* Header */}
        <div className="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
          <h3 className="text-lg font-semibold text-gray-900">View Settings</h3>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors text-xl p-1"
            aria-label="Close modal"
          >
            &times;
          </button>
        </div>

        {/* Form Body */}
        <div className="p-6 space-y-6">

          {/* Checkbox Field */}
          <label className="flex items-start gap-3 cursor-pointer select-none">
            <input
              type="checkbox"
              checked={enableSwitching}
              onChange={enableSwitchingChange}
              className="mt-1 h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500 cursor-pointer"
            />
            <div className="flex flex-col text-left">
              <span className="text-sm font-medium text-gray-900">Enable view switching</span>
              <span className="text-xs text-gray-500">Automatically rotate between views on a timer.</span>
            </div>
          </label>
          <div
            className={`flex items-center gap-3 transition-opacity duration-200 ${enableSwitching ? 'opacity-100' : 'opacity-40'}`}>
            <input
              type="number"
              id="switchDelay"
              min={1}
              max={999}
              disabled={!enableSwitching}
              value={switchDelay + ''}
              onChange={switchDelayChange}
              className="w-[3.5rem] rounded-lg border border-gray-300 bg-white px-2 py-1.5 text-center text-sm text-gray-900 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 disabled:bg-gray-50 disabled:text-gray-400 disabled:border-gray-200 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
            />
            <label htmlFor="switchDelay" className="text-sm font-medium text-gray-700 whitespace-nowrap">
              View switch delay (seconds)
            </label>
          </div>
          {/* Footer Actions */}
          <div className="flex justify-end gap-3 pt-4 border-t border-gray-100">
            <button
              type="button"
              onClick={onClose}
              className="rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-colors"
            >
              Cancel
            </button>
            <button
              type="button"
              onClick={onSave}
              className="btn rounded-lg bg-teal-300 px-4 py-2 text-sm font-medium text-black shadow-sm hover:bg-teal-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-colors"
            >
              Save
            </button>
          </div>

        </div>
      </div>
    </div>
  );
}