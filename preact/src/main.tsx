import { render } from "preact";
import { App } from "./app.tsx";
import { Provider } from "react-redux";
import "./index.css";
import { store } from "./store";
import { initPythonBridge } from "./bridge/pythonBridge";

initPythonBridge();

render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById("app")!,
);
