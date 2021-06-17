import os
import tkinter as tk
from tkinter import StringVar,filedialog,messagebox,ttk
from tkcalendar import DateEntry
from PIL import ImageTk,Image
import pymysql
from datetime import date


filename=''

def errorbox(stringval):
	messagebox.showerror('error',stringval)

def makeConn():
	conn=pymysql.connect(host='localhost',user='root',password='',database='student_data')
	return conn



window=tk.Tk()
window.title('Student Management')
window.geometry('800x720')
window.configure(bg='#ddddff')

#scroll=tk.Scrollbar(window)
#scroll.pack(side=tk.RIGHT,fill=tk.Y)
#window.configure(yscrollcommand=txt_vscroll.set)

#scrollFrame=tk.Frame(window,bg='#ddddff',width='50',height='30',yscrollcommand=scroll.set)
#scrollFrame.pack(side=tk.LEFT,fill=tk.BOTH)
titleLab=tk.Label(window,text='Student Management',bg='#ADADFF',width='20',height='2',font=("Times New Roman",30,"bold"))
titleLab.place(x=180,y=50)

fnameLab=tk.Label(window,text='First Name:',bg='#ddddff')
fnameLab.place(x=150,y=200)
fnameEnt=tk.Entry(window,width='50')
fnameEnt.place(x=250,y=200)
lnameLab=tk.Label(window,text='Last Name:',bg='#ddddff')
lnameLab.place(x=150,y=250)
lnameEnt=tk.Entry(window,width='50')
lnameEnt.place(x=250,y=250)
idLab=tk.Label(window,text='ID:',bg='#ddddff')
idLab.place(x=150,y=300)
idEnt=tk.Entry(window,width='25')
idEnt.place(x=250,y=300)
addressLab=tk.Label(window,text='Address:',bg='#ddddff')
addressLab.place(x=150,y=350)
addressEnt=tk.Entry(window,width='50')
addressEnt.place(x=250,y=350)
mobLab=tk.Label(window,text='Mob no:',bg='#ddddff')
mobLab.place(x=150,y=400)
mobEnt=tk.Entry(window,width='35')
mobEnt.place(x=250,y=400)
emailLab=tk.Label(window,text='Email:',bg='#ddddff')
emailLab.place(x=150,y=450)
emailEnt=tk.Entry(window,width='35')
emailEnt.place(x=250,y=450)
dobLab=tk.Label(window,text='DOB:',bg='#ddddff')
dobLab.place(x=150,y=500)
dobDate=DateEntry(window,bg='#ddddff',fg='#ffffff',locale='en_UK')
dobDate.place(x=250,y=500)

def nextFn():
	fname=fnameEnt.get().strip()
	lname=lnameEnt.get().strip()
	id=idEnt.get().strip()
	address=addressEnt.get().strip()
	mob=mobEnt.get().strip()
	email=emailEnt.get().strip()
	dob=dobDate.get()
	dobyear=dob.split('/')
	dobyear=int(dobyear[2])
	diffYear=int(str(date.today()).split('-')[0])-dobyear







	if(not fname.isalpha() and len(fname)<25):
		errorbox('Invalid First Name')
		return

	if(not (lname.isalpha() and len(lname)<26)):
		errorbox('Invalid Last Name')
		return
	if(not id.isnumeric()):
		errorbox('Invalid ID')
		return


	if(not (mob.isnumeric() and len(mob)==10 and (mob.startswith('7') or mob.startswith('8') or mob.startswith('9')))):
		errorbox('Invalid Mobile Number')
		return
	#email check
	domainName=['.com','.org','.co','.in']
	isdomain=False
	for i in domainName:
		if(email.endswith(i)):
			isdomain=True
			break
	if(not(email.find('@')!=-1 ) and isdomain==False):
		errorbox(('Invalid Email ID'))
		return


	if(diffYear<16 and diffYear>60):
		errorbox('Invalid Age : age should be between 16 and 60')

	connS = makeConn()
	cursorS = connS.cursor()
	insertQ = 'SELECT id, mobile,email FROM student_data'
	cursorS.execute(insertQ)
	recordData = cursorS.fetchall()
	print(recordData[0])

	for row in recordData:
		if(row[0]==id):
			errorbox('ID already in Database.\nPlease check again')
			return
		if (row[1] == mob):
			errorbox('Mobile No. already in Database.\nPlease check again')
			return
		if (row[2] == email):
			errorbox('Email ID already in Database.\nPlease check again')
			return



	window.destroy()
	window2=tk.Tk()
	window2.geometry('800x720')
	window2.title('Student Data Management')
	window2.configure(bg='#ddddff')

	genLabel=tk.Label(window2)


	gen=StringVar()
	genderLab=tk.Label(window2,text='Gender',bg='#ddddff',activebackground='#ADADFF')
	#genderLab.pack(anchor=tk.W)
	genderLab.place(x=100,y=100)
	#genList={'Male':'1','Female':'2'}
	gen1=tk.Radiobutton(window2,text='Male',value='male',variable=gen,bg='#ddddff')
	#gen1.pack(anchor=tk.W)
	gen1.place(x=250,y=100)
	gen2=tk.Radiobutton(window2,text='Female',value='female',variable=gen,bg='#ddddff')
	#gen2.pack(anchor=tk.W)
	gen2.place(x=250,y=150)

	imgLab=tk.Label(window2,text='Image',bg='#ddddff')
	imgLab.place(x=150,y=200)
	imgEnt=tk.Entry(window2,width='50')
	imgEnt.place(x=250,y=200)
	def openFn():
		#box=tk.Tk()
		imgEnt.delete(0,tk.END)
		global filename
		filename=filedialog.askopenfilename(initialdir='/storage/emulated/0',title='Select Image',filetypes=(('jpg files','*.jpg'),('jpeg files','*.jpeg')))
		if(os.path.getsize(filename)<250000):
			imgEnt.insert(tk.END,filename)
		else:
			errorbox('Size of Image is greater than 250kb')
			return

		root = tk.Toplevel()
		root.geometry('300x300')
		img = ImageTk.PhotoImage(Image.open(filename).resize((250,250),Image.ANTIALIAS))
		panel = tk.Label(root, image=img)
		panel.pack(side="bottom", fill="both", expand="yes")
		root.mainloop()

	openBut=tk.Button(window2,text='Open',bg='#ADADFF',command=openFn,font=("Times New Roman",12,"bold"))
	openBut.place(x=650,y=200)

	def checkFn():
		#window2.destroy()
		#check if ent is empty if not then get selected path check if that ttue or not
		if(gen.get()==''):
			errorbox('Please select gender')
			return
		checkWin=tk.Toplevel()
		checkWin.title('Student data')
		checkWin.geometry('600x720')
		checkWin.configure(bg='white')
		fnameWin=tk.Label(checkWin,text='First Name: '+fname,bg='white')
		fnameWin.place(x=100,y=100)
		lnameWin=tk.Label(checkWin,text='Last Name: '+lname,bg='white')
		lnameWin.place(x=100,y=150)
		idWin=tk.Label(checkWin,text='ID: '+id,bg='white')
		idWin.place(x=100,y=200)
		addressWin=tk.Label(checkWin,text='Address: '+address,bg='white')
		addressWin.place(x=100,y=250)
		mobWin=tk.Label(checkWin,text='Mobile: '+mob,bg='white')
		mobWin.place(x=100,y=300)
		emailWin=tk.Label(checkWin,text='Email: '+email,bg='white')
		emailWin.place(x=100,y=350)
		dobWin=tk.Label(checkWin,text='DOB: '+dob,bg='white')
		dobWin.place(x=100,y=400)
		genWin=tk.Label(checkWin,text='Gender: '+gen.get(),bg='white')
		genWin.place(x=100,y=450)
		global filename
		img=ImageTk.PhotoImage(Image.open(filename).resize((250,250),Image.ANTIALIAS))
		imgWinLab=tk.Label(checkWin,image=img,width=250,height=250)
		imgWinLab.place(x=300,y=100)
		checkWin.mainloop()

	checkBut=tk.Button(window2,text='Check',bg='#ADADFF',command=checkFn,font=("Times New Roman",12,"bold"))
	checkBut.place(x=100,y=300)

	def subFn():
		#connection
		global filename
		imgRB=open(filename,'rb')
		imgBin=imgRB.read()
		conn=makeConn()
		cursor=conn.cursor()
		insertQ="INSERT INTO student_data (firstname,lastname,id,address,mobile,email,dob,gender,image)  VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		var=(fname,lname,id,address,mob,email,dob,gen.get(),imgBin)
		cursor.execute(insertQ,var)
		conn.commit()
		messagebox.showinfo('Submitted','Data submitted')
		print('established')
		#query


	submitBut=tk.Button(window2,text='Submit',bg='#ADADFF',command=subFn,font=("Times New Roman",12,"bold"))
	submitBut.place(x=300,y=300)



	window2.mainloop()

nextBut=tk.Button(window,text='Next',bg='#ADADFF',command=nextFn,width=20,height=2,font=("Times New Roman",12,"bold"))
nextBut.place(x=350,y=600)

window.mainloop()
