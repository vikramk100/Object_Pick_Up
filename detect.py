 
from ultralytics import YOLO
import numpy as np
import cv2
import serial.tools.list_ports

model = YOLO('yolov8n.pt')
cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()

    results = model.track(frame, persist = True)
    results = results[0]
    frame_p = results.plot()

    for box in results.boxes:
      coord = box.xywhn[0].tolist()
      clss = box.cls[0].item()
      conf = box.conf[0].item()

      print(f"Class: {model.names[clss]}, Confidence: {conf:.2f}")
      print(f"Coordinates: center_x_norm={coord[0]:.5f}, center_y_norm={coord[1]:.5f}, "
            f"width_norm={coord[2]:.5f}, height_norm={coord[3]:.05}")
      print("-" * 50)


    cv2.imshow('frame', frame_p)
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break

      
cap.release()
cv2.destroyALLWindows()
