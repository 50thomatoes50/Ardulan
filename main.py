#!/usr/bin/env python
# -*- coding: utf-8 -*-
from threading import Thread
import time
import socket
import gui
import arduino
import tornado.ioloop
import tornado.web
import os
import sys

version = "0.0.1"
Servname = "Arduilan "+version+" | TornadoServer/4.0.2"

dir_=""
if getattr(sys, 'frozen', False):
    # frozen
    dir_ = os.path.realpath(sys.executable)
else:
    # unfrozen
    dir_ = os.path.realpath(__file__)

class WebServer(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.application = tornado.web.Application([
            (r"/", WebIndex),
            (r"/arduino", Webduino),
            (r"/mega", WebduinoMega),
            (r"/([a-zA-Z\-0-9\.:,_]+)", WebFile),
            (r"/img/([a-zA-Z\-0-9\.:,_]+)", WebFile),
            ])
        self.webrunning = True

    def run(self):
        self.application.listen(8888)
        tornado.ioloop.IOLoop.instance().start()
        while(self.webrunning):
            pass
    
    def stop(self):
        self.webrunning = False
        tornado.ioloop.IOLoop.instance().stop()

class WebIndex(tornado.web.RequestHandler):
    def get(self):
        global Servname
        self.set_header('Server', Servname)
        f = open(os.path.dirname(os.path.abspath(dir_))+"\\html\\index_header.html", 'r')
        test = f.read()
        self.write(test)
        f.close()
        
        for cl in manage.clients:
            if cl.stype == "MEGA":
                self.write("\n<tr><td><a href='mega?id="+cl.id+"'>"+cl.id+"</a></td><td><a href='mega?id="+cl.id+"'>"+cl.ip+"</a></td><td>"+cl.type+"</td></a></tr>")
            else:
                self.write("\n<tr><td>"+cl.id+"</td><td>"+cl.ip+"</td><td>Inconnu : "+cl.type+" ("+cl.stype+")</td></tr>")

        
        f = open(os.path.dirname(os.path.abspath(dir_))+"\\html\\index_footer.html", 'r')
        test = f.read()
        self.write(test)
        f.close()

class Webduino(tornado.web.RequestHandler):
    def get(self):
        global Servname, manage
        self.set_header('Server', Servname)
        try:
            #self.write("input=")
            #self.write(manage.clients[0].input)
            #self.write("<br>")
            for cl in manage.clients:
                if cl.id == self.get_argument("id"):
                    self.write(','.join(map(str,cl.input)))
                    self.write("|")
                    self.write(','.join(map(str,cl.stats)))
                    return
                self.write("id not found")
                    
        except Exception as inst:
            #self.write("truc?<br>")
            self.write(str(inst.args))
            self.flush()
    def post(self):
        global Servname
        self.set_header('Server', Servname)
        """self.write(self.get_argument("ard", default="?"))
        self.write("<br>\n")
        self.write(self.get_argument("pin", default="?"))
        self.write("<br>\n")
        self.write(self.get_argument("mode", default="?"))
        self.write("<br>\n")
        self.write(self.get_argument("data", default="?"))"""
        if(manage.stat(self.get_argument("ard"),self.get_argument("pin"),self.get_argument("mode"),self.get_argument("data", default="0"))):
            self.write("isok\n")
        else:
            self.write("nope!!!")
        
     
class WebduinoMega(tornado.web.RequestHandler):
    def get(self):
        global udpthread, Servname
        self.set_header('Server', Servname)
        f = open(os.path.dirname(os.path.abspath(dir_))+"\\html\\mega.html", 'r')
        test = f.read()
        self.write(test)
        f.close()

class WebFile(tornado.web.RequestHandler):
    def get(self, filename):
        #print "WebFile:"+filename
        global Servname
        self.set_header('Server', Servname)
        if filename[len(filename)-4:] == ".ico":
            self.set_header('Content-Type', "image/x-icon")
        elif filename[len(filename)-4:] == ".svg":
            self.set_header('Content-Type', "image/svg+xml")
        
        if filename[len(filename)-4:] == ".svg":
            filepath = os.path.dirname(os.path.abspath(dir_))+"\\html\\img\\"+filename
        else:
            filepath = os.path.dirname(os.path.abspath(dir_))+"\\html\\"+filename
        #print filepath    
        if os.path.isfile(filepath):
            f = open(filepath, 'r')
            test = f.read()
            self.write(test)
        else:
            self.set_header('Content-Type', "text/html")
            print "404 not found : "+filepath
            self.write("<h1>Not found</h1><address>"+filepath)
            self.set_status(404, reason="<h1>Not found</h1><address>"+filepath)
            

class UDPBroadcast(Thread):
    """Outgauge UDP Server thread class"""
     
    def __init__(self, UDP_IP, UDP_PORT = 5050):
        Thread.__init__(self)
        self.Udpbwork = True
        self.ip = UDP_IP
        self.ipb = self.getbroadcastip(self.ip)
        self.port = UDP_PORT
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.s.settimeout(2)
        print "UDPBroadcast started at ",self.ip,":",self.port
          
    def run(self):
        while self.Udpbwork:
            #self.s.sendto(self.ip, ("<broadcast>", self.port))
            self.s.sendto("Ardulan1", (self.ipb, self.port))
            try:
                data , addr = self.s.recvfrom(128)
                #print("received echo: ", data)
                #print("received at: " , addr )
                print "Arduino a répondu"
                try:
                    truc = data.split("!")
                except:
                    print("Can't parse data value from arduino : " + data)
                    break
                manage.add(addr[0],addr[1],truc[0],truc[1])
                #time.sleep(1)
            except socket.timeout:
                pass

            
    def getbroadcastip(self, ip):
        data = ip.split('.')
        return data[0]+"."+data[1]+"."+data[2]+".255"

class Gestionnaire(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.clients= []
        self.Gest = True
        
    def add(self,ip,port,ard_type,id):
        if ard_type == "MEGA":
            self.clients.append(arduino.MEGA(id,ip,port))
            self.clients[len(self.clients)-1].idgui = app.add(id,ip,ard_type)
        else:
            print "Unknow arduino type @",ip," type:",ard_type
        
    def run(self):
        while self.Gest:
            for i,client in enumerate(self.clients):
                if not client.actu():
                    app.remove(client.idgui)
                    print "Arduino déconnecté ",client.ip
                    self.clients.remove(client)
            time.sleep(2)
        for client in self.clients:
            client.quit()
            
    def stat(self,id, pin, mode, data):
        for c in self.clients:
            if c.id == id:
                c.stat(pin,mode,data)
                return 1
        return 0
            
if __name__ == '__main__':
    ip = socket.gethostbyname(socket.gethostname())
    ips = []
    if(ip == '127.0.0.1'):
        data = socket.gethostbyname_ex(socket.gethostname())
        ipfound = False
        for i in data[2]:
            if i != '127.0.0.1':
                if not ipfound:
                    ip = i
                    ipfound = True
                if ipfound:
                    ips.append(i)
        if ipfound:
            ips.append(ip)
    if len(ips):
        nc = gui.NetChooser(ips)
        nc.mainloop()
        udpthread = UDPBroadcast(nc.network)
    else:
        udpthread = UDPBroadcast(ip)
        
    app = gui.Main(ip)
    manage = Gestionnaire()
    manage.start()
    udpthread.start()
    web = WebServer()
    web.start()
    #time.sleep(10)
    app.mainloop()
    #popup = gui.QuitPopup_d()
    #popup.start()
    web.stop()
    udpthread.Udpbwork = False
    manage.Gest = False
    web.join()
    udpthread.join()
    manage.join()
    print "Au revoir"
    #popup.stop()
    #popup.join()