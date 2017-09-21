import paho.mqtt.client as mqtt
import time
import sys
import subprocess

MQTT_USERNAME  = "fa6c6990-12bc-11e7-9088-a1111bb51eb7"
MQTT_PASSWORD  = "341461ce22c41cbac607346fc16c1620d85fb8df"
MQTT_CLIENT_ID = "af425330-12cb-11e7-8a12-9ba5897beb06"

mqttc = mqtt.Client(client_id=MQTT_CLIENT_ID)
mqttc.username_pw_set(MQTT_USERNAME, password=MQTT_PASSWORD)
mqttc.connect("mqtt.mydevices.com", port=1883, keepalive=60)

topic_temp = "v1/"+MQTT_USERNAME+"/things/"+MQTT_CLIENT_ID+"/data/100"  #change username/clientid here without quotes
topic_humidity = "v1/"+MQTT_USERNAME+"/things/"+MQTT_CLIENT_ID+"/data/101"
topic_airpress = "v1/"+MQTT_USERNAME+"username/things/"+MQTT_CLIENT_ID+"/data/102"
i=0;
while True:
    try: 
        #temp = subprocess.Popen(['mosquitto_sub', '-t', '/tinkerforge/bricklet/temperature/t6Q/temperature', stdout=subprocess.PIPE)
        #humidity= subprocess.Popen(['mosquitto_sub', '-t', '/tinkerforge/bricklet/humidity/uk9/humidity', stdout=subprocess.PIPE)
        #airpress= subprocess.Popen(['mosquitto_sub', '-t', '/tinkerforge/bricklet/barometer/vGZ/air_pressure', stdout=subprocess.PIPE)
	temp = i
	humidity = (i*10) % 100
	airpress = i*3
	i = i+1
        if temp is not None:
                temp = "temp,c=" + str(int(temp))
                mqttc.publish(topic_temp, payload= temp , retain=True)	

        if humidity is not None:
                humidity = "humidity,%=" + str(int(humidity))
                mqttc.publish(topic_humidity, payload= humidity , retain=True)

        if airpress is not None:
                airpress = "airpress,hPa=" + str(int(airpress))
                mqttc.publish(topic_airpress, payload= airpress , retain=True)

        time.sleep(5)
    except (EOFError, SystemExit, KeyboardInterrupt):
        mqttc.disconnect()
        sys.exit()


