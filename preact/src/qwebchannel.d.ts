declare module "qwebchannel" {
  export class QWebChannel {
    constructor(
      transport: any,
      initCallback: (channel: { objects: any }) => void,
    );
    objects: any;
  }
}
