import serial
import sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
import psutil
import collections
import json
import time

MIN_ROW = 0
MAX_ROW = 1

R_CARGA = 10 * (10**3)
R_DESCARGA = 220
C = 470 * (10**(-6))

TAU_CARGA = (R_CARGA * C)
TAU_DESCARGA = (R_DESCARGA * C)

charge_time_init = 0

voltaje = collections.deque(np.zeros(10))
tiempo = collections.deque(np.zeros(10))

comando = 'read'
estado = 'descarga'


def readlinefromArduino(self):
	try:
		global comando
		global charge_time_init
		global estado
		print(comando)
		
		arduino.write(str.encode(comando))
		arduino.flush()
		
		comando = 'read'
		
		line = arduino.readline()
		print(line)
		arduino_json = json.loads(line)
		print(arduino_json)
		vc = arduino_json["vc"]
		current_time = arduino_json["time"]

		print(vc)
		print(current_time)

		voltaje.append(vc)
		tiempo.append(current_time)
		
		actual_time = time.time()
		
		if(estado == 'carga'):
			tiempo_transcurrido = actual_time - charge_time_init	
			if(tiempo_transcurrido > 5*TAU_CARGA):
				ax.plot(tiempo,voltaje,'red')
			else:
				ax.plot(tiempo,voltaje,'blue')
		else:
			ax.plot(tiempo,voltaje,'blue')
		
		
	except Exception:
		pass	
	
	
	
class capacitorMode:

	def carga(self,event):
		global comando
		comando = 'carga'
		global charge_time_init
		charge_time_init = time.time()
		global estado
		estado = 'carga'
			
	
	def descarga(self,event):
		global comando
		global estado
		comando = 'descarga'
		estado = 'descarga'
		


port = sys.argv[1]
arduino = serial.Serial(port=port, baudrate=115200, timeout = 1.2)
#arduino.dtr = False
#arduino.rts = False
#arduino.port = port
#arduino.open()


fig, ax = plt.subplots()

fig.set_figwidth(10)
fig.set_figheight(6)

fig.subplots_adjust(bottom=0.2)

callback = capacitorMode()
axcarga = fig.add_axes([0.7,0.05,0.1,0.075])
bcarga = Button(axcarga, 'carga')
bcarga.on_clicked(callback.carga)

axdescarga = fig.add_axes([0.81,0.05,0.1,0.075])
bdescarga = Button(axdescarga, 'descarga')
bdescarga.on_clicked(callback.descarga)


plt.plot(tiempo,voltaje)
ax.set_xlabel('tiempo')
ax.set_ylabel('Voltaje')

ani = FuncAnimation(fig, readlinefromArduino, interval=400)
plt.show()
#arduino.close()
