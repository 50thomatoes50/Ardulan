#!/usr/bin/env python

from threading import Thread





            
if(__name__ == '__main__'):
    import webbrowser
    web = WebServer()
    webbrowser.open("http://127.0.0.1:8888")
    web.start()