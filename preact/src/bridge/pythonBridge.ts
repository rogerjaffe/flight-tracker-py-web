import { QWebChannel } from "qwebchannel";
import { store } from "../store";
import { setConfig } from "../store/configSlice.ts";
import { setFlightList } from "../store/flightListSlice.ts";
import { setDarkmode } from "../store/appSlice.ts";
import { setFlightInfo } from "../store/flightInfoSlice.ts"; // Your configured RTK store
// import {setFlightData} from "../store/flightSlice";
// import {setAppConfig} from "../store/appSlice.ts";

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

    if (!backend.send_config) {
      console.error("initPythonBridge: backend signal(s) not found");
      return;
    }

    console.log("initPythonBridge: backend object:", backend);

    // backend.send_flight_data.connect((list: string) => {
    //   console.log("initPythonBridge: backend send_flight_data:", list);
    // });

    backend.send_darkmode.connect((jsonData: any) => {
      console.log("initPythonBridge: backend send_darkmode:", jsonData);
      store.dispatch(setDarkmode(jsonData));
    });

    backend.send_config.connect((jsonData: any) => {
      console.log("initPythonBridge: backend send_config:", jsonData);
      store.dispatch(setConfig(jsonData));
    });

    backend.send_flight_list.connect((jsonData: any) => {
      console.log("send_flight_list", jsonData);
      store.dispatch(setFlightList(jsonData));
    });

    backend.send_flight_data.connect((jsonData: any) => {
      console.log("send_flight_data", jsonData);
      store.dispatch(setFlightInfo(jsonData));
    });

    if (typeof backend.preact_ready === "function") {
      backend.preact_ready();
    } else {
      console.error("initPythonBridge: backend.preact_ready slot not found");
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
