import requests
import json
from adafruit_servokit import ServoKit
import time
pca=ServoKit(channels=16)

def moveServo(n):
	pca.servo[n].angle = 0
	time.sleep(.5)

	pca.servo[n].angle = 180
	time.sleep(.5)

	pca.servo[n].angle = 0
	time.sleep(.5)

while True:
	if __name__ == '__main__':
		
		casilleros = []
		
		with open(r'Lockers.txt', 'r') as fp:
			for line in fp:
				
				x = line[:-1]
				
				if x == '0':
					casilleros.append(int(x))
				else:
					casilleros.append(x)
		
		url = 'http://dev.relred.com/soldix/api/transactions'
		user = input('Scan QR\n')
		payload = { 'u_id': user, 'p_id': 'p6368e1c90d9bc' }
		
		if user in casilleros:
			
			n = casilleros.index(user)
			moveServo(n)
			casilleros[n] = 0
			
		else:
			
			if 0 in casilleros:
				n = casilleros.index(0)
				
				response = requests.post(url, json=payload)
				print(response.url)
				
				if response.status_code == 200:
					result = response.json()
					if result['message'] == 'SUCCESS':
						moveServo(n)
						casilleros[n] = user
					if result['message'] == 'FAIL':
						
						continue
			else:
				
				continue
		
		with open(r'Lockers.txt', 'w') as fp:
			fp.truncate()
			for item in casilleros:
				fp.write("%s\n" % item)
			print('Done')
			
