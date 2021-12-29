import socket 
import select 
import sys 
from threading import Thread
from thread import *
from Tkinter import Tk, Canvas, Label, Frame, IntVar, Radiobutton, Button
from PIL import ImageTk
import math
from goompy import GooMPy
import csv


#Variables //////////////////////////////////////////////////////////////////////////////////
WIDTH = 800
HEIGHT = 500
LATITUDE  =  32.826869
LONGITUDE = -83.648404
ZOOM = 17
MAPTYPE = 'OSM'
_EARTHPIX = 268435456
_TILESIZE = 640
_PIXRAD = _EARTHPIX / math.pi
_DEGREE_PRECISION = 4
pixels_per_meter = 2**ZOOM / (156543.03392 * math.cos(math.radians(LATITUDE)))
R=6378137
HOST = '192.168.1.145' #Change for Router
PORT = 50000
BUFSIZ = 2048

#Binding Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("", PORT))
#server.listen(100)
list_of_clients = [] 

#Math Methods ///////////////////////////////////////////////////////////////////////////////
def _pixToDeg(pix,zoom):
    return pix * 2 ** (21 - zoom)

def _pixItLon(pix):
    distOfPix = 40075016.686000 * math.cos(LATITUDE)/((2 ** ZOOM)*_TILESIZE)
    distance = ((pix-320)*distOfPix)/(R*math.cos(math.pi*LATITUDE/180))
    lonSelected = LONGITUDE + (distance * 180/math.pi)
    return lonSelected

def _pixItLat(pix):
    distOfPix = 40075016.686000 * math.cos(LATITUDE)/((2 ** ZOOM)*_TILESIZE)
    distance = (pix-316)*distOfPix/R
    latSelected = LATITUDE + (distance *180/math.pi)
    return latSelected
#Start UI Class //////////////////////////////////////////////////////////////////////////////
class UI(Tk):

    def __init__(self):
        print("Initializing")
        
        Tk.__init__(self)

        self.geometry('%dx%d+500+500' % (WIDTH,HEIGHT))
        self.title('GooMPy')

        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT)

        self.canvas.pack()

        self.bind("<Key>", self.check_quit)
        self.bind('<B1-Motion>', self.drag)
        self.bind('<Button-1>', self.click)

        self.label = Label(self.canvas)

        self.radiogroup = Frame(self.canvas)
        self.radiovar = IntVar()
        self.maptypes = ['OSM', 'GoogleSatellite', 'Satellite']
        self.add_radio_button('OSM',  0)
        self.add_radio_button('GoogleSatellite', 1)
        self.add_radio_button('Satellite',    2)

        self.zoom_in_button  = self.add_zoom_button('+', +1)
        self.zoom_out_button = self.add_zoom_button('-', -1)

        self.zoomlevel = ZOOM

        maptype_index = 0
        self.radiovar.set(maptype_index)

        self.goompy = GooMPy(WIDTH, HEIGHT, LATITUDE, LONGITUDE, ZOOM, MAPTYPE)

        self.restart()

    def add_zoom_button(self, text, sign):

        button = Button(self.canvas, text=text, width=1, command=lambda:self.zoom(sign))
        return button

    def reload(self):

        self.coords = None
        self.redraw()

        self['cursor']  = ''


    def restart(self):

        # A little trick to get a watch cursor along with loading
        self['cursor']  = 'watch'
        self.after(1, self.reload)

    def add_radio_button(self, text, index):

        maptype = self.maptypes[index]
        Radiobutton(self.radiogroup, text=maptype, variable=self.radiovar, value=index, 
                command=lambda:self.usemap(maptype)).grid(row=0, column=index)

    def click(self, event):

        self.coords = event.x, event.y
        print("X: " + str(event.x))
        #print(event.x)
        print("Y: " + str(event.y))
        #print(event.y)
        #print("\nLong: ")
        #print(_pixItLon(event.x))
        #print("\nLLat: ")
        #print(_pixItLat(event.y))
        #coods = str(_pixItLat(event.y)) + ';' + str(_pixItLon(event.x))
        coods = str(event.x-315) + ";" + str(309-event.y)
        coods = coods.encode()
        broadcast(coods,HOST)

    def drag(self, event):

        #self.goompy.move(self.coords[0]-event.x, self.coords[1]-event.y)
        #self.image = self.goompy.getImage()
        #self.redraw()
        self.coords = event.x, event.y
        #print("X: " + event.x + "\nY:: " + event.y)

    def redraw(self):

        self.image = self.goompy.getImage()
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.label['image'] = self.image_tk

        self.label.place(x=0, y=0, width=WIDTH, height=HEIGHT) 

        self.radiogroup.place(x=0,y=0)

        x = int(self.canvas['width']) - 50
        y = int(self.canvas['height']) - 80

        self.zoom_in_button.place(x= x, y=y)
        self.zoom_out_button.place(x= x, y=y+30)

    def usemap(self, maptype):

        self.goompy.useMaptype(maptype)
        self.restart()

    def zoom(self, sign):

        newlevel = self.zoomlevel + sign
        if newlevel > 0 and newlevel < 22:
            self.zoomlevel = newlevel
            self.goompy.useZoom(newlevel)
            self.restart()
                
    def check_quit(self, event):

        if ord(event.char) == 27: # ESC
            exit(0)
            
#END OF UI////////////////////////////////////////////////////////////////////////////////////////////////


#Server Methods //////////////////////////////////////////////////////////////////////////////////////////
def clientthread(conn, addr): 
  
    # sends a message to the client whose user object is conn 
    conn.send(addr[0])
    fieldnames = ['Latitude', 'Longitude', 'TimeStamp']
    with open('TestData' + addr[0] + '.csv', mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'Latitude': 123456, 'Longitude': 123456, 'TimeStamp': 123456})

    while True: 
            try: 
                message = conn.recv(2048)
                message = message.decode()
                print(message)
                temp_data = message.split(";")





                with open('TestData' + addr[0] + '.csv', mode='a') as csv_file:
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                    writer.writerow({'Latitude': temp_data[0], 'Longitude': temp_data[1], 'TimeStamp': temp_data[2]})
                # Calls broadcast function to send message to all
                message_to_send = "<" + addr[0] + "> " + message
                message_to_send = message_to_send.encode()
                broadcast(message_to_send, conn)
  
            except:
                continue
  
"""Using the below function, we broadcast the message to all 
clients who's object is not the same as the one sending 
the message """
def broadcast(message, connection):
    #print ("Enter Broadcast")
    for clients in list_of_clients: 
        if clients!=connection: 
            try:
                print(message)
                #print(clients)
                clients.send(message) 
            except: 
                clients.close()
  
                # if the link is broken, we remove the client 
                #remove(clients)
  
"""The following function simply removes the object 
from the list that was created at the beginning of  
the program"""
def remove(connection): 
    if connection in list_of_clients: 
        list_of_clients.remove(connection)

def accept_connections():
    """Sets up handling for incoming clients."""
    while True:
        conn, addr = server.accept() 
        list_of_clients.append(conn)
        print addr[0] + " connected"
        #conn.send(bytes("S;", "utf8"))
        Thread(target=clientthread, args=(conn,addr)).start()

#Main ////////////////////////////////////////////////////////////////////////
if __name__ == "__main__":
    #Server listens for 5 active connections
    server.listen(5)
    print("Waiting to connect to swarm....")
    accept_thread = Thread(target=accept_connections)
    accept_thread.start()
    UI().mainloop()

#Close the connections`
server.close() 



