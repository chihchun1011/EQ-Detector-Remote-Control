import paramiko
import time
import csv
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.dates as plt_date
# import pytz

def Init_Connection():
	global client, transport
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect('IP',username='usr',password='pwd')

	transport = client.get_transport() ##create a transport
	if transport.is_active() :
		print("Successfully connected.")
	else :
		print("Reconnecting...")
		Init_Connection()

def Visualization(data):
	matplotlib.rcParams['timezone'] = 'Asia/Shanghai'
	time = plt_date.date2num([d['time'] for d in data_list])
	# print(time)
	plt.figure(figsize=(9,5))
	plt.suptitle('2020.11.29')
	plt.subplot(2,1,1)
	plt.subplots_adjust(left=None, bottom=0.2, right=None, top=None, wspace=7, hspace=0.5)
	plt.plot_date(time , [data['temperature'] for data in data_list] , fmt='-')
	# plt.xlabel('time')
	plt.xticks(rotation=25)
	plt.ylabel('T(˚C)')
	plt.subplot(2,1,2)
	plt.plot_date(time , [data['humidity'] for data in data_list] , fmt='-')
	plt.xlabel('time')
	plt.xticks(rotation=25)
	plt.ylabel('H(%)')
	plt.show()



if __name__ == "__main__":
	Init_Connection()

	#Get Data by command
	# stdin,stdout,stderr = client.exec_command('cd /wk_cms2/chihchun;cat abc.csv',get_pty=True) ##open a channel
	# receive = stdout.read()
	# print(receive.decode())
	if transport.is_active() :
		sftp_client = paramiko.SFTPClient.from_transport(client.get_transport())
		sftp_client.get('/wk_cms2/chihchun/abc.csv', './abc.csv')
		sftp_client.close()
	else :
		print("Reconnecting...")
		Init_Connection()

	d = {}
	data_list = []

	with open('./abc.csv') as csvfile:
		reader = csv.DictReader(csvfile)
		next(reader)
		for row in reader:
			# timee = row['time'].split()
			# d['day'] = timee[0]+timee[1]+timee[2]+timee[4]
			# d['time'] = timee[3]
			# print(row['time'])
			d['time'] = row['time']
			d['temperature'] = float(row['temperature'])
			d['humidity'] = float(row['humidity'])
			# print(d)
			data_list.append(d.copy())

	Visualization(data_list)
	
	# time.sleep(0.0000000000000001)   ##macOS attribute error
	client.close()