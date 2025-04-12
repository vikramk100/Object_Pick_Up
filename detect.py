from ultralytics import YOLO
import numpy as np
import cv2
import serial.tools.list_ports
import time

model = YOLO('yolov8n.pt')
cap = cv2.VideoCapture(1)

ports = serial.tools.list_ports.comports()
arduino_port = None
for port in ports:
    if 'Arduino' in port.description:
        arduino_port = port.device
        break


if arduino_port:
    arduino = serial.Serial(arduino_port, 9600, timeout=1)
    time.sleep(2)  # Wait for connection to establish
    print(f"Connected to Arduino on {arduino_port}")
else:
    print("Arduino not found!")
    arduino = None

vals = None

for i in range(40):
    ret, frame = cap.read()

    results = model.track(frame, persist = True)
    results = results[0]
    frame_p = results.plot()

    for box in results.boxes:
      coord = box.xywhn[0].tolist()
      clss = box.cls[0].item()
      conf = box.conf[0].item()

      vals = [float(coord[0]), float(coord[1]), float(coord[2]), float(coord[3])]


    cv2.imshow('frame', frame_p)
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break



print(f"Coordinates: center_x_norm={coord[0]:.5f}, center_y_norm={coord[1]:.5f}, "
      f"width_norm={coord[2]:.5f}, height_norm={coord[3]:.05}")

if vals and arduino:
    data_string = f"{vals[0]:.5f},{vals[1]:.5f},{vals[2]:.5f},{vals[3]:.5f}\n"
    arduino.write(data_string.encode())
    print(f"Sent to Arduino: {data_string.strip()}")
      
cap.release()
cv2.destroyALLWindows()

if arduino:
    arduino.close()