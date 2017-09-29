'''

HolzPuzzle.py

Loesung eines 6-teiligen Holzpuzzles

Uebung zur Nutzung verschiedener Datentypen in Python.

 7 sep 2017 Hans-Georg Koepken
 
'''
import numpy as np
import copy

file = open('Puzzle.txt','r')
PuzzleString=file.read()
file.close()
# Wertepaare iy,iz
yzpos={'H':[1,1], 'h':[1,0], 'V':[0,1], 'v':[0,0]}

# Puzzleteile als Liste 6 leerer Matrizen anlegen
Parts=[ np.empty((3,0)) for iPart in range(6) ]
ix=0
iPart=0
for i in range(len(PuzzleString)):
	# Neue Zeile 	
	if PuzzleString[i]=='\n':
		if ix>0:
			ix= 0
		else:
			# Leerzeile startet neues Teil
			iPart= iPart+1
		continue
	# Vektor (ix,iy,iz) zur Liste des aktuellen Teils hinzufuegen
	if PuzzleString[i] in yzpos:
		Parts[iPart]=np.append(Parts[iPart],np.mat([ix]+yzpos[PuzzleString[i]]).T,1)
	ix=ix+1
print('*** Start with ',len(Parts),' Parts')

# Drehung um X-Achse
Rx0=np.mat('0;0;1')
Rx=np.mat('1,0,0;0,0,1;0,-1,0')
# Drehung um Z-Achse
Rz0=np.mat('5;1;0')
Rz=np.mat('-1,0,0;0,-1,0;0,0,1')

# Jedes Teil in allen 8 Drehungen probieren
PartsRot=[ [] for iPart in range(len(Parts))]
for i in range(len(Parts)):
	x=Parts[i].astype(dtype=np.int)
	# Originalteil speichern (darf aussen keine Luecken haben)
	PartsRot[i]=[x]
	for j in range(7):
		x=Rx0+Rx*x
		if(j==3):
			x=Rz0+Rz*x
		shape=np.zeros([6,2,2],dtype=np.int)
		shape[x[0],x[1],x[2]]=1
		# gedrehtes Teil speichern, wenn aussen keine Luecken
		if shape[1][0][0]==1 and shape[1][1][0]==1 and shape[4][0][0]==1 and shape[4][1][0]==1:	
			PartsRot[i].append(x)
		
# 6 Positionen 
PosOff=[      np.mat('3;5;4')]
PosRot=[      np.mat(' 1, 0, 0; 0, 1, 0; 0, 0, 1')]
PosOff.append(np.mat('5;7;8'))
PosRot.append(np.mat(' 0, 1, 0; 0, 0,-1;-1, 0, 0'))
PosOff.append(np.mat('7;8;6'))
PosRot.append(np.mat(' 0, 0,-1;-1, 0, 0; 0,-1, 0'))
PosOff.append(np.mat('5;4;8'))
PosRot.append(np.mat(' 0,1, 0; 0, 0,1;-1, 0, 0'))
PosOff.append(np.mat('4;3;5'))
PosRot.append(np.mat(' 0, 0, 1; 1, 0, 0; 0, 1, 0'))
PosOff.append(np.mat('3;6;7'))
PosRot.append(np.mat(' 1, 0, 0; 0,-1, 0; 0, 0,-1'))

# Zustand des zusammengebauten Puzzles
state=np.zeros([12,12,12],dtype=np.int)
# bereits verbaute Teile
used=[0 for ip in range(6)]
# Position der verbauten Teile
PartsPos=[[] for ip in range(6)]

# Teil einfügen
def insertPart(position,part,rotation):
	ind=PosOff[position]+PosRot[position]*PartsRot[part][rotation]
	if np.max(state[ind[0],ind[1],ind[2]])==0:
		state[ind[0],ind[1],ind[2]]=part+1
		used[part]=1
		PartsPos[part]=ind
		return True
	else:
		return False

# Teil entfernen
def removePart(position,part,rotation):
	ind=PosOff[position]+PosRot[position]*PartsRot[part][rotation]
	state[ind[0],ind[1],ind[2]]=0
	used[part]=0

# Zustand anzeigen
def showState(state):
	for iy in range(5,-1,-1):
		for iz in range(6):
			for ix in range(6):
				print(state[ix+3,iy+3,iz+3],' ',end='')
			print('  ',end='')
		print()
		
global sol
sol=0
solutions=[]
solpos=[]

# Alle Loesungszustaende suchen
def solve(pos):
	global sol
	for part in range(6):
		if used[part]:
			continue
		for rot in range(len(PartsRot[part])):
			if insertPart(pos,part,rot):
				#print('pos=',pos,' part',part,' rot',rot)
				if pos==5:
					print('sol ',sol)
					solutions.append(np.copy(state))
					solpos.append(copy.deepcopy(PartsPos))
					sol=sol+1
				else:
					solve(pos+1)
				removePart(pos,part,rot)
				
# erstes Teil festlegen um gedrehte Loesungen zu vermeiden
insertPart(0,0,0)
solve(1)
removePart(0,0,0)
showState(solutions[0])
# Verschiebungen
directions=np.mat('-1,1,0,0,0,0;0,0,-1,1,0,0;0,0,0,0,-1,1')

# Teil verschieben
def movePart(part,shift):
	ind=PartsPos[part]
	state[ind[0],ind[1],ind[2]]=0
	ind2=PartsPos[part]+directions[:,shift]
	ok= np.max(state[ind2[0],ind2[1],ind2[2]])==0
	if ok:
		ind=ind2
	state[ind[0],ind[1],ind[2]]=part+1
	return ok

movePart(0,0)


