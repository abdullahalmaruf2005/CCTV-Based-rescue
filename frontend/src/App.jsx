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
    return (
    <div className="bg-black min-h-screen text-white p-6">
      <h1 className="text-3xl font-bold text-red-500">Fire & Smoke Detection</h1>

      <div className="mt-6 flex gap-4">
        <button onClick={startCamera} className="bg-green-600 px-4 py-2 rounded">
          Start Camera
        </button>
         <button onClick={stopCamera} className="bg-red-600 px-4 py-2 rounded">
          Stop Camera
        </button>
      </div>
      {fire && (
        <div className="mt-4 bg-red-700 p-4 text-xl animate-pulse">
          FIRE / SMOKE DETECTED!
        </div>
      )}
       <div className="mt-6">
        <img src="http://localhost:5000/video_feed" className="rounded-lg border" />
      </div>
    </div>
  );
}