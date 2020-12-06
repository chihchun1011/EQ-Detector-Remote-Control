import paramiko
from datetime import datetime as dt
from datetime import timezone, timedelta
import time
import csv
import Adafruit_DHT
import pytz

def Init_Connection():
	global client, transport
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect('ntugrid5.phys.ntu.edu.tw',username='chihchun',password='EYP*aRMA|_')

	transport = client.get_transport() ##create a transport
	if transport.is_active() :
		print("Successfully connected.")
	else :
		print("Reconnecting...")
		Init_Connection()

def Init_Sensor():
	global sensor, pin
	sensor = 22
	pin = 2


if __name__ == "__main__":
	
	Init_Connection()
	Init_Sensor()

	data_list =[]

	# # header = ['time', 'temperature', 'humidity']
	# with open('./abc.csv', 'w', newline='') as csvfile:	
	# 		writer1 = csv.writer(csvfile)
	# 		writer1.writerows(['time', 'temperature', 'humidity'])
	
	while True:
		# t0 = time.time()
		while len(data_list) <= 1 : 
			t1 = time.time() 
			humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

			if humidity is not None and temperature is not None:
				now = dt.now( tz=timezone( timedelta(hours=8) ) )
				data = {'time' : now ,'temperature' : temperature, 'humidity': humidity}
				data_list.append(data)

			else : 
				print("Failed to get data from DHT22")
			# print("read data",time.time()-t1)

		# print("read total time",time.time()-t0)
		# t3 = time.time()
		header = data_list[0].keys()
		with open('./abc.csv', 'a+', newline='') as csvfile:	
			writer2 = csv.DictWriter(csvfile,header)
			writer2.writerows(data_list)
		# t4 = time.time()
		# print("writing time",t4-t3)
		##uploading

		if transport.is_active() : 
			sftp_client = paramiko.SFTPClient.from_transport(transport)
			sftp_client.put('/home/pi/Desktop/abc.csv', '/wk_cms2/chihchun/abc.csv')
			sftp_client.close()
			print("Successfully uploaded.")

		else :
			print("Reconnecting...")
			Init_Connection()
		# print("uploading time",time.time()-t4)
		data_list =[]

	client.close()