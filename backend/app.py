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
from datetime import datetime, timedelta
from repositories.DataRepository import DataRepository
from repositories.Database import Database
#region **** variables ****
started = 0
tijd = datetime.now()
tijd_start = datetime.now()
tijd_end = datetime.now()
tijd_set=0
tijd_cooldown = datetime.now()
tijd_cooldown_start = datetime.now()
publish = 0
power_off =0
game_progress = 0
btn_choiche1= 0
btn_choiche2=0
name1, name2, color1,color2, degree, buttonGoal,minutes = "","", "", "", "", "",""
score1,score2=0,0
score1_oud, score2_oud = 0,0
timerstart=0
color_choiche = ""
game_bezig = 0
aantal_knoppen = 0
selected_gamemode_old=0
selected_gamemode = 0 # 1 = speedrun, 2 = 1v1, 3 = simon says, 4 = shuttle run
speedrun_init = 0
#endregion
# Custom endpoint
endpoint = '/api/v1'


def on_publish(client, userdata, mid):
    #voorlopig niks
    pass 
#region **** ESPcallback ****
def callback_esp32_sensor1(client, userdata, msg):
    global btn_choiche1, btn_choiche2, score1, score2,started , selected_gamemode,score1_oud, score2_oud,game_progress
    if(selected_gamemode == 1):
        if(started==1 or btn_choiche1 == 1):
            speedrun_next(client, userdata, msg)
            started = 0
    elif(selected_gamemode == 2):
        if(started==1):
            multiplayer_init(client, userdata, msg)
            started = 0
        if(started==0 and btn_choiche1 == 1):
            score1_oud = score1
            score2_oud = score2
            score1 = score1+1
            multiplayer_next(client, userdata, msg)
        if(started==0 and btn_choiche2 == 1):
            score1_oud = score1
            score2_oud = score2
            score2 = score2+1
            multiplayer_next(client, userdata, msg)
    elif(selected_gamemode == 3):
        if(started == 0 and btn_choiche1 == 1):
            print("next")
            game_progress = game_progress+1
            shuttlerun_next(client, userdata, msg)
        if(started == 1):
            print("init")
            started = 0
            shuttlerun_init(client, userdata, msg)
    print("knop 1")
def callback_esp32_sensor2(client, userdata, msg):
    global btn_choiche1, btn_choiche2, score1, score2,started , selected_gamemode,score1_oud, score2_oud,game_progress
    if(selected_gamemode == 1):
        if(started==1 or btn_choiche1 == 2):
            speedrun_next(client, userdata, msg)
            started = 0
    elif(selected_gamemode == 2):
        if(started==1):
            multiplayer_init(client, userdata, msg)
            started = 0
        if(started==0 and btn_choiche1 == 2):
            score1_oud = score1
            score2_oud = score2
            score1 = score1+1
            multiplayer_next(client, userdata, msg)
        if(started==0 and btn_choiche2 == 2):
            score1_oud = score1
            score2_oud = score2
            score2 = score2+1
            multiplayer_next(client, userdata, msg)
    elif(selected_gamemode == 3):
        if(started == 0 and btn_choiche1 == 2):
            print("next")
            game_progress = game_progress+1
            shuttlerun_next(client, userdata, msg)
        if(started == 1):
            print("init")
            started = 0
            shuttlerun_init(client, userdata, msg)
    print("knop 2")
def callback_esp32_sensor3(client, userdata, msg):
    global btn_choiche1, btn_choiche2, score1, score2,started , selected_gamemode,score1_oud, score2_oud,game_progress
    if(selected_gamemode == 1):
        if(started == 1 or btn_choiche1 == 3):
            speedrun_next(client, userdata, msg)
            started = 0
    elif(selected_gamemode == 2):
        if(started==1):
            multiplayer_init(client, userdata, msg)
            started = 0
        if(started==0 and btn_choiche1 == 3):
            score1_oud = score1
            score2_oud = score2
            score1 = score1+1
            multiplayer_next(client, userdata, msg)
        if(started==0 and btn_choiche2 == 3):
            score1_oud = score1
            score2_oud = score2
            score2 = score2+1
            multiplayer_next(client, userdata, msg)
    elif(selected_gamemode == 3):
        if(started == 0 and btn_choiche1 == 3):
            print("next")
            game_progress = game_progress+1
            shuttlerun_next(client, userdata, msg)
        if(started == 1):
            print("init")
            started = 0
            shuttlerun_init(client, userdata, msg)
    print("knop 3")
def callback_esp32_sensor4(client, userdata, msg):
    global btn_choiche1, btn_choiche2, score1, score2,started , selected_gamemode,score1_oud, score2_oud,game_progress
    if(selected_gamemode == 1):
        if(started ==1 or btn_choiche1 == 4):
            speedrun_next(client, userdata, msg)
            started = 0
    elif(selected_gamemode == 2):
        if(started==1):
            multiplayer_init(client, userdata, msg)
            started = 0
        if(started==0 and btn_choiche1 == 4):
            score1_oud = score1
            score2_oud = score2
            score1 = score1+1
            multiplayer_next(client, userdata, msg)
        if(started==0 and btn_choiche2 == 4):
            score1_oud = score1
            score2_oud = score2
            score2 = score2+1
            multiplayer_next(client, userdata, msg)
    elif(selected_gamemode == 3):
        if(started == 0 and btn_choiche1 == 4):
            print("next")
            game_progress = game_progress+1
            shuttlerun_next(client, userdata, msg)
        if(started == 1):
            print("init")
            started = 0
            shuttlerun_init(client, userdata, msg)
    print("knop 4")
def callback_esp32_sensor5(client, userdata, msg):
    global btn_choiche1, btn_choiche2, score1, score2,started , selected_gamemode,score1_oud, score2_oud,game_progress
    if(selected_gamemode == 1):
        if(started == 1 or btn_choiche1 == 5):
            speedrun_next(client, userdata, msg)
            started = 0
    elif(selected_gamemode == 2):
        if(started==1):
            multiplayer_init(client, userdata, msg)
            started = 0
        if(started==0 and btn_choiche1 == 5):
            score1_oud = score1
            score2_oud = score2
            score1 = score1+1
            multiplayer_next(client, userdata, msg)
        if(started==0 and btn_choiche2 == 5):
            score1_oud = score1
            score2_oud = score2
            score2 = score2+1
            multiplayer_next(client, userdata, msg)
    elif(selected_gamemode == 3):
        if(started == 0 and btn_choiche1 == 5):
            print("next")
            game_progress = game_progress+1
            shuttlerun_next(client, userdata, msg)
        if(started == 1):
            print("init")
            started = 0
            shuttlerun_init(client, userdata, msg)
    print("knop 5")
def callback_esp32_sensor6(client, userdata, msg):
    global btn_choiche1, btn_choiche2, score1, score2,started , selected_gamemode,score1_oud, score2_oud,game_progress
    if(selected_gamemode == 1):
        if(started == 1 or btn_choiche1 == 6):
            speedrun_next(client, userdata, msg)
            started = 0
    elif(selected_gamemode == 2):
        if(started==1):
            multiplayer_init(client, userdata, msg)
            started = 0
        if(started==0 and btn_choiche1 == 6):
            score1_oud = score1
            score2_oud = score2
            score1 = score1+1
            multiplayer_next(client, userdata, msg)
        if(started==0 and btn_choiche2 == 6):
            score1_oud = score1
            score2_oud = score2
            score2 = score2+1
            multiplayer_next(client, userdata, msg)
    elif(selected_gamemode == 3):
        if(started == 0 and btn_choiche1 == 6):
            print("next")
            game_progress = game_progress+1
            shuttlerun_next(client, userdata, msg)
        if(started == 1):
            print("init")
            started = 0
            shuttlerun_init(client, userdata, msg)
    print("knop 6")
#endregion

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
#region **** colorconvert ****
def colorconvert(value):
    temp = value.replace("#", "")
    temp = "0x" + temp
    return temp
#endregion

#region **** game logic steps ****
def speedrun_next(client, userdata, msg):
    global started, publish, power_off, btn_choiche1, game_bezig, aantal_knoppen, game_progress, name1, tijd_start, speedrun_init, btn_choiche2, tijd_cooldown, tijd_cooldown_start, degree
    print('verwerken:', str(msg.payload.decode('utf-8')))
    if(speedrun_init == 1):
        game_progress = game_progress+1
        speedrun_init = 0
    if(game_bezig ==1):
        #print('test succes')
        if(game_progress == 0):
            print("unix_timestamp => ",(time.mktime(tijd_start.timetuple())))
            socketio.emit("Start",time.mktime(tijd_start.timetuple()))
        publish = 1
        temp = random.randint(1,6)
        while(temp == btn_choiche1 or temp == btn_choiche2):
            temp = random.randint(1,6)
        btn_choiche1 = temp
        print(btn_choiche1)
        data = {"Username": name1, "GameMode": "Speedrun", "ButtonsRemaining": aantal_knoppen-game_progress}
        y = json.dumps(data)
        socketio.emit('B2F_new_data_speedrun',y)
        tijd_cooldown_start = datetime.now()
        if(degree == '2'):
            tijd_cooldown = datetime.now()+timedelta(seconds=12)
        elif(degree == '3'):
            tijd_cooldown = datetime.now()+timedelta(seconds=7)
        else:
            tijd_cooldown = datetime.now()+timedelta(seconds=16)
        #timedelta moet afhankelijk worden van difficulty en moet in if komen of het zeker moeilijker is dan difficulty 1
        #print("verzonden")
        btn_choiche2 = 0
        #als het 2 keer dezelfde word regel hierboven verwijderen :)
        print(data)
        print(y)
    elif(game_bezig == 0):
        power_off = 1
        game_bezig = 1
def multiplayer_init(client,userdate, msg):
    print('verwerken:', str(msg.payload.decode('utf-8')))
    global timerstart,started, publish, power_off, btn_choiche1, game_bezig, aantal_knoppen, game_progress, name1, btn_choiche2, score1, score1_oud, score2, score2_oud,tijd_start,tijd_set,tijd_end,tijd
    tijd_start = datetime.now()
    tijd_end = tijd_start + timedelta(seconds=int(tijd_set))
    timerstart = 1
    print('timergestart')
    print(tijd_start)
    print(tijd_end)
    if(game_bezig ==1):
        print('big successsss')
        #print('test succes')
        publish = 1
        ##voor de initial one moeje ze 1 keer alle 2 analeggen en dan de rest laten verlopen via dit
        temp = random.randint(1,6)
        while(temp == btn_choiche1):
            temp = random.randint(1,6)
        btn_choiche1 = temp
        print(btn_choiche1)
        temp = random.randint(1,6)
        while(temp==btn_choiche1 or temp == btn_choiche2):
            temp = random.randint(1,6)
        btn_choiche2= temp
    data = {"Username1": name1, "GameMode": "Speedrun", "Username2":name2,"Score1":score1, "Score2":score2}
    y = json.dumps(data)
    socketio.emit('B2F_new_data_1vs1',y)
    print("unix_timestamp => ",(time.mktime(tijd_start.timetuple())))
    socketio.emit("Start",time.mktime(tijd_start.timetuple()))
    
def multiplayer_next(client, userdata, msg):
    global started, publish, power_off, btn_choiche1, game_bezig, aantal_knoppen, game_progress, name1, btn_choiche2, score1, score1_oud, score2, score2_oud
    print('verwerken:', str(msg.payload.decode('utf-8')))
    if(game_bezig ==1):
        publish = 1
        ##voor de initial one moeje ze 1 keer alle 2 analeggen en dan de rest laten verlopen via dit
        if(score1_oud != score1):
            temp = random.randint(1,6)
            while(temp == btn_choiche1 or temp == btn_choiche2):
                temp = random.randint(1,6)
            btn_choiche1 = temp
            print(btn_choiche1)
        elif(score2_oud != score2):
            temp = random.randint(1,6)
            while(temp==btn_choiche1 or temp == btn_choiche2):
                temp = random.randint(1,6)
            btn_choiche2= temp
        data = {"Username1": name1, "GameMode": "Speedrun", "Username2":name2,"Score1":score1, "Score2":score2}
        y = json.dumps(data)
        socketio.emit('B2F_new_data_1vs1',y)
        #print("verzonden")
        #print(data)
        #print(y)
    elif(game_bezig == 0):
        power_off = 1
        game_bezig = 1
def shuttlerun_init(client,userdate, msg):
    global timerstart,started, publish, power_off, btn_choiche1, game_bezig, aantal_knoppen, game_progress, name1, btn_choiche2, score1, score1_oud, score2, score2_oud,tijd_start,tijd_set,tijd_end,tijd
    game_progress = 0
    tijd_start = datetime.now()
    tijd_end = tijd_start + timedelta(seconds=int(tijd_set))
    temp = random.randint(1,6)
    while(temp == btn_choiche1):
        temp = random.randint(1,6)
    btn_choiche1 = temp
    print(btn_choiche1)
    score1 = score1 + 1
    publish = 1
    timerstart = 1
    data = {"Username": name1, "GameMode": "Shuttlerun","Score":score1}
    y = json.dumps(data)
    socketio.emit('B2F_new_data_shuttle_run',y)
    print("unix_timestamp => ",(time.mktime(tijd_start.timetuple())))
    socketio.emit("Start",time.mktime(tijd_start.timetuple()))

def shuttlerun_next(client,userdate, msg):
    global timerstart,started, publish, power_off, btn_choiche1, game_bezig, aantal_knoppen, game_progress, name1, btn_choiche2, score1, score1_oud, score2, score2_oud,tijd_start,tijd_set,tijd_end,tijd, degree
    tijd_start_run = datetime.now()
    score1 = score1 + 1
    if(degree == '1'):
        tijd_set= tijd_set*0.98
    elif(degree == '2'):
        tijd_set= tijd_set*0.97
    elif(degree == '3'):
        tijd_set= tijd_set*0.96
    tijd_end = tijd_start_run + timedelta(seconds=int(tijd_set))
    print(tijd_set)
    temp = random.randint(1,6)
    while(temp == btn_choiche1):
        temp = random.randint(1,6)
    btn_choiche1 = temp
    print(btn_choiche1)
    publish = 1
    data = {"Username": name1, "GameMode": "ShuttleRun","Score":score1}
    y = json.dumps(data)
    socketio.emit('B2F_new_data_shuttle_run',y)


#endregion
#region **** INIT ****
# Start app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheim!'
socketio = SocketIO(app, cors_allowed_origins="*", logger=False, engineio_logger=False, ping_timeout=1)
CORS(app)

#endregion
#region **** DATABASE ****

def add_speedrun(spelNaam, spelers, tijd, naam1, aantalPalen, winnaar, moeilijkheidsgraad):
    sql = "insert into spel (spelNaam, spelers, tijd, naam1, aantalPalen, winnaar, moeilijkheidsgraad) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    params = [spelNaam, spelers, tijd, naam1, aantalPalen, winnaar, moeilijkheidsgraad]
    result = Database.execute_sql(sql, params)
    return result

def add_multiplayer(spelNaam, spelers, tijd, naam1, naam2, winnaar, moeilijkheidsgraad):
    sql = "insert into spel (spelNaam, spelers, tijd, naam1, naam2, winnaar, score) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    params = [spelNaam, spelers, tijd, naam1, naam2, winnaar, moeilijkheidsgraad]
    result = Database.execute_sql(sql, params)
    return result

def add_shuttlerun(spelNaam, spelers, naam1, winnaar,score, moeilijkheidsgraad, tijd):
    sql = "insert into spel (spelNaam, spelers, naam1, winnaar, score, moeilijkheidsgraad, tijd) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    params = [spelNaam, spelers, naam1, winnaar, score, moeilijkheidsgraad,tijd]
    result = Database.execute_sql(sql, params)
    return result
#endregion
#region **** ROUTES ****
@app.route('/')
def hallo():
    print('start')
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."


@app.route(endpoint + '/1vs1/<time>/', methods=['GET'])
def OneVsOne(time):
    if request.method == 'GET':
        print('1vs1 database ophalen')
        data = DataRepository.read_1vs1_data_by_time(time)
        return jsonify(data), 200

@app.route(endpoint + '/speedrun/<difficulty>/<buttons>/', methods=['GET'])
def Speedrun(difficulty, buttons):
    if request.method == 'GET':
        print(difficulty)
        print(buttons)
        data = DataRepository.read_speedrun_data_by_difficulty_and_buttons(difficulty, buttons)
        return jsonify(data), 200

@app.route(endpoint + '/shuttle_run/<difficulty>/', methods=['GET'])
def ShuttleRun(difficulty):
    if request.method == 'GET':
        print(difficulty)
        data = DataRepository.read_shuttlerun_data_by_difficulty(difficulty)
        return jsonify(data), 200

@app.route(endpoint + '/simon_says/<difficulty>/<startbuttons>/', methods=['GET'])
def Simonsays(difficulty, startbuttons):
    if request.method == 'GET':
        print(difficulty)
        print(startbuttons)
        data = DataRepository.read_simonsays_data_by_difficulty_and_start_buttons(difficulty, startbuttons)
        return jsonify(data), 200

#endregion




# SOCKET.IO EVENTS
@socketio.on('connect')
def initial_connection():
    print('A new client connect')
@socketio.on('getLiveGameData')
def PageReload():
    global game_bezig, aantal_knoppen, game_progress, name1, name2, color1, color2, selected_gamemode, score1, score2, started, tijd_start, tijd, timerstart, selected_gamemode_old
    print('getLiveGameData')
    if(selected_gamemode == 1):
        data = {"Username": name1, "GameMode": "Speedrun", "ButtonsRemaining": aantal_knoppen-game_progress}
        y = json.dumps(data)
        socketio.emit('B2F_new_data_speedrun',y)
        print("verzonden")
        print(data)
        print(y)
        socketio.emit('Start',time.mktime(tijd_start.timetuple()))
        if(btn_choiche2 != 0):
            socketio.emit('knop_aan', {'knop1': btn_choiche2, 'knop2':0})
        else:
            socketio.emit('knop_aan', {'knop1': btn_choiche1, 'knop2':0})
    elif(selected_gamemode == 2):
        print('socketio tis met 1v1 te doen')
        data = {"Username1": name1, "GameMode": "OnevsOne", "Username2":name2,"Score1":score1, "Score2":score2}
        y = json.dumps(data)
        socketio.emit('B2F_new_data_1vs1',y)
        if(timerstart == 1):
            #print("unix_timestamp => ",(time.mktime(tijd_start.timetuple())))
            data = {"Username1": name1, "GameMode": "OnevsOne", "Username2":name2,"Score1":score1, "Score2":score2}
            y = json.dumps(data)
            socketio.emit('B2F_new_data_1vs1',y)
            socketio.emit("Start",time.mktime(tijd_start.timetuple()))
            socketio.emit('knop_aan', {'knop1': btn_choiche1, 'knop2':btn_choiche2})
    elif(selected_gamemode == 3):
        print("socketio tis met shuttle te doen")
        data = {"Username": name1, "GameMode": "ShuttleRun","Score":score1}
        y = json.dumps(data)
        socketio.emit('B2F_new_data_shuttle_run',y)
        socketio.emit('knop_aan', {'knop1': btn_choiche1, 'knop2':0})
        if(timerstart == 1):
            data = {"Username": name1, "GameMode": "ShuttleRun","Score":score1}
            y = json.dumps(data)
            socketio.emit('B2F_new_data_shuttle_run',y)
            socketio.emit("Start",time.mktime(tijd_start.timetuple()))
            socketio.emit('knop_aan', {'knop1': btn_choiche1, 'knop2':0})
    elif(selected_gamemode == 0 and selected_gamemode_old == 1):
        data = {"Username": name1, "GameMode": "Speedrun", "ButtonsRemaining": aantal_knoppen-game_progress, "Tijd": tijd}
        y = json.dumps(data)
        socketio.emit('Reload',y)
        socketio.emit('knop_aan', {'knop1': 0, 'knop2':0})
    elif(selected_gamemode == 0 and selected_gamemode_old == 2):
        data = {"Username1": name1, "GameMode": "OnevsOne", "Username2":name2,"Score1":score1, "Score2":score2, "Tijd": tijd}
        y = json.dumps(data)
        socketio.emit('Reload',y)
        socketio.emit('knop_aan', {'knop1': 0, 'knop2':0})
    elif(selected_gamemode == 0 and selected_gamemode_old == 3):
        data = {"Username": name1, "GameMode": "ShuttleRun","Score":score1, "Tijd": tijd}
        y = json.dumps(data)
        socketio.emit('Reload',y)
        socketio.emit('knop_aan', {'knop1': 0, 'knop2':0})
@socketio.on('1vs1')
def newOneVsOne(testvariabl):
    global name1,publish, name2,btn_choiche1, btn_choiche2, color1,color2, degree, buttonGoal,minutes,game_bezig,aantal_knoppen,color_choiche,game_progress,started,tijd_set,selected_gamemode,score1,score2,timerstart, tijd_start, tijd_end
    print('1vs1', testvariabl)
    color1 = testvariabl["color1"]
    color2 = testvariabl["color2"]
    name1 = testvariabl["name1"]
    name2 = testvariabl["name2"]
    minutes = testvariabl["minutes"]
    tijd_set = int(minutes)*60
    ###tijd is hardcoded op 30 sec
    ####ding hierboven is het juiste
    #tijd_set = 30
    selected_gamemode = 2
    timerstart = 0
    game_bezig = 1
    started=1
    score1=0
    score2=0
    print('1vs1 aangemaakt')
    time.sleep(4)
    tijd_start = datetime.now()
    tijd_end = tijd_start + timedelta(seconds=int(tijd_set))
    timerstart = 1
    print('timergestart')
    print(tijd_start)
    print(tijd_end)
    if(game_bezig ==1):
        print('big successsss')
        #print('test succes')
        publish = 1
        ##voor de initial one moeje ze 1 keer alle 2 analeggen en dan de rest laten verlopen via dit
        temp = random.randint(1,6)
        while(temp == btn_choiche1):
            temp = random.randint(1,6)
        btn_choiche1 = temp
        print(btn_choiche1)
        temp = random.randint(1,6)
        while(temp==btn_choiche1 or temp == btn_choiche2):
            temp = random.randint(1,6)
        btn_choiche2= temp
    data = {"Username1": name1, "GameMode": "Speedrun", "Username2":name2,"Score1":score1, "Score2":score2}
    y = json.dumps(data)
    socketio.emit('B2F_new_data_1vs1',y)
    print("unix_timestamp => ",(time.mktime(tijd_start.timetuple())))
    socketio.emit("Start",time.mktime(tijd_start.timetuple()))
    started = 0
    #y = json.dumps(testvariabl)

#difficulty is datie na x sec nie drukt vanzelf naar volgende gaat ma dan zonder punt te geven.
@socketio.on('Speedrun')
def newSpeedrun(testvariabl):
    global game_bezig,tijd_cooldown, tijd_cooldown_start, aantal_knoppen,btn_choiche1, color_choiche, game_progress, started, name1, name2, color1, degree, buttonGoal, tijd_start, selected_gamemode, publish, btn_choiche2, speedrun_init
    print('Speedrun', testvariabl)
    #y = json.dumps(testvariabl)
    aantal_knoppen = int(testvariabl["buttonGoal"])
    buttonGoal = int(testvariabl["buttonGoal"])
    name1 = testvariabl["name1"]
    color1 = testvariabl["color1"]
    degree = testvariabl["degree"]
    tijd_start = datetime.now()
    color_choiche=colorconvert(color1)
    game_bezig = 1
    selected_gamemode = 1
    started = 1
    game_progress = 0
    if(degree == '2'):
        tijd_cooldown = datetime.now()+timedelta(seconds=12)
    elif(degree == '3'):
        tijd_cooldown = datetime.now()+timedelta(seconds=7)
    else:
        tijd_cooldown = datetime.now()+timedelta(seconds=16)
    #hieredit
    #ook hier nog seconds afhankelijk van difficulty
    time.sleep(4)
    temp = random.randint(1,6)
    while(temp==btn_choiche1 or temp == btn_choiche2):
        temp = random.randint(1,6)
    btn_choiche2= temp
    speedrun_init = 1
    publish = 1
    tijd_start = datetime.now()
    

@socketio.on('ShuttleRun')
def newSpeedrun(testvariabl):
    global game_bezig, aantal_knoppen, color_choiche, game_progress, started, name1, name2, color1, degree, buttonGoal, tijd_start, selected_gamemode,tijd_set, score1, timerstart,started, publish, power_off, btn_choiche1, game_bezig, aantal_knoppen, game_progress, name1, btn_choiche2, score1, score1_oud, score2, score2_oud,tijd_start,tijd_set,tijd_end,tijd
    print('Shuttlerun', testvariabl)
    name1 = testvariabl["name1"]
    color1 = testvariabl["color1"]
    degree = testvariabl["degree"]
    color_choiche=colorconvert(color1)
    #tijd set moet afafhankelijk zijn van de degree maar idk :)
    tijd_set = 30
    game_bezig = 1
    selected_gamemode = 3
    started = 1
    score1 = 0
    game_progress = 0
    time.sleep(4)
    game_progress = 0
    tijd_start = datetime.now()
    tijd_end = tijd_start + timedelta(seconds=int(tijd_set))
    temp = random.randint(1,6)
    while(temp == btn_choiche1):
        temp = random.randint(1,6)
    btn_choiche1 = temp
    print(btn_choiche1)
    publish = 1
    timerstart = 1
    data = {"Username": name1, "GameMode": "ShuttleRun","Score":score1}
    y = json.dumps(data)
    socketio.emit('B2F_new_data_shuttle_run',y)
    print("unix_timestamp => ",(time.mktime(tijd_start.timetuple())))
    socketio.emit("Start",time.mktime(tijd_start.timetuple()))
    print('Shuttlerun aangemaakt')

def mqttrun():
    global timerstart,selected_gamemode_old,tijd_cooldown, tijd_cooldown_start, speedrun_init, started, publish, power_off, btn_choiche1,btn_choiche2, game_bezig, aantal_knoppen, game_progress, color_choiche, tijd, tijd_start, name1, name2, color1,color2, degree, buttonGoal,selected_gamemode, tijd_end, tijd_set
    client = mqtt.Client("rpi_client2") #this name should be unique
    client.on_publish = on_publish
    flag_connected = 0
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.message_callback_add('esp32/sensor5', callback_esp32_sensor5)
    client.message_callback_add('esp32/sensor4', callback_esp32_sensor4)
    client.message_callback_add('esp32/sensor6', callback_esp32_sensor6)
    client.message_callback_add('esp32/sensor3', callback_esp32_sensor3)
    client.message_callback_add('esp32/sensor2', callback_esp32_sensor2)
    client.message_callback_add('esp32/sensor1', callback_esp32_sensor1)
    client.message_callback_add('rpi/broadcast', callback_rpi_broadcast)
    #client.message_callback_add('esp32/kleur5', callback_rpi_esp5)
    client.connect('127.0.0.1',1883)
    client.loop_start()
    client_subscriptions(client)
    print("......client setup complete............")
    # start a new thread
    client.loop_start()
    while True:
        try:
            if(power_off == 1):
                print("enter")
                msg ='led_uit'
                pubMsg = client.publish(
                    topic='rpi/broadcast',
                    payload=msg.encode('utf-8'),
                    qos=0,
                    )
                pubMsg.wait_for_publish()
                print("game end - alles uit")
                socketio.emit('Stop')
                if(selected_gamemode==1):
                    tijd = datetime.now() - tijd_start
                    tijd = round(tijd.total_seconds())
                    add_speedrun("Speedrun",1,tijd,name1,buttonGoal,name1,degree)
                    selected_gamemode_old=selected_gamemode
                    selected_gamemode=0
                if(selected_gamemode==2):
                    if(score1>score2):
                        winnaar = name1
                        score=score1
                    elif(score2>score1):
                        winnaar = name2
                        score=score2
                    else:
                        winnaar = "gelijkspel"
                        score=score1
                    add_multiplayer("1VS1",2,tijd_set,name1,name2,winnaar,score)
                    tijd = datetime.now() - tijd_start
                    tijd = round(tijd.total_seconds())
                    selected_gamemode_old=selected_gamemode
                    selected_gamemode=0
                if(selected_gamemode==3):
                    tijd = datetime.now() - tijd_start
                    tijd = round(tijd.total_seconds())
                    print(tijd)
                    add_shuttlerun("Shuttle Run",1,name1,name1,score1,degree,tijd)
                    selected_gamemode_old=selected_gamemode
                    selected_gamemode=0
                socketio.emit('knop_aan', {'knop1': 0, 'knop2':0})
                for i in range(0, 7):
                    msg ="0x00ff00"
                    pubMsg = client.publish(
                        topic=f'esp32/kleur{i}',
                        payload=msg.encode('utf-8'),
                        qos=0,
                    )
                    pubMsg.wait_for_publish()
                time.sleep(2)
                for i in range(0, 7):
                    msg =""
                    pubMsg = client.publish(
                        topic=f'esp32/kleur{i}',
                        payload=msg.encode('utf-8'),
                        qos=0,
                    )
                    pubMsg.wait_for_publish()
                power_off = 0
                selected_gamemode = 0
            if(publish == 1 and selected_gamemode==1):
                if(speedrun_init == 1):
                    msg ='led_uit'
                    pubMsg = client.publish(
                        topic='rpi/broadcast',
                        payload=msg.encode('utf-8'),
                        qos=0,
                    )
                    pubMsg.wait_for_publish()
                    #print("succes")
                    msg =color_choiche
                    pubMsg = client.publish(
                        topic=f'esp32/kleur{btn_choiche2}',
                        payload=msg.encode('utf-8'),
                        qos=0,
                    )
                    pubMsg.wait_for_publish()
                    print("succes2")
                    socketio.emit('knop_aan', {'knop1': btn_choiche2, 'knop2':0})
                else:
                    print("enter")
                    msg ='led_uit'
                    pubMsg = client.publish(
                        topic='rpi/broadcast',
                        payload=msg.encode('utf-8'),
                        qos=0,
                        )
                    pubMsg.wait_for_publish()
                    #print("succes")
                    msg =color_choiche
                    pubMsg = client.publish(
                        topic=f'esp32/kleur{btn_choiche1}',
                        payload=msg.encode('utf-8'),
                        qos=0,
                        )
                    pubMsg.wait_for_publish()
                    print("succes2")
                    socketio.emit('knop_aan', {'knop1': btn_choiche1, 'knop2':0})
                    game_progress = game_progress+1
                if(aantal_knoppen==game_progress):
                    game_bezig=0
                    game_progress=0
                    aantal_knoppen = 0
                    color_choiche = ""
                publish = 0
                #btn_choiche = 0
            if(publish==1 and selected_gamemode==2):
                print('1v1 dingen doen')
                print(color1)
                print(color2)
                numbers = [1,2,3,4,5,6]
                temp = [btn_choiche1,btn_choiche2]
                for i  in numbers:
                    #print(i)
                    if(i not in temp):
                        #print(i)
                        msg =""
                        pubMsg = client.publish(
                            topic=f'esp32/kleur{i}',
                            payload=msg.encode('utf-8'),
                            qos=0,
                            )
                        pubMsg.wait_for_publish()
                msg =colorconvert(color1)
                pubMsg = client.publish(
                    topic=f'esp32/kleur{btn_choiche1}',
                    payload=msg.encode('utf-8'),
                    qos=0,
                    )
                pubMsg.wait_for_publish()
                msg =colorconvert(color2)
                pubMsg = client.publish(
                    topic=f'esp32/kleur{btn_choiche2}',
                    payload=msg.encode('utf-8'),
                    qos=0,
                    )
                pubMsg.wait_for_publish()
                print("succes3")
                
                socketio.emit('knop_aan', {'knop1': btn_choiche1, 'knop2':btn_choiche2})
                publish=0
            
            if(publish == 1 and selected_gamemode==3):
                print("enter")
                msg ='led_uit'
                pubMsg = client.publish(
                    topic='rpi/broadcast',
                    payload=msg.encode('utf-8'),
                    qos=0,
                    )
                pubMsg.wait_for_publish()
                #print("succes")
                msg =color_choiche
                pubMsg = client.publish(
                    topic=f'esp32/kleur{btn_choiche1}',
                    payload=msg.encode('utf-8'),
                    qos=0,
                    )
                pubMsg.wait_for_publish()
                print("succes2")
                socketio.emit('knop_aan', {'knop1': btn_choiche1, 'knop2':0})
                publish = 0
                #btn_choiche = 0
            #hier tijdstart + ingestelde tijd (in seconden fzo erbij tellen)
            if( datetime.now()>tijd_end and selected_gamemode==2 and timerstart==1):
                print("game gedaan game gedaan")
                power_off = 1
                timerstart=0
            if(datetime.now()>tijd_end and selected_gamemode==3 and timerstart==1):
                print("game gedaan game gedaan")
                power_off = 1
                timerstart=0
            if(datetime.now()>tijd_cooldown and selected_gamemode==1 and degree != '1'):
                if(degree == '2'):
                    tijd_cooldown = datetime.now()+timedelta(seconds=12)
                elif(degree == '3'):
                    tijd_cooldown = datetime.now()+timedelta(seconds=7)
                else:
                    tijd_cooldown = datetime.now()+timedelta(seconds=16)
                temp = random.randint(1,6)
                while(temp==btn_choiche1 or temp == btn_choiche2):
                    temp = random.randint(1,6)
                btn_choiche2= temp
                btn_choiche1 = temp
                game_progress = game_progress-1
                speedrun_init= 1
                publish = 1
                print("te lang gewacht")
        
        except Exception as e:
            print(e)
# START THE APP
if __name__ == '__main__':
    try:
        print("in de try")
        print("\n\n1VS1 data:")
        print(DataRepository.read_1vs1_data_by_time(300))
        print("\n\nspeedrun data:")
        print(DataRepository.read_speedrun_data_by_difficulty_and_buttons(1,5))
        print("\n\nSimon says data:")
        print(DataRepository.read_simonsays_data_by_difficulty_and_start_buttons(1,5))
        print("\n\nShuttle run data:")
        print(DataRepository.read_shuttlerun_data_by_difficulty(2))
        thread = threading.Thread(target=mqttrun, args=(), daemon=True)
        thread.start()
        print("thread gestart")
        print("backend running")
        socketio.run(app, debug=False, host='0.0.0.0')
    except KeyboardInterrupt:
        print('KeyboardInterrupt exception is caught')