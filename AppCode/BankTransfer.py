from tkinter import *
import datetime
import requests
from bs4 import BeautifulSoup as bs
import random
from tkinter import ttk
from time import sleep

with open('User.txt') as read:
    name,password = read.read().split()

pay = ('Gift','Borrow','Lend','Payment')

url = 'http://127.0.0.1:8000/'
login = url+'login'
session = requests.session()
rsp = session.get(url)
token = rsp.cookies['csrftoken']
session.post('http://127.0.0.1:8000/login',{'username':name,'password':password,'csrfmiddlewaretoken':token})
rsp = session.get(url)
token = rsp.cookies['csrftoken']
your_id = int(bs(session.get(url+'u_id').text,'lxml').find('body').text)
def last_transaction():
    try:
        bs(session.get(url+'last').text,'lxml').find('body').text.split()
        try:
            pk,summ = bs(session.get(url+'last').text,'lxml').find('body').text.split()
            return tuple(map(int,[pk,summ]))
        except ValueError:
            pk,summ,destin = bs(session.get(url+'last').text,'lxml').find('body').text.split()
            return tuple(map(int,[pk,summ]))+(destin,)
    except:
        return (None,None)
def account_now():
    return int(
        bs(session.get(url+'account').text,'lxml').find('body').text
        )
class Main:
    def __init__(self):
        self.root=Tk()
        self.root.title(name)
        self.period = 3500
        self.paused = False
        self.mFrame = Frame()
        self.mFrame.pack(side=TOP,expand=YES,fill=X)
        self.payment_dest = ttk.Combobox(self.mFrame,values=pay)
        self.last_trans = last_transaction()[0]
        self.summ = Entry(self.mFrame)
        self.receiver = Entry(self.mFrame)
        Label(self.mFrame,text='Summ').grid(row=0,column=0)
        Label(self.mFrame,text="Receiver's id").grid(row=0,column=1)
        self.current_sum = account_now()
        self.current = Label(self.mFrame,text=f"{self.current_sum} $")
        self.current.grid(row=2,column=1)
        self.summ.grid(row=1,column=0)
        self.receiver.grid(row=1,column=1)
        Button(self.mFrame,text='Transfer',command=self.transfer).grid(row=2,column=0)
        self.news = Text(self.mFrame, state='disabled')
        self.news.grid(row=1,column=3)
        self.payment_dest.grid(row=1,column=2)
        self.changeLabel()
    def changeLabel(self):
        try:
            requests.get('http://127.0.0.1:8000/')
        except:
            self.mFrame.destroy()
        else:
            last = last_transaction()
            if last[0]!=self.last_trans:
                self.news.config(state='normal')
                self.news.insert(END,f"You've got {last[1]} $. ")
                self.last_trans = last[0]
                self.news.insert(END,f"Now you have {self.current_sum+last[1]} $\n\n")
                if len(last)>2:
                    self.news.insert(END,f"Message: {last[2]}\n\n")
                self.news.config(state='disabled')
                self.current_sum += last[1]
                self.current.config(text=str(self.current_sum)+' $')
            self.mFrame.after(self.period, self.changeLabel) #it'll call itself continuously
    def transfer(self):
        receiver_id = int(self.receiver.get())
        summ = int(self.summ.get())
        self.news.config(state='normal')
        if summ>self.current_sum:
            self.news.insert(END,'You have not enough money\n\n')
        else:
            try:
                post = session.post(url+'transfer',{'receiver':receiver_id,'sender':your_id,'sum':summ,'csrfmiddlewaretoken':token,'destin':str(pay.index(self.payment_dest.get()))})
            except:
                post = session.post(url+'transfer',{'receiver':receiver_id,'sender':your_id,'sum':summ,'csrfmiddlewaretoken':token})
            self.news.insert(END,f"You've sent {summ} $. Now you have {self.current_sum-summ} $\n\n")
            self.current_sum -= summ
            self.current.config(text=str(self.current_sum)+' $')
        self.news.config(state='disabled')
obj1 = Main()

obj1.mFrame.mainloop()
