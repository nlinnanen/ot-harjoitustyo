
from tkinter import Tk, Entry
import tkinter



def main():
    window = Tk()
    window.title("Todo application")
    window.geometry("400x400")
    entry = Entry(window, width=10)
    entry.pack(pady=20)

    print(tkinter.TkVersion)
    window.mainloop()

if __name__ == "__main__":
    main()
