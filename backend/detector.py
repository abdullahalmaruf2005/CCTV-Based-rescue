from ultralytics import YOLO
import cv2

fire_model = YOLO("weights/best.pt")

try:
    accident_model = YOLO("weights/accident.pt")
except Exception:
    accident_model = None

def detect_fire(frame):
    detected = False
    detected_type = None

    fire_results = fire_model(frame, imgsz=640, conf=0.5, verbose=False)

    for result in fire_results:
        for box in result.boxes:
            detected = True
            detected_type = "fire"
            conf = float(box.conf[0])
            cid = int(box.cls[0])
            x1,y1,x2,y2 = map(int, box.xyxy[0])

            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,0,255),2)
            cv2.putText(frame,f"{fire_model.names[cid]} {conf:.2f}",(x1,max(20,y1-10)),
                        cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,255),2)

    if accident_model is not None:
        acc_results = accident_model(frame, imgsz=640, conf=0.5, verbose=False)

        for result in acc_results:
            for box in result.boxes:
                detected = True
                detected_type = "accident"
                conf = float(box.conf[0])
                cid = int(box.cls[0])
                x1,y1,x2,y2 = map(int, box.xyxy[0])

                cv2.rectangle(frame,(x1,y1),(x2,y2),(255,0,0),2)
                cv2.putText(frame,f"{accident_model.names[cid]} {conf:.2f}",(x1,max(20,y1-10)),
                            cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,0,0),2)

    return frame, detected, detected_type
