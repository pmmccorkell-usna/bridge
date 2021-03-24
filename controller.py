#24 March 2021
#US Naval Academy, Robotics and Control TSD
#Patrick McCorkell

from machine import Pin,ADC
from time import sleep
from utime import ticks_us, ticks_diff
from stats import stdev, mean
from ujson import dumps
from gc import collect as trash
import mqttClass

DEBUG=1

# server = '192.168.5.4'
server = '10.60.5.238'
client = mqttClass.mqttClass(server)

# ADC pin attenuation setting:
	#ATTN_0DB	0	1.00 volt
	#ATTN_2_5DB	1	1.34 volt
	#ATTN_6DB	2	2.00 volt
	#ATTN_11DB	3	3.60 volt
attenuation = 3

left_stick = ADC(Pin(34))
right_stick = ADC(Pin(35))

stall_time = 0.001

values = {
}
commands = {
	'left_stick':left_stick.read,
	'right_stick':right_stick.read
}

def poll_cmds():
	global values, commands
	for key in commands:
		values[key] = commands[key]()
	
poll_cmds()

def sample(samples=500,smooth_samples=49):
	t0=ticks_us()
	global left_stick_samples, right_stick_samples
	left_stick_samples=[]
	right_stick_samples=[]

	left_stick_smooth=[]
	right_stick_smooth=[]

	for i in range(samples):
		poll_cmds()

		left_stick_samples.append(values['left_stick'])
		right_stick_samples.append(values['right_stick'])

		if (j==smooth_samples):
			left_stick_smooth.append(mean(left_stick_samples[(i-smooth_samples):(i+1)]))
			right_stick_smooth.append(mean(right_stick_samples[(i-smooth_samples):(i+1)]))
			j=0
		i+=1
		j+=1

	data = {
		'left_stick' : mean(left_stick_smooth)
		'right_stick' : mean(right_stick_smooth)
	}

	if (DEBUG==1):
		t1=ticks_us()
		print(ticks_diff(t1,t0))

	return data

def process():
	stick_data = sample()
	message = {
		'leftJS' : stick_data['left_stick'],
		'rightJS' : stick_data['right_stick']
	}

	topic = 'TestBoat/controller'