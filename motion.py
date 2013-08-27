import time
import pyfinch

finch = pyfinch.Finch()
direction = ['ST','ST','ST','ST','RT','ST','ST','ST','LT']
for dir in direction:
	print dir, "\n"
	if dir == 'ST':		
		finch.wheels(1.0,0.9) # straight
		time.sleep(0.75)
	elif dir == 'RT':
		finch.wheels(1.0,-0.9) # turn right
		time.sleep(0.5),
	elif dir == 'LT':
		finch.wheels(-1.0,0.9) # turn left
		time.sleep(0.5),
	print finch.obstacle()

finch.wheels(0,0) # stop
