from tkinter import *
from tkinter.filedialog import *
import detect
import os
from datetime import date
today = date.today()
filepath=""
def f1():
    global filepath
    filepath1 = askopenfilename(title="Ouvrir une image",filetypes=[('png files','.png')])
    filepath=filepath1.replace('/','\\')
    print (filepath)
def f():
    #img = entree2.get()
    name = entree1.get()
    #function
    dirName = "dataset/"+name
    try:
        # Create target Directory
        os.mkdir(dirName)
        print("Directory " , dirName ,  " Created ") 
    except FileExistsError:
        print("Directory " , dirName ,  " already exists")
    # Create target Directory if don't exist & create a new target for today
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Directory " , dirName ,  " Created ")
    else:
        dirName=dirName+"/"+str(today)
        try:
            os.mkdir(dirName)
            print("Directory" ,dirName ,  " Created ")
        except FileExistsError:
            print("Directory " , dirName ,  " already exists")
    #patientpath c'est le fichier de patient pour aujourdhui
    PatientPath=name
    print (PatientPath)
    detect.function(filepath,PatientPath)
     

fenetre = Tk()
fenetre.title("Parkinson detection")

photo = PhotoImage(file="parkinson.png")

l=Label(fenetre, text='Bienvenue dans votre application de détection du Parkinson!',background='#173F5F', fg='white', anchor=CENTER, width=77, height=3, font="Arial 16 bold")
l.pack()
p = PanedWindow(fenetre, orient=HORIZONTAL, width=1000, height=460)
p.pack(side=TOP)
p2 = PanedWindow(fenetre, orient=VERTICAL, width=550, height=460)
p2.pack(side=TOP)
entree1=Entry(p2, font="Arial 14")
button1=Button(p2,text="parcourir",font="Arial 12 bold", background='#173F5F', fg='white', height=2)
button=Button(p2,text="valider",font="Arial 12 bold", background='#cc0000', fg='white')
button['command']=f
button1['command']=f1

p2.add(Label(p2, text="Testez votre état de parkinson chez vous \navec un simple dessin. \nSaisissez votre nom dans la case de l'identifiant,\net le chemin de votre image de test dans la case suivante", background='white', anchor=CENTER, height=8, font="Arial 16 ") )
p2.add(Label(p2, text='Nom de patient :', anchor=CENTER, height=2,background='silver', font="Arial 14"))
p2.add(entree1, height=40)
p2.add(Label(p2, text="Chemin de l'image :", background='silver', anchor=CENTER, height=2, font="Arial 14") )
p2.add(button1, padx=100)
p2.add(button)
p.add(p2)
p.add(Label(p, image=photo))
fenetre.mainloop()