from flask import Flask, Response, jsonify
from flask_cors import CORS
import cv2
import pygame
import time
import requests
from detector import detect_fire

app = Flask(__name__)

# ✅ CORS FIX
CORS(app, resources={r"/*": {"origins": "*"}})

# 🔊 SAFE AUDIO INIT
try:
    pygame.mixer.init()
    alarm_sound = pygame.mixer.Sound("alarm.mp3")
except:
    alarm_sound = None
    print("Audio init failed")

# 📷 Camera state
camera = None
camera_running = False
fire_detected = False

# 🔥 Telegram config
TELEGRAM_BOT_TOKEN = "8772768466:AAE5LstS86HbBGTGHL8fTVKn1GLZjojLOsI"
TELEGRAM_CHAT_ID = "6102913867"

# ⏱️ cooldown
_last_alert_time = 0


# 📩 Telegram alert
def send_telegram_alert(msg):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            json={"chat_id": TELEGRAM_CHAT_ID, "text": msg},
            timeout=5
        )
    except Exception as e:
        print("Telegram error:", e)


# 🎥 SAFE FRAME LOOP (NO CRASH)
def generate_frames():
    global camera_running, camera, fire_detected, _last_alert_time

    while camera_running and camera is not None:
        try:
            ok, frame = camera.read()
            if not ok:
                time.sleep(0.05)
                continue

            frame = cv2.resize(frame, (640, 480))

            # 🔥 SAFE detection
            detected = False
            try:
                result = detect_fire(frame)
                if result is not None:
                    frame, detected, detected_type = result
            except Exception as e:
                print("Detection error:", e)
                detected = False

            fire_detected = detected

            # 🔊 Alarm safe
            try:
                if alarm_sound:
                    if detected:
                        if not pygame.mixer.get_busy():
                            alarm_sound.play(-1)
                    else:
                        alarm_sound.stop()
            except:
                pass

            # 📩 Telegram (30 sec cooldown)
            if detected:
                now = time.time()
                if now - _last_alert_time > 30:
                    send_telegram_alert("🔥Maruf Fire detected!" if detected_type=="fire" else "🚗Maruf Accident detected!")
                    _last_alert_time = now

            # 🎥 encode frame
            try:
                ret, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                if not ret:
                    continue
            except:
                continue

            time.sleep(0.05)  # 🔥 CPU CONTROL (IMPORTANT)

            yield (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' +
                buffer.tobytes() +
                b'\r\n'
            )

        except Exception as e:
            print("Loop recovered:", e)
            time.sleep(0.2)
            continue


# 🏠 Home
@app.route("/")
def home():
    return jsonify({"message": "Backend Running Successfully"})


# 📷 Start camera
@app.route("/start_camera")
def start_camera():
    global camera, camera_running

    try:
        if camera_running:
            return jsonify({"message": "Already Running"})

        camera = cv2.VideoCapture(0)

        if not camera.isOpened():
            return jsonify({"error": "Camera not found"}), 500

        camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # 🔥 Mac stability fix

        camera_running = True
        return jsonify({"message": "Camera Started"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🛑 Stop camera
@app.route("/stop_camera")
def stop_camera():
    global camera, camera_running

    camera_running = False

    try:
        if camera:
            camera.release()
            camera = None

        if alarm_sound:
            alarm_sound.stop()

        return jsonify({"message": "Camera Stopped"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 📊 Status
@app.route("/status")
def status():
    return jsonify({"fire_detected": fire_detected})


# 🎥 Video feed
@app.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True, threaded=True)