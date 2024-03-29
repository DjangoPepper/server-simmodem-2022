#!/usr/bin/env python
# -*- coding:utf-8 -*-

from src.sim_audio import *
from src.sim_sql import *
from src.sim_modem import *
from src.sim_hardaware import *
import time

modem = Modem('/dev/ttyS0', baudrate=115200, timeout=2, at_cmd_delay=0.5, debug=False,)

FLAG_ONLINE = False

global FLAG_CAN_RECORD 
FLAG_CAN_RECORD = False

FLAG_OFFLINE = True
FLAG_CONNECTED = False
global FLAG_RECORDED 
FLAG_RECORDED = False
FLAG_CALLCOUNTDOWN = False

global APPELANT_SRV
APPELANT_SRV = 1111

global USER_ID
USER_ID = 1

global DTMF_SONG
DTMF_SONG = ""


PIN_NUMBER = "0000"

TELM = "0664018952"
TELB = "0800943376"
TEL = TELB


def CallCountDown(t):
	# define the countdown func.
	
	while t:
		mins, secs = divmod(t, 60)
		timer = '{:02d}:{:02d}'.format(mins, secs)
		print(timer, end="\r")
		time.sleep(1)
		t -= 1

def transcibeurre():
	#  vosk-transcriber -i stem_record.wav -o text_stem_record.txt -n vosk-model-fr-0.22
	 pass

def MacAndCheese(_USER_ID, _APPELANT_SRV,_DTMF_SONG):
	print("user id : ", _USER_ID)
	
	# CallCountDown(1)
	FLAG_CAN_RECORD = modem.send_dtmf_code(_DTMF_SONG)
	print("DTMF SEND")

	# CallCountDown(1)
	if FLAG_CAN_RECORD == True and FLAG_RECORDED == False:
		myaudio.recordheure(_APPELANT_SRV)
		print ("AUDIO DONE")
		FLAG_RECORDED = True
		FLAG_CAN_RECORD = False


def main_initmodem():
		
	modem.set_cmee(0)
	# signal_quality_range  = modem.get_signal_quality_range()
	modem.get_signal_quality_range()
	# modem.check_sim_pin(5, PIN_NUMBER)
	modem.check_sim_pin(5, PIN_NUMBER)
	# network_status = modem.get_network_registration_status()
	modem.get_network_registration_status()
	modem.set_recognition(0)
	modem.set_vtd(10)
	modem.hangup()

def main_loop():
		global USER_ID
		global FLAG_OFFLINE
		global FLAG_CONNECTED
		global FLAG_RECORDED
		_USER_ID = USER_ID
		
		
		DTMF_SONG = MySqlDATABASE.get_appelant(_USER_ID)
		APPELANT_SRV = DTMF_SONG[1]
		DTMF_SONG = DTMF_SONG[0]
		
		print("DTMF SONG: ", DTMF_SONG)
		# print("APPELANT : ", APPELANT_SRV)
				
		if FLAG_OFFLINE == True:
			modem.call(TEL)
			# CallCountDown(2)
			for x in range (5):
				if FLAG_CONNECTED == False :
					FLAG_CONNECTED = modem.check_connected()
					print ("Attempt : ", x)
					# CallCountDown(1)
			
			# while FLAG_CONNECTED == True :
			while (modem.check_connected()) == True :
				# print("Mac and Cheese")
				# MacAndCheese(USER_ID, APPELANT_SRV,DTMF_SONG)
				
				print("user id : ", USER_ID)
				# CallCountDown(1)
				FLAG_CAN_RECORD = modem.send_dtmf_code(DTMF_SONG)
				print("DTMF SEND")

				# CallCountDown(1)
				if FLAG_CAN_RECORD == True and FLAG_RECORDED == False:
					myaudio.recordheure(APPELANT_SRV)
					print ("AUDIO DONE")
					FLAG_RECORDED = True
					FLAG_CAN_RECORD = False
				
				if FLAG_RECORDED == True :
					print(" new player ")
					USER_ID = USER_ID + 1
					
					FLAG_OFFLINE = False
					FLAG_CONNECTED = False
					FLAG_RECORDED = False
					main_exit()
def main_exit():
	# nice and clean exit
	# modem.send_sms('+33664018952', 'Your job will be mine : .... !')
	SimHardaware.L_OFFON()

def main():
	main_initmodem()
	main_loop()
	
if __name__ == "__main__":
	main()
