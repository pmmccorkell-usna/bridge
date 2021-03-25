from time import sleep
import paho.mqtt.client as MQTT
import logging
import logging.handlers
from datetime import datetime
from gc import collect as trash
import json
import os
from server import *
from random import randint
from statistics import mean

#					   #
#-----Logging Setup-----#
#					   #
filename=default_directory + datetime.now().strftime('qtm_mqtt_%Y%m%d_%H:%M:%s.log')
log = logging.getLogger()
log.setLevel(logging.INFO)
format = logging.Formatter('%(asctime)s, %(message)s')
file_handler = logging.FileHandler(filename)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(format)
log.addHandler(file_handler)

#					   #
#-------MQTT Setup-----#
#					   #
name = clientname + str(randint(1000,9999))
client=MQTT.Client(name)


# basic callback for MQTT that prints message data directly.
def print_message(client,userdata,message):
	data={}
	print()
	print('mqtt rx:')
	print(message.topic)
#	print(message.qos)
#	print(message.payload)
	data=json.loads(message.payload.decode())
	print(data)
	print(data["h"])
#	print(message.payload.)
#	print(message.retain)
	print(client)

# Dictionary and Function to store remote control readings.
voltages = {
	'leftJS' : [],
	'rightJS' : []
}
def gather_V(message):
	global voltages
	buffer = json.loads(data.payload.decode())
	for key in voltages:
		voltages[key].append(buffer[key])


# A basic callback for MQTT that stores message data to a log file.
def log_message(message):
	# log.info('message rx')
	# log.info(str(message.topic)+', '+str(message.payload))
	# buffer = {}
	buffer = json.loads(data.payload.decode())
	data['h'] = buffer['h']
	for key in voltages:
		data[key] = mean(voltages[key])
		voltages[key]=[]
	#log.info(data["h"])
	log.info(json.dumps(data))

# Redirect from MQTT callback function.
# Error checking.
def defaultFunction(message):
	print("PYTHON >> Discarding. No filter for topic "+str(message.topic)+" discovered.")

topic_outsouring = {
	'TestBoat/controller' : gather_V,
	'TestBoat/orientation' : log_message,
	'default':defaultFunction
}
def topic_callback(client,userdata,message):
	################# EXAMPLE START ##################
	# print(message.payload.decode())
	# print(message.topic)
	# msg=message.payload.decode().lower()
	# if (msg.topic == 'OptiTrack/Control/AddObject'):
		# AddObject(message)
	################# EXAMPLE END ####################
	
	# Get the function associated to the MQTT topic.
	# load the defaultFunction if an associated topic is not found.
	topicFunction=topic_outsourcing.get(message.topic,defaultFunction)
	
	# Execute the function associated to the MQTT topic, 
	# passing the MQTT message.
	topicFunction(message)


# The callback that our program will use to control device.
def process(client,userdata,message):
	#
	# Code to use the mqtt data.
	#
	a = 1

def check_quit():
	return 1

def setup_subscription():
	check=0
	try:
		# Connect to the server (defined by server.py)
		client.connect(server)

		# Assigns the callback function when a mqtt message is received.
		if (DEBUGGING):
			client.on_message=print_message
			#client.on_message=log_message
		else:
			client.on_message=log_message

		# Subscribes to all the topics defined at top.
		for i in topiclist:
			client.subscribe(i+'/'+'#')

		# Start the mqtt subscription.
		client.loop_start()
		log.info('mqtt subscription script started')
		check=1
	except:
		print("didn't connect")
		log.info('mqtt subscription failed')
	return check

def main():
	q=0
	# Run the MQTT setup once.
	q=setup_subscription()

	# Because the subscription works on interrupt callbacks, nothing happens in main.
	while(q):
		trash()
		sleep(1)
		q=check_quit()

main()




