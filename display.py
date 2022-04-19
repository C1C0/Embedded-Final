from time import sleep
from tkinter import Tk, StringVar, IntVar
from tkinter import ttk
from turtle import position, update

import sqlite3
import threading


def check(updateCounter, data, history: list):
    con = sqlite3.connect('station.db')
    cur = con.cursor()

    while True:
        print("looping")
        sleep(2)
        updateCounter.set(updateCounter.get() + 1)
        for row in cur.execute('SELECT * FROM measurements ORDER BY id DESC LIMIT 1'):
            data["temperature"].set(str(row[1]))
            data["humidity"].set(str(row[2]))
            data["pressure"].set(str(row[3]))
            
        for index, row in enumerate(cur.execute('SELECT timestamp, temperature FROM measurements ORDER BY id DESC LIMIT 10')):
            history[index][0].set(row[0])
            history[index][1].set(row[1])

def setup() -> None:
    """Setup and run display"""

    root = Tk()

    data = {
        "temperature": StringVar(),
        "humidity": StringVar(),
        "pressure": StringVar(),
    }
    
    history=[]
    
    updateCounter = IntVar()
    
    con = sqlite3.connect('station.db')
    cur = con.cursor()

    root.title("Weather Station")

    frm = ttk.Frame(root, padding=2)

    frm.grid()

    for row in cur.execute('SELECT * FROM measurements ORDER BY id DESC LIMIT 1'):
        print(type(str(row[1])), str(row[1]))

        data["temperature"].set(str(row[1]))
        data["humidity"].set(str(row[2]))
        data["pressure"].set(str(row[3]))
        
    for row in cur.execute('SELECT timestamp, temperature FROM measurements ORDER BY id DESC LIMIT 10'):
        history.append((StringVar(None, row[0]), IntVar(None, row[1])))

    ttk.Label(frm, text="Weather Station", font=25).grid(column=0, row=0)
    ttk.Label(frm, textvariable=updateCounter).grid(column=1, row=0)

    ttk.Label(frm, text="Temperature").grid(column=0, row=1)
    ttk.Label(frm, textvariable=data["temperature"], padding=25).grid(
        column=1, row=1)

    ttk.Label(frm, text="Humidity").grid(column=0, row=2)
    ttk.Label(frm, textvariable=data["humidity"],
              padding=25).grid(column=1, row=2)

    ttk.Label(frm, text="Pressure").grid(column=0, row=3)
    ttk.Label(frm, textvariable=data["pressure"],
              padding=25).grid(column=1, row=3)
    
    ttk.Label(frm, text="------------TEMP HISORY---------------------").grid(column=0, row=4)
    
    rowNow = 5
    
    for row in history:
        ttk.Label(frm, textvariable=row[0]).grid(column=0, row=rowNow)
        ttk.Label(frm, textvariable=row[1]).grid(column=1, row=rowNow)
        rowNow += 1
    
    thCheck = threading.Thread(target=check, args=(updateCounter, data, history))
    thCheck.start()

    root.mainloop()


if __name__ == '__main__':
    setup()
