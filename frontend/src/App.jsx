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

  const stopCamera = async () => {
      await axios.get("http://localhost:5000/stop_camera");
      setRunning(false);
    };
  
    const checkStatus = () => {
      setInterval(async () => {
        const res = await axios.get("http://localhost:5000/status");
        setFire(res.data.fire);
      }, 1000);
    };