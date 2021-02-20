import pyttsx3
import tkinter
from tkinter import *
from tkinter import messagebox

engine = pyttsx3.init()
engine.setProperty("rate", 130)


def speak(root, message):
    answer = messagebox.askquestion("Confirmation", "Play speech?")
    if (answer == "yes"):
        engine.say(message.get("1.0", "end"))
        engine.runAndWait()
    message.delete("1.0", "end")


def paste(root, message):
    message.delete("1.0", "end")
    message.insert("1.0", root.clipboard_get())
    speak(root, message)


def main():
    root = tkinter.Tk()
    root.title("Simple Text-To-Speech by Glenn")
    
    positionRight = int(root.winfo_screenwidth()/2 - 500/2)
    positionDown = int(root.winfo_screenheight()/2 - 315/2)
    
    root.geometry("500x315+{}+{}".format(positionRight, positionDown))
    root.resizable(False, False)

    prompt = Label(root, text="Enter your message here:", font=('Tahoma', 12, 'bold'))
    message = Text(root, width=60, height=15)
    clipbrd = Button(root, text="Paste and Speak", width=30, command= lambda: paste(root, message))
    butn = Button(root, text="Speak message", width=30, command= lambda: speak(root, message))

    prompt.grid(row=0, column=0, padx=7.5, pady=2.5, columnspan=2)
    message.grid(row=1, column=0, padx=7.5, columnspan=2)
    clipbrd.grid(row=2, pady=7.5, column=0)
    butn.grid(row=2, pady=7.5, column=1)

    root.mainloop()


if __name__ == "__main__":
    main()
