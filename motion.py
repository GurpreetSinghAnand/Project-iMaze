import time
import pyfinch

finch = pyfinch.Finch()
direction = ['ST','ST','ST','ST','RT','ST','ST','ST','LT']
for dir in direction:
	print dir, "\n"
	if dir == 'ST':		
		finch.wheels(0.8,0.7) # straight
		time.sleep(0.75)
	elif dir == 'RT':
		finch.wheels(0.8,-0.7) # turn right
		time.sleep(0.5),
	elif dir == 'LT':
		finch.wheels(-0.8,0.7) # turn left
		time.sleep(0.5),
	print finch.obstacle()

finch.wheels(0,0) # stop
