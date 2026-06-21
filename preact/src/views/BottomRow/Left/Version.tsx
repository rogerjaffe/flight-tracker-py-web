import pkg from "../../../../package.json";

const Version = () => <div className="text-xs italic text-left pl-2 pt-1">Version {pkg.version}</div>

export default Version;