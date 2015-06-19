#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import time, struct
import array

class MEGA():
    def __init__(self,id,ip,UDP_PORT):
        self.id = id
        self.idgui = ''
        self.ip = ip
        self.type = "Arduino MEGA (2560)"
        self.stype = "MEGA"
        self.port = UDP_PORT
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.s.settimeout(1)
        self.input = {}
        self.decode = struct.Struct('6B')
        self.stats = array.array('B',[85]*9)
        self.statactu = False
        self.encode = struct.Struct('9B')
    def actu(self):
        self.s.sendto("Actu", (self.ip, self.port))
        try:
            data , addr = self.s.recvfrom(128)
            if data == "ACK":
                time.sleep(0.05)
                if self.statactu:
                    print "actu stat"
                    self.s.sendto("st"+self.encode.pack(*self.stats)+self.decode.pack(*self.input), (self.ip, self.port))
                    self.statactu = False
                    time.sleep(0.05)
                self.s.sendto("in", (self.ip, self.port))
                data , addr = self.s.recvfrom(128)
                self.input = self.decode.unpack(data)
                return 1
        except socket.timeout:
            return 0
        return 0
    def quit(self):
        print "kick ", self.ip
        self.s.sendto("qr", (self.ip, self.port))
        self.s.close()
        
    def stat(self, pin, mode, data):
        self.statactu = True
        pin = int(pin)
        mode = int(mode)
        data = int(data)
        if pin < 10:
            pin -=2
        elif pin > 20:
            pin -=15
        """arrnb = int(pin/2)
        if pin%2:
            self.stats[arrnb] = self.stats[arrnb] & 240 | mode
        else:
            self.stats[arrnb] = mode << 4 | self.stats[arrnb] & 15"""
        arrnb = int(pin/4)
        bitpos=pin
        while bitpos >3:
            bitpos-=4
        if bitpos==0:
            self.stats[arrnb] = self.stats[arrnb] & 252 | mode
        elif bitpos==1:
            self.stats[arrnb] = mode << 2 | self.stats[arrnb] & 243
        elif bitpos==2:
            self.stats[arrnb] = mode << 4 | self.stats[arrnb] & 207
        elif bitpos==3:
            self.stats[arrnb] = mode << 6 | self.stats[arrnb] & 63
        print "Stat",pin, mode, data
        print self.stats
        
class LEONARDO():
    def __init__(self,ip,data):
        self.ip = ip
        self.data = data