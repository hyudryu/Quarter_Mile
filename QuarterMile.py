#Mark Chang
import csv
import tkMessageBox
import Tkinter
import easygui
from Tkinter import*

#setting global varaibles
time= []
vss = []
newvss = []
trap = 0
path = ""
def upload():
#Prompts user with path via GUI
	global newvss
	global path
	global vss
	global time
	path = easygui.fileopenbox()
	size = len(path)
	filetype = path[size-4:size]
	infile = open(path)
	time = []
	vss = []
	newvss = []
	#Check to see if filetype is valid
	if(filetype == ".csv"):
		#Takes all the valid speed and time measurements and 
		#appends them to their own list
		for line in infile:
			first = line[0]
			if first.isdigit():
				separated = line.split(',')
				time.append(separated[1])
				vss.append(separated[3]) #Change this to read ABS rear wheel speed
		try:
			#deletes all 0 values in the beginning of the datalog
			while vss[1] == '0':
				vss.pop(0)
				time.pop(0)
			newvss = [float(x)/3600 for x in vss]
			calculateQuarter()
		except:
			#Invalid/corrupted csv error message
			w.insert(INSERT, "Wtf kinda .csv file did you upload LOL\n1. Open the datalog on flashpro manager\n2. Click on 'Datalog' inbetween Online and Options\n3. Export it as a .csv file\n")
	#Invalid filetype		
	else:
		w.insert(INSERT, "Invalid filetype, please upload a .csv file. \n")
		
def calculateQuarter():
#All the math will be done here
	distance = 0.0
	counter = 1
	#0.25th of a mile
	while distance <= 0.25:
		#Calculus, sum of rectangles method to find the area under the VSS curve
		try:
			avg = (float(time[counter+1]) - float(time[counter]))* ((newvss[counter]+newvss[counter+1])/2)
			distance = distance + avg
			counter = counter + 1
		#if datalog's too short, it'll return this error and set distance to be 9999+
		except:
			distance = distance + 9999
	#If datalog was long enough...
	if(distance < 9900):	
		w.insert(INSERT, path + "\n")
		w.insert(INSERT, "Quarter mile time: ")
		w.insert(INSERT, float(time[counter-1]))
		w.insert(INSERT, "\nTrap Speed: ")
		w.insert(INSERT, int(float(newvss[counter-1])* 3600))
		counter = 1
		distance = 0
		#60' time
		while distance <= 0.01136364:
			avg = (float(time[counter+1]) - float(time[counter]))* ((newvss[counter]+newvss[counter+1])/2)
			distance = distance + avg
			counter = counter + 1
		w.insert(INSERT, "\n60 ft time: ")
		w.insert(INSERT, float(time[counter-1]))
		counter = 1
		distance = 0
		#Eighth mile time
		while distance <= 0.125:
			avg = (float(time[counter+1]) - float(time[counter]))* ((newvss[counter]+newvss[counter+1])/2)
			distance = distance + avg
			counter = counter + 1
		w.insert(INSERT, "\nEighth mile time: ")
		w.insert(INSERT, float(time[counter-1]))
		w.insert(INSERT, "\n\n")
	else:
		w.insert(INSERT, "Your datalog is too short, seems like you didn't even travel a quarter mile lol\nChoose a longer datalog...\n")		
#Gui stuff		
top = Tkinter.Tk()
upload = Tkinter.Button(top, text = "Upload File", command = upload)
top.resizable(width=False, height=False)
top.geometry('{}x{}'.format(700, 270))
#Message box
tkMessageBox.showinfo(title="Greetings", message="This is a free program for you to get your quarter mile time. \n Creator: Mark Chang ")
#If user wants tutorial
if tkMessageBox.askyesno(title="Tutorial?", message="Would you like a brief explanation on how to use this program?"):
	tkMessageBox.showinfo(title="Tutorial", message="This program will take a .csv file from your flashpro and compute a rough quarter mile estimation as well as the trap speed. \n\nThings to keep in mind when taking a datalog:\n   ~The less tirespin, the more accurate the estimation will be\n   ~The faster your datalog speed, the more accurate the estimation\n   ~The flatter the road, the better\n   ~Don't break any local laws when doing this\n\n\n")
	tkMessageBox.showinfo(title="Tutorial (continued)", message = "You would need to trim your .csv starting from when your car is at a dead stop(0mph), and the program will cut it off as soon as you've traveled 1/4 mile")
w = Text(top)
w.place(height = 200, width = 700, x=0, y=70)
upload.place(height = 69, width = 700)
top.mainloop()
