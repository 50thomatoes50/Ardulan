#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Tkinter import *
from ttk import *
import webbrowser
from threading import Thread

class NetChooser(Tk):
    """ Mon programme graphique utilisant Python3 et Tkinter """

    def __init__(self,ips):
        Tk.__init__(self)	# On dérive de Tk, on reprend sa méthode d'instanciation
        self.wm_title("Choose Network Interface")
        self.iconbitmap(default='ardulan.ico')
        # Widgets

        self.selected	= StringVar()
        self.SerialPorts	= ips
        self.liste	= Combobox(self, textvariable = self.selected, \
                                        values = self.SerialPorts, state = 'active', width=50)

        # Placement des widgets
        self.liste.pack(padx=5,pady=5)
        
        self.b = Button(self, text="OK", command=self.apply)
        self.b.pack(side=LEFT,padx=5,pady=5)
        
        self.button = Button(self, 
                         text="QUIT",
                         command=self.quit_win)
        self.button.pack(side=RIGHT,padx=5,pady=5)
        
    def apply(self):
        self.network = self.liste.get()
        #return comnb
        self.quit_win()
    
    def quit_win(self):
        self.destroy()
"""   def quit(self):
        Tk.quit(self)
        return self.getport()"""
 
# -------------------------

class Main(Tk):
    """ Mon programme graphique utilisant Python3 et Tkinter """

    def __init__(self,ip):
        Tk.__init__(self)	# On dérive de Tk, on reprend sa méthode d'instanciation
        self.wm_title("Ardulan Server")
        self.iconbitmap(default='ardulan.ico')
        # Widgets
        self.ip = ip
        
        self.frame1 = LabelFrame(self, text="Arduino connecté")
        self.scrollbar = Scrollbar(self.frame1)
        self.scrollbar.pack( side = RIGHT, fill=Y )

        self.tree = Treeview(self.frame1,yscrollcommand = self.scrollbar.set)
        self.tree.heading('#0', text='iD', anchor='w')
        self.tree["columns"]=("ip","type")
        self.tree.column('ip', width=100, anchor='center')
        self.tree.heading('ip', text='ip')
        self.tree.column('type', width=100)
        self.tree.heading('type', text='Type')
        self.tree.pack()
        #self.Lb1 = Listbox(self.frame1,yscrollcommand = self.scrollbar.set)
        #self.Lb1.pack()
        
        self.scrollbar.config( command = self.tree.yview )
        
        self.frame1.pack(padx=40,pady=5,ipadx=5,ipady=5)
        
        self.button = Button(self, 
                         text="QUIT",
                         command=self.destroy)
        self.button.pack(side=RIGHT,padx=5,pady=5)
        
        self.button1 = Button(self, 
                         text="Web",
                         command=self.OpenLink)
        self.button1.pack(side=LEFT,padx=5,pady=5)
        
    def OpenLink(self):
        webbrowser.open("http://"+self.ip+":8888")
    def add(self,id,name,type):
        return self.tree.insert('', 'end', text=id, values=(name,type))
        #self.Lb1.insert('end', name)
        
    def remove(self,nb):
        self.tree.delete(nb)
        #self.Lb1.delete(nb)
    
    def quit_win(self):
        self.destroy()
        
class QuitPopup(Tk):
    """ Mon programme graphique utilisant Python3 et Tkinter """

    def __init__(self):
        Tk.__init__(self)	# On dérive de Tk, on reprend sa méthode d'instanciation
        self.wm_title("Ardulan Server")
        self.iconbitmap(default='ardulan.ico')
        #self.attributes("-toolwindow", 2)
        self.resizable(0,0)
        self.overrideredirect(True)
        self.attributes("-topmost", 1)
        self.lb = Label(self, text="ArduiLan Stopping ...")
        self.lb.pack(padx=40,pady=40)
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        
    def test(self):
        self.after(5000, self.destroy)

class QuitPopup_d(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.q = QuitPopup()
        
    def run(self):
        self.q.mainloop()
        
    def stop(self):
        self.q.destroy()
 
if(__name__ == '__main__'):
    #root = Tk()
    application = NetChooser(['127.0.0.1','192.168.1.50','10.5.0.96'])	# Instanciation de la classe
    #application.wait_window()
    application.mainloop()		# Boucle pour garder le programme en vie
    try:
        print "Selected=", application.network
    except:
        pass
    app = Main("127.0.0.1")
    app.add("Python","?","?")
    app.add("Perl","?","?")
    app.mainloop()
    q = QuitPopup()
    q.test()
    q.mainloop()
