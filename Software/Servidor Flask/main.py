#!/usr/bin/env python

from flask import Flask, render_template, Response
from camera import VideoCamera
import serial, sys, glob, time, thread

app = Flask(__name__)

try:
	arduino = serial.Serial('/dev/ttyUSB0', 9600)
except:
	print('Nao foi possivel detctar o arduino.')
	pass
finally:
	print('Finally')
	

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
                    
@app.route('/up')
def up():
	print('[INFO] Up')
	arduino.write("1200\n") 
	return "nothing"
                    
@app.route('/down')
def down():
	print('[INFO] Down')
	arduino.write("2200\n")   
	return "nothing"

@app.route('/left')
def left():
	print('[INFO] Left')
	arduino.write("3100\n")   
	return "nothing"

@app.route('/right')
def right():
	print('[INFO] Right')
	arduino.write("4100\n")    
	return "nothing"

@app.route('/stop')
def stop():
	print('[INFO] Stop')
	arduino.write("1000\n")  
	return "nothing"

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, debug=True)

