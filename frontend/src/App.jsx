import { useState } from "react";
import axios from "axios";

export default function App() {
  const [running, setRunning] = useState(false);
  const [fire, setFire] = useState(false);

  const startCamera = async () => {
    await axios.get("http://localhost:5000/start_camera");
    setRunning(true);
    checkStatus();
  };