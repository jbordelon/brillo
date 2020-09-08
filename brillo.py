#!/usr/bin/python3

# Brillo V1.0 José Bordelon 8jul2015

# http://www.tutorialspoint.com/python/tk_pack.htm
# http://www.tutorialspoint.com/python/tk_frame.htm
# http://www.tutorialspoint.com/python/tk_scale.htm

from tkinter import *
from tkinter import ttk
# from subprocess import call
import subprocess

aMonitor = []
aBrillo = []
aGamma = []
Xbl = 100        # 0-15 lee de 0 a 100 en comando
MonActual = -1

def centrar(ventana):
	ventana.update_idletasks()
	w=ventana.winfo_width()
	h=ventana.winfo_height()
	extraW=ventana.winfo_screenwidth()-w
	extraH=ventana.winfo_screenheight()-h
	ventana.geometry("%dx%d%+d%+d" % (w,h,extraW/2,extraH/2))

def Salir():
	exit()

def Preset(NivelBrillo, NivelGamma):
	global MonActual
	aGamma[MonActual] = NivelGamma
	aBrillo[MonActual] = NivelBrillo
	# print(NivelBrillo, NivelGamma)
	# CambiaGamma(NivelGamma)
	# CambiaBrillo(NivelBrillo)
	sGamma.set(NivelGamma)
	sBrillo.set(NivelBrillo)
	Xrandr(0)

def CambiaGamma(Nivel):
	global MonActual
	aGamma[MonActual] = Nivel
	lGamma['text'] = '\n ' + Nivel
	# print(MonActual, Nivel, aGamma)

def CambiaBrillo(Nivel):
	global MonActual
	aBrillo[MonActual] = Nivel
	lBrillo['text'] = '\n ' + str(int(float(Nivel) * 100)) + ' %'
	# print(MonActual, Nivel, aBrillo)

def CambiaXbl(Nivel):
	global Xbl
	lXbl['text'] = '\n ' + Nivel + ' %'
	Xbl = Nivel
	# print(Xbl)

def CambiaMonitor(Nada):
	global MonActual
	MonActual = cMonitores.current()
	sGamma.set(aGamma[MonActual])
	sBrillo.set(aBrillo[MonActual])

def SueltaScale(Nada):
	Xrandr(0)

def SueltaXbl(Nada):
	# print("Xbl:", Xbl)
	# subprocess.call(["xbacklight", "-set", sXbl.get()])
	subprocess.call(["xbacklight", "-set", str(Xbl)])

def Xrandr(Nada):
	global MonActual
	# xrandr --output LVDS1 --brightness 0.75 --gamma 0.6:0.6:0.6
	# print("Mon:", aMonitor[MonActual], "Activo:", MonActual, "Brillo:", aBrillo[MonActual], "Gamma:", aGamma[MonActual])
	# Temporal = "xrandr --output " + aMonitor[MonActual] + " --brightness " + aBrillo[MonActual] + " --gamma " + aGamma[MonActual] + ":" + aGamma[MonActual] + ":" + aGamma[MonActual]
	# subprocess.call(["xrandr", Temporal])
	# print("xrandr", Temporal)
	subprocess.call(["xrandr", "--output", aMonitor[MonActual], "--brightness", aBrillo[MonActual], "--gamma", aGamma[MonActual] + ":" + aGamma[MonActual] + ":" + aGamma[MonActual]])
	# print(           "xrandr", "--output", aMonitor[MonActual], "--brightness", aBrillo[MonActual], "--gamma", aGamma[MonActual] + ":" + aGamma[MonActual] + ":" + aGamma[MonActual])

# Lee xbacklight va de 0 a 100
p = subprocess.Popen('xbacklight -get', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

#try:
#Xbl = int(float(p.stdout.read()))
#except:
#	print("\n=== Error ejecutando xbacklight -get ===\nPuede instalar xbacklight usando $sudo apt-get install xbacklight\n")
#	Salir()

# print('Xbacklight:', Xblight)
# print('Xbacklight:', Xblight.decode("utf-8"))

# Lee xrandr:
Contador = 0
PosSig = -2
p = subprocess.Popen('xrandr --current --verbose', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
for Linea in p.stdout.readlines():
	# print(Linea)
	if Linea[:1] != b'\t' and Linea[:1] != b' ' and Linea[:6] != b'Screen':
		Pos = Linea.find(b' ')
		# print(Linea[Pos+1:Pos+4])
		# Solo coloca los monitores conectados
		if Linea[Pos+1:Pos+4] == b'con':
			aMonitor.append((Linea[:Pos]).decode("utf-8"))
			PosSig = Contador + 4
			MonActual += 1
	elif Contador == PosSig:
		aGamma.append(1/float((Linea[13:16]).decode("utf-8")))
		# print('Gamma:',MonActual, aMonitor[MonActual], Contador, PosSig, Linea)
		# print('Gamma:', 1/float((Linea[13:16]).decode("utf-8")))
		#aGamma.append('1')
		#CambiaGamma(1/float((Linea[13:16]).decode("utf-8")))
	elif Contador == (PosSig + 1):
		aBrillo.append((Linea[13:17]).decode("utf-8"))
		# print('Brillo:',MonActual, aMonitor[MonActual], Contador, PosSig, Linea)
		# print('Brillo:', (Linea[13:17]).decode("utf-8"))
		#aBrillo.append('1')
		#CambiaBrillo((Linea[13:17]).decode("utf-8"))
	Contador += 1

# print(aMonitor)
# print(aBrillo)
# print(aGamma)
# print(Monitores, Contador, MonActivo)

# =============== Carga Form ===============
v = Tk()
v.geometry("400x400+200+100")
v.title("Brillo y Gamma")
# centrar(v)
v.resizable(0,0)

# =============== Agrega controles ===============

# Combo monitores:
cMonitores = ttk.Combobox(v, values=aMonitor, state='readonly')
cMonitores.bind('<<ComboboxSelected>>', CambiaMonitor)

# Botones de presets:
# f1 = Frame(v, bg='#000000')
f1 = Frame(v, highlightthickness=1, highlightbackground='#000000', highlightcolor='#000000')
b1 = Button(f1, text=" ", command=lambda: Preset('0.2', '0.5'), bg='#000000', fg='#000000', bd=0, highlightthickness=0)
b2 = Button(f1, text=" ", command=lambda: Preset('0.3', '0.3'), bg='#202020', fg='#202020', bd=0, highlightthickness=0)
b3 = Button(f1, text=" ", command=lambda: Preset('0.45', '0.4'), bg='#404040', fg='#404040', bd=0, highlightthickness=0)
b4 = Button(f1, text=" ", command=lambda: Preset('0.6', '0.5'), bg='#606060', fg='#606060', bd=0, highlightthickness=0)
b5 = Button(f1, text=" ", command=lambda: Preset('0.75', '0.6'), bg='#808080', fg='#808080', bd=0, highlightthickness=0)
b6 = Button(f1, text=" ", command=lambda: Preset('0.9', '0.7'), bg='#a0a0a0', fg='#a0a0a0', bd=0, highlightthickness=0)
b7 = Button(f1, text=" ", command=lambda: Preset('1.1', '0.8'), bg='#c0c0c0', fg='#c0c0c0', bd=0, highlightthickness=0)
b8 = Button(f1, text=" ", command=lambda: Preset('1.3', '0.3'), bg='#e0e0e0', fg='#e0e0e0', bd=0, highlightthickness=0)
b9 = Button(f1, text=" ", command=lambda: Preset('1.5', '0.2'), bg='#ffffff', fg='#ffffff', bd=0, highlightthickness=0)

# Sliders de Brillo y Gamma:
f2 = Frame(v, width=380)
sBrillo = Scale(f2, label="Brillo:", orient=HORIZONTAL, length=240, from_=0.1, to=1.5, resolution=0.05, showvalue=0, command=CambiaBrillo)
sBrillo.bind("<ButtonRelease-1>", SueltaScale)
sBrillo.set(aBrillo[MonActual])
lBrillo = Label(f2, text = aBrillo[MonActual], font=("Helvetica", 16))

f3 = Frame(v, width=380) #, width=400
sGamma = Scale(f3, label="Gamma:", orient=HORIZONTAL, length=240, from_=0.2, to=3, resolution=0.1, showvalue=0, command=CambiaGamma)
sGamma.bind("<ButtonRelease-1>", SueltaScale)
sGamma.set(aGamma[MonActual])
lGamma = Label(f3, text = aGamma[MonActual], font=("Helvetica", 16))

f4 = Frame(v, width=380) #, width=400
sXbl = Scale(f4, label="xBackLight:", orient=HORIZONTAL, length=240, from_=0, to=100, resolution=10, showvalue=0, command=CambiaXbl)
sXbl.bind("<ButtonRelease-1>", SueltaXbl)
# print("Xbl2:",Xbl)
sXbl.set(Xbl)
lXbl = Label(f4, text = sXbl.get(), font=("Helvetica", 16))

# Botones inferiores:
bSalir = ttk.Button(v, text ="Salir", command=Salir, padding=10)
bRestaurar = ttk.Button(v, text ="Restaurar", command=lambda: Preset('1.00', '1.0'), padding=10)

cMonitores.current(MonActual)

# ========== PACKS ==========
cMonitores.pack(ipadx=5, ipady=5, pady=20)

# Botones de presets:
f1.pack() #f1.pack(ipadx=1, ipady=1)
b1.pack(side = LEFT, ipadx=5, ipady=5)
b2.pack(side = LEFT, ipadx=5, ipady=5)
b3.pack(side = LEFT, ipadx=5, ipady=5)
b4.pack(side = LEFT, ipadx=5, ipady=5)
b5.pack(side = LEFT, ipadx=5, ipady=5)
b6.pack(side = LEFT, ipadx=5, ipady=5)
b7.pack(side = LEFT, ipadx=5, ipady=5)
b8.pack(side = LEFT, ipadx=5, ipady=5)
b9.pack(side = LEFT, ipadx=5, ipady=5)

# Sliders:
#f2.pack(padx=20, pady=10)
f2.pack(padx=20)
sBrillo.pack(side = LEFT)
lBrillo.pack(side = LEFT, padx=20) #, pady=10)

f3.pack(padx=20)
sGamma.pack(side = LEFT)
lGamma.pack(side = LEFT, padx=20) #, pady=10)

f4.pack(padx=20)
sXbl.pack(side = LEFT)
lXbl.pack(side = LEFT, padx=20) #, pady=10)

# Botones:
bSalir.pack(side = LEFT, padx=30)
bRestaurar.pack(side = RIGHT, padx=30)

v.mainloop()
