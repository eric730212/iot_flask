from flask import Flask, request, jsonify, render_template
from flask_mqtt import Mqtt
import sqlite3
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)

app.config['MQTT_BROKER_URL'] = '192.168.0.123'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = 'god01'  # Set this item when you need to verify username and password
app.config['MQTT_PASSWORD'] = '0101xx'  # Set this item when you need to verify username and password
app.config['MQTT_KEEPALIVE'] = 5  # Set KeepAlive time in seconds
app.config['MQTT_TLS_ENABLED'] = False  # If your broker supports TLS, set it True
topic = '/flask/mqtt'

mqtt_client = Mqtt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Connected successfully')
        mqtt_client.subscribe(topic)  # subscribe topic
    else:
        print('Bad connection. Code:', rc)


@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    print('Received message on topic: {topic} with payload: {payload}'.format(**data))
    print("***" * 30)
    msg = str(message.payload.decode())
    iot = msg.split(':')[1].split(',')[0]
    temperature = msg.split(':')[2].split(',')[0]
    humidity = msg.split(':')[3].split(',')[0]
    lux = msg.split(':')[4].split(',')[0]
    tvoc = msg.split(':')[5].split(',')[0]
    co2 = msg.split(':')[6].split(',')[0]
    pm25 = msg.split(':')[7].split(',')[0].split('\n')[0]
    # timenow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('temperature = ', temperature)
    print('humidity = ', humidity)
    print('lux = ', lux)
    print('tvoc = ', tvoc)
    print('co2 = ', co2)
    print('pm25 = ', pm25)
    conn = sqlite3.connect('iots.sqlite3')
    c = conn.cursor()
    c.execute("INSERT INTO iots (iot, temperature, humidity, lux, tvoc, co2, pm25, time) VALUES (%s,%s,%s,%s,%s,%s,%s,datetime('now','localtime'))"%(iot, temperature, humidity, lux, tvoc, co2, pm25))
    conn.commit()
    conn.close()

@app.route('/publish', methods=['POST'])
def publish_message():
    request_data = request.get_json()
    publish_result = mqtt_client.publish(request_data['topic'], request_data['msg'])
    return jsonify({'code': publish_result[0]})


@app.route('/')
def root():
    # return render_template("page.html")
    conn1 = sqlite3.connect('iots.sqlite3')
    c = conn1.cursor()
    c.execute(
        "SELECT iot,temperature,humidity,lux,tvoc,co2,pm25,time FROM iots ORDER by time DESC")
    arr = c.fetchone()
    iot_test = arr[0]
    temperature_test = arr[1]
    humidity_test = arr[2]
    lux_test = arr[3]
    tvoc_test = arr[4]
    co2_test = arr[5]
    pm25_test = arr[6]
    time_test = arr[7]
    conn1.commit()
    conn1.close()

    appInfo = {  # dict
        'iot': iot_test,
        'temperature': temperature_test,
        'humidity': humidity_test,
        'lux': lux_test,
        'tvoc': tvoc_test,
        'co2': co2_test,
        'pm25': pm25_test,
        'time': time_test
    }

    # conn1.commit()
    # conn1.close()

    return render_template('test.html', appInfo=appInfo)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
