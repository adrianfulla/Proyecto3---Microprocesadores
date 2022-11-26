!find / -iname 'libdevice'
!find / -iname 'libnvvm.so'
#Librerias para funcionamiento de CUDA en Python en Google Collaboratory
#Universidad del Valle de Guatemala
#Programacion de Microprocesadores
#
#Proyecto 3
#
#David Jonathan Aragon Vasquez - 21053
#Adrian Fulladolsa Palma - 21592
#Renatto Guzman Sosa - 21646


# Link de Google Sheets: https://docs.google.com/spreadsheets/d/16fah92m0G2jjedTm7LPEi9xMwk2Fdl_VbAL7iWN8Zqk/edit#gid=0

#Conexion a servicios de Google 
from google.colab import auth
auth.authenticate_user()

#Importacion de librerias
from numba import cuda
import math
import numpy as np
import time

#Conexion a Google Sheets
import gspread
from google.auth import default
creds, _ = default()

gc = gspread.authorize(creds)

print("\nCalculadora de porcentaje de cambio promedio al acercar una llama a un sensor de temperatura\n")
print("Se esperan 500 datos\n")

#Obtencion de datos de archivo de Google Sheets
wb = gc.open_by_key('16fah92m0G2jjedTm7LPEi9xMwk2Fdl_VbAL7iWN8Zqk')
ws = wb.worksheet('DatosTemperatura')
array1 = np.array(ws.col_values(1)).astype(np.float32)




#Se esperan a tener 500 datos en el archivo
while(len(array1)<500):
  array1 = np.array(ws.col_values(1)).astype(np.float64)
  print("Esperando a 500 datos, actualmente hay: " + str(len(array1)))
  time.sleep(1)

print("\nSe han obtenido 500 datos")

#Se inicia conexion a GPU
import os
os.environ['NUMBAPRO_LIBDEVICE'] = "/usr/local/cuda-10.0/nvvm/libdevice"
os.environ['NUMBAPRO_NVVM'] = "/usr/local/cuda-10.0/nvvm/lib64/libnvvm.so"


#Kernel a utilizar, obtiene porcentaje de cambio de datos en dos arrays
@cuda.jit
def porcentaje_de_cambio_kernel(N, x, y, out):
  idx = cuda.grid(1)
  
  if  (idx < N):    
    out[idx] = (y[idx]-x[idx])/x[idx]

    
#Arrays para almacenar datos de antes y despues de acercar llama a sensor de temperatura, este evento se concidera la mitad del array de datos importados
arAntes = []
arDesp = []

#Se separa el array de datos importados en dos arrays desde el punto medio hasta los extremos
for i in range(len(array1)//2):
  arAntes.append(array1[len(array1)//2-i-1])
  arDesp.append(array1[len(array1)//2+i])

#Se obtiene la cantidad de Threads a necesitar
N = len(array1)//2

# Se mueven datos de arrays de Host a Device
d_a = cuda.to_device(arAntes)
d_d = cuda.to_device(arDesp)
# Se crea array en Device para almacenar datos resultantes del kernel
d_out = cuda.device_array_like(d_a)

# Se crea la cantidad de hilos y bloques, se utiliza 1 hilo por bloque para prevenir dasaprovechamiento de GPU
threads = 1
blocks = (N // threads) + 1
#Se inicia kernel
porcentaje_de_cambio_kernel[blocks, threads](N, d_a, d_d, d_out,)
#Se espera a que el kernel termine
cuda.synchronize()

#Se mueve array resultante de kernel de device a host
out = d_out.copy_to_host()

#Se calcula el porcentaje de cambio promedio 
promedio = 0.0
for i in out:
  promedio += i
promedio = promedio/len(out) *100 
print("\nEl porcentaje de cambio promedio al acercar una llama al sensor es: " + str(promedio) + "%")

#Fin de programa
print("\n\n")
