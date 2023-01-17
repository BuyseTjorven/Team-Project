#region **** IMPORTS ****
import json
from flask_socketio import SocketIO, emit, send
from flask import Flask, jsonify, request
from flask_cors import CORS
#endregion
import time
import paho.mqtt.client as mqtt
import random
import threading
started = 0
publish = 0
btn_choiche = 0
def on_publish(client, userdata, mid):
    #voorlopig niks
    pass 
def callback_esp32_sensor1(client, userdata, msg):
    print('ESP sensor1 data: ', msg.payload.decode('utf-8'))
def callback_esp32_sensor2(client, userdata, msg):
    print('ESP sensor2 data: ', str(msg.payload.decode('utf-8')))
def callback_rpi_esp5(client, userdata, msg):
    print('send naar esp5: ', str(msg.payload.decode('utf-8')))
def callback_esp32_sensor5(client, userdata, msg):
    global started
    global publish
    global btn_choiche
    print('ESP sensor5 data: ', str(msg.payload.decode('utf-8')))
    if(started ==1):
        print('test succes')
        publish = 1
        btn_choiche = random.randint(4,5)
        print(btn_choiche)
    elif(started == 0):
        started = 1
def callback_rpi_broadcast(client, userdata, msg):
    print('RPi Broadcast message:  ', str(msg.payload.decode('utf-8')))
def client_subscriptions(client):
    client.subscribe("esp32/#")
    client.subscribe("rpi/broadcast")
def on_connect(client, userdata, flags, rc):
   global flag_connected
   flag_connected = 1
   client_subscriptions(client)
   print("Connected to MQTT server")
def on_disconnect(client, userdata, rc):
   global flag_connected
   flag_connected = 0
   print("Disconnected from MQTT server")


#region **** INIT ****
# Start app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheim!'
socketio = SocketIO(app, cors_allowed_origins="*", logger=False, engineio_logger=False, ping_timeout=1)
CORS(app)

#endregion



# SOCKET.IO EVENTS
@socketio.on('connect')
def initial_connection():
    print('A new client connect')

@socketio.on('1vs1')
def newOneVsOne(testvariabl):
    print('1vs1', testvariabl)
    #y = json.dumps(testvariabl)
    print(type(testvariabl))
    print(testvariabl["name1"])

@socketio.on('Speedrun')
def newSpeedrun(testvariabl):
    print('Speedrun', testvariabl)
    #y = json.dumps(testvariabl)
    print(type(testvariabl))
    print(testvariabl["name"])

@socketio.on('test')
def test():
    print('test')

def mqttrun():
    global started
    global publish
    global btn_choiche
    client = mqtt.Client("rpi_client2") #this name should be unique
    client.on_publish = on_publish
    flag_connected = 0
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.message_callback_add('esp32/sensor1', callback_esp32_sensor1)
    client.message_callback_add('esp32/sensor2', callback_esp32_sensor2)
    client.message_callback_add('esp32/sensor5', callback_esp32_sensor5)
    client.message_callback_add('esp32/sensor4', callback_esp32_sensor5)
    client.message_callback_add('rpi/broadcast', callback_rpi_broadcast)
    client.message_callback_add('esp32/kleur5', callback_rpi_esp5)
    client.connect('127.0.0.1',1883)
    client.loop_start()
    client_subscriptions(client)
    print("......client setup complete............")
    # start a new thread
    client.loop_start()
    while True:
        try:
            if(publish == 1):
                print("enter")
                msg ='led_uit'
                pubMsg = client.publish(
                    topic='rpi/broadcast',
                    payload=msg.encode('utf-8'),
                    qos=0,
                    )
                pubMsg.wait_for_publish()
                print("succes")
                #hier komt normaal dan random esp kiezen en die aanzetten
                #voorlopig gewoon delay en zelfde terug aan
                msg ='0x00FF00'
                pubMsg = client.publish(
                    topic=f'esp32/kleur{btn_choiche}',
                    payload=msg.encode('utf-8'),
                    qos=0,
                    )
                pubMsg.wait_for_publish()
                print("succes2")
                started = 0
                publish = 0
                btn_choiche = 0
        
        except Exception as e:
            print(e)
# START THE APP
if __name__ == '__main__':
    try:
        print("in de try")
        thread = threading.Thread(target=mqttrun, args=(), daemon=True)
        thread.start()
        print("thread gestart")
        print("backend running")
        socketio.run(app, debug=False, host='0.0.0.0')
    except KeyboardInterrupt:
        print('KeyboardInterrupt exception is caught')