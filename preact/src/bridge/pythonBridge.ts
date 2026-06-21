import {QWebChannel} from "qwebchannel";
import {store} from "../store"; // Your configured RTK store
import {setFlightData} from "../store/flightSlice";
import {setAppConfig} from "../store/appSlice.ts";

declare global {
  interface Window {
    QtWebChannel: any;
    qt: { webChannelTransport: any };
  }
}

let backend: any = null;

export function initPythonBridge() {
  console.log("initPythonBridge");

  if (!window.qt?.webChannelTransport) {
    console.log(
      "initPythonBridge: window.qt.webChannelTransport not available",
    );
    return;
  }

  console.log("initPythonBridge: window.qt.webChannelTransport available");

  new QWebChannel(window.qt.webChannelTransport, async (channel: any) => {
    console.log("initPythonBridge: QWebChannel created");
    console.log("initPythonBridge: channel objects:", channel.objects);

    backend = channel.objects.backend;

    if (!backend) {
      console.error("initPythonBridge: backend object not found");
      return;
    }

    if (!backend.flight || !backend.config) {
      console.error("initPythonBridge: backend.flight signal not found");
      return;
    }

    console.log("initPythonBridge: backend object:", backend);

    backend.flight.connect((jsonString: string) => {
      store.dispatch(setFlightData(jsonString));
    });

    backend.status.connect((error: string) => {
      console.log("initPythonBridge: backend status:", error);
    });

    try {
      const configJsonString = await channel.objects.backend.fetch_config();
      console.log(configJsonString);
      store.dispatch(setAppConfig(configJsonString));

      // store.dispatch(setAppConfig(configJsonString));
    } catch (error) {
      console.error(
        "Failed to fetch initial configuration from backend",
        error,
      );
    }

    console.log("initPythonBridge: connected to backend.flight");
  });
}

export function setFlight(hexCode: string) {
  if (!backend) {
    console.error("setPythonFlight: backend is not ready");
    return;
  }

  if (!hexCode) {
    console.error("setPythonFlight: hexCode is required");
    return;
  }

  backend.set_flight(hexCode);
}
