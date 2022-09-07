import subprocess
import tkinter
import platform
import re
import json
import requests
from tkinter import *
from screeninfo import get_monitors

def add_package(parent,name="Lorem Ipsum",version="v2",description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc magna enim, commodo in mi et, tempus semper arcu. Aenean nec consequat neque. Maecenas bibendum imperdiet."):
    if len(name) > 17:
        name = name[:18]+"..."
    if len(description) > 92*2:
        description = description[:92*2]+"..."
    description = re.sub("(.{92})", "\\1\n", description, 0, re.DOTALL)
    frame = Frame(parent,width=600,background=Colors.Background,highlightbackground=Colors.Text,highlightthickness=1)
    frame.pack_propagate(0)
    label = Label(parent,text=name,background=Colors.Background,fg=Colors.Text,font=["Calibri",40])
    label.pack(anchor=NW)
    version = Label(parent,text=version,background=Colors.Background,fg="#999494",font=["Calibri",10])
    version.pack(anchor=NW)
    description = Label(parent,text=description,background=Colors.Background,fg=Colors.Text,font=["Calibri",10])
    description.pack(anchor=NW)
    frame.pack()
class ScrollFrame(tkinter.Frame):
    def __init__(self, parent,width=100,height=200):
        super().__init__(parent) # create a frame (self)

        self.canvas = tkinter.Canvas(self, borderwidth=0, background="#ffffff",width=width,height=height)          #place canvas on self
        self.viewPort = tkinter.Frame(self.canvas, background="#ffffff",width=width,height=height)                    #place a frame on the canvas, this frame will hold the child widgets 
        self.vsb = tkinter.Scrollbar(self, orient="vertical", command=self.canvas.yview) #place a scrollbar on self 
        self.canvas.configure(yscrollcommand=self.vsb.set)                          #attach scrollbar action to scroll of canvas

        self.vsb.pack(side="right", fill="y")                                       #pack scrollbar to right of self
        self.canvas.pack(side="left", fill="both", expand=True)                     #pack canvas to left of self and expand to fil
        self.canvas_window = self.canvas.create_window((4,4), window=self.viewPort, anchor="nw",            #add view port frame to canvas
                                  tags="self.viewPort")

        self.viewPort.bind("<Configure>", self.onFrameConfigure)                       #bind an event whenever the size of the viewPort frame changes.
        self.canvas.bind("<Configure>", self.onCanvasConfigure)                       #bind an event whenever the size of the canvas frame changes.
            
        self.viewPort.bind('<Enter>', self.onEnter)                                 # bind wheel events when the cursor enters the control
        self.viewPort.bind('<Leave>', self.onLeave)                                 # unbind wheel events when the cursorl leaves the control

        self.onFrameConfigure(None)                                                 #perform an initial stretch on render, otherwise the scroll region has a tiny border until the first resize

    def onFrameConfigure(self, event):                                              
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))                 #whenever the size of the frame changes, alter the scroll region respectively.

    def onCanvasConfigure(self, event):
        '''Reset the canvas window to encompass inner frame when required'''
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width = canvas_width)            #whenever the size of the canvas changes alter the window region respectively.

    def onMouseWheel(self, event):                                                  # cross platform scroll wheel event
        if platform.system() == 'Windows':
            self.canvas.yview_scroll(int(-1* (event.delta/120)), "units")
        elif platform.system() == 'Darwin':
            self.canvas.yview_scroll(int(-1 * event.delta), "units")
        else:
            if event.num == 4:
                self.canvas.yview_scroll( -1, "units" )
            elif event.num == 5:
                self.canvas.yview_scroll( 1, "units" )
    
    def onEnter(self, event):                                                       # bind wheel events when the cursor enters the control
        if platform.system() == 'Linux':
            self.canvas.bind_all("<Button-4>", self.onMouseWheel)
            self.canvas.bind_all("<Button-5>", self.onMouseWheel)
        else:
            self.canvas.bind_all("<MouseWheel>", self.onMouseWheel)

    def onLeave(self, event):                                                       # unbind wheel events when the cursorl leaves the control
        if platform.system() == 'Linux':
            self.canvas.unbind_all("<Button-4>")
            self.canvas.unbind_all("<Button-5>")
        else:
            self.canvas.unbind_all("<MouseWheel>")
class Colors:
    Background = "white"
    Text = "black"
    Seperator = "grey"
class Strings:
    search = 'Search'
    remove = 'Uninstall'
    #add space after serverfail string
    serverfail = "Sorry, getting description failed. "
def center(win):
    for m in get_monitors():
        if m.is_primary:
            mointor = m
            break
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = mointor.width // 2 - win_width // 2
    y = mointor.height // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()

# CODE STARTS HERE #
app = tkinter.Tk()
menu = tkinter.Frame(app,width=200, height=600,background=Colors.Background)
menu.pack_propagate(0)
photo = PhotoImage(file="logo.png")
Label(menu,image=photo,width=200,height=200,background=Colors.Background).pack()
serach = Entry(menu,background=Colors.Background).pack(fill=tkinter.X)
Button(menu,text=Strings.search,background=Colors.Background).pack(fill=tkinter.X)
app.geometry("800x600")
app.resizable(False, False)
menu.pack(side="left")
applist = ScrollFrame(app,600,600)
applist.pack()
app.title("pGUIp DEV")
for i in "urllib3==1.26\ncryptography==1.0".split("\n"):#subprocess.getoutput("python3 -m pip freeze").split("\n"):
    i = i.split("==")
    try:
        data = requests.get(f"https://pypi.org/pypi/{i[0]}/json").text
        data = json.loads(data)
        add_package(applist.viewPort,i[0],i[1],data["info"]["description"])
    except Exception as e:
        add_package(applist.viewPort,i[0],i[1],Strings.serverfail+str(e))

center(app)
app.mainloop()