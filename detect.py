
from ultralytics import YOLO
import numpy as np
import cv2
import serial.tools.list_ports
import time
from flask import Flask, request, jsonify
from flask_cors import CORS 
import threading


# Action values: 1 = find object, 2 = follow object, 3 = pick up object
action = 1  # Default action is to find object

app = Flask(__name__)
CORS(app)

@app.route('/update_action', methods=['POST'])
def update_action():
    global action
    data = request.json
    action = data.get('action', 1)
    return jsonify({'status': 'success', 'action': action})

def run_detection():
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

    while True:
        ret, frame = cap.read()

        results = model.track(frame, persist = True)
        results = results[0]
        frame_p = results.plot()

        for box in results.boxes:
            coord = box.xywhn[0].tolist()
            clss = box.cls[0].item()
            conf = box.conf[0].item()

            vals = [float(coord[0]), float(coord[1]), float(coord[2]), float(coord[3])]

        # Include action in the data string
        if vals:
          data_string = f"{action},{vals[0]:.5f},{vals[1]:.5f},{vals[2]:.5f},{vals[3]:.5f}\n"

        else:
            data_string = f"{action},0.0,0.0,0.0,0.0\n" 
        arduino.write(data_string.encode())
        print(f"Sent to Arduino: {data_string.strip()}")
        response = arduino.readline().decode('utf-8', errors='ignore').strip()
        if response:
            print(f"Received from Arduino: {response}")

        cv2.imshow('frame', frame_p)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if arduino:
        arduino.close()

if __name__ == '__main__':
    # Start the detection loop in a separate thread
    detection_thread = threading.Thread(target=run_detection)
    detection_thread.daemon = True
    detection_thread.start()
    
    # Start the Flask server
    app.run(host='0.0.0.0', port=5000)
