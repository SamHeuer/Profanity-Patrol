from tkinter import *
from PIL import Image,ImageTk
from customtkinter import *
from hatesonar import Sonar

width,height=960,667

root=Tk()
sonar = Sonar()
inputText= StringVar()

def textparser(obj):
    topClass=obj['top_class']
    str=""
    hateSpeechConfidence=(obj['classes'][0]['confidence'])*100
    offensiveLanguageConfidence=(obj['classes'][1]['confidence'])*100
    neitherConfidence=(obj['classes'][2]['confidence'])*100
    if(topClass=='hate_speech'):
        str+="The text has been analyzed and determined to be classified as \"hate speech\" with a confidence level of {:.2f}% . ".format(hateSpeechConfidence)
        
        if(offensiveLanguageConfidence<neitherConfidence):
            str+="Additionally, it has been deemed as \"offensive language\" with a confidence level of {:.2f}%, and as \"neither\" with a confidence level of {:.2f}%.".format(neitherConfidence,offensiveLanguageConfidence)

        else:
            str+="Additionally, it has been deemed as \"neither\"  with a confidence level of {:.2f}%, and as \"offensive language\" with a confidence level of {:.2f}%.".format(offensiveLanguageConfidence,neitherConfidence)

    elif(topClass=='neither'):
        str+="Upon careful analysis and examination, the text has been deemed as appropriate and inoffensive, with a primary classification of \"neither\" at a confidence level of {:.2f}% . ".format(neitherConfidence)

        if(hateSpeechConfidence<offensiveLanguageConfidence):
            str+="It is noteworthy, however, that there are slight indications of  \"offensive language\" and \"hate speech\" present, with respective confidence levels of {:.2f}% and {:.2f}%.".format(offensiveLanguageConfidence,hateSpeechConfidence)

        else:
            str+="It is noteworthy, however, that there are slight indications of \"hate speech\" and \"offensive language\" present, with respective confidence levels of {:.2f}% and {:.2f}%.".format(hateSpeechConfidence,offensiveLanguageConfidence)
            
    else:
        str+="It has been identified that it contains explicit and offensive language, with a predominating classification of \"offensive language\" at a confidence level {:.2f}% . ".format(offensiveLanguageConfidence)

        if(neitherConfidence<hateSpeechConfidence):
            str+="It should be noted that there is also a slight inclination towards \"hate speech\" at a confidence level of {:.2f}% and \"neither\" at a confidence level of {:.2f}%.".format(hateSpeechConfidence,neitherConfidence)
        
        else:
            str+=". It should be noted that there is also a slight inclination towards \"neither\" at a confidence level of {:.2f}% and \"hate speech\" at a confidence level of {:.2f}%.".format(neitherConfidence,hateSpeechConfidence)
    
    return str 

def hatecheck():
    global computedOutput
    outputField.place_forget()
    parsedText=textparser(sonar.ping(text=inputText.get()))
    computedOutput.set(parsedText)
    outputField.text=computedOutput.get()
    outputField.place(relx=0.05,rely=0.55)

def refresh():
    global inputText,computedOutput
    inputText.set("")
    inputField.text=""
    computedOutput.set("")
    outputField.text=computedOutput.get()
    outputField.place_forget()

# Configuring root window
root.title("FoulSpeech")
root.geometry("{}x{}".format(width,height))
root.minsize(width=width, height=height)
root.maxsize(width=width, height=height)
root.iconbitmap("./Media/Icon/icon.ico")

# setting background image
img=Image.open("./Media/BackgroundImg/Home.jpg")
backgroundimg = ImageTk.PhotoImage(img,Image.ANTIALIAS)
coverimagelabel = Label(root,image=backgroundimg,highlightthickness=0)
coverimagelabel.pack(fill="both")

homeCardWidgetContainerBox=CTkFrame(root, corner_radius=10,fg_color="#07085b",bg_color="#07085b",width=200,height=200)
homeCardWidgetContainerBox.place(relx=0.15,rely=0.25,anchor="center")

HeadingLabel=Label(homeCardWidgetContainerBox,text="Profanity\nPatrol",font=("Segoe UI bold",32),fg="white",bg="#07085b")
HeadingLabel.place(relx=0.5,rely=0.5,anchor= CENTER)

inputForm=CTkFrame(root, corner_radius=10,fg_color="#7e7fd2",bg_color="#7e7fd2",width=400,height=500)
inputForm.place(relx=0.75,rely=0.5,anchor=CENTER)

inputField= CTkEntry(inputForm,textvariable = inputText,fg_color="white",text_color="black",font=("Segoe UI",13),width=320,height=30)
inputField.place(relx=0.1,rely=0.2)
inputField.focus_force()

getResultButton=CTkButton(inputForm,width=160,corner_radius=8,text_color="white",fg_color="#4e4fa2",hover_color="#373771", border_width=0, command=hatecheck,height=30,text="Get Result",text_font=("Segoe UI bold",13))
getResultButton.place(relx=0.58,rely=0.4)

refreshButton=CTkButton(inputForm,width=160,corner_radius=8,text_color="white",fg_color="#4e4fa2",hover_color="#373771", border_width=0, command=refresh,height=30,text="Refresh",text_font=("Segoe UI bold",13))
refreshButton.place(relx=0.75,rely=0.4)

computedOutput=StringVar()
computedOutput.set("")
outputField=CTkLabel(inputForm,corner_radius=10, fg_color="white",bg_color="#7e7fd2",textvariable=computedOutput,height=200,width=360,wraplengt=350)

inputField.bind('<Return>',hatecheck)

root.mainloop()