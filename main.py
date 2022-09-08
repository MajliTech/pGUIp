import subprocess
import tkinter
import pymsgbox
import platform
import re
import json
import requests
import installer as pipings
from tkinter import *
from elevate import elevate
from screeninfo import get_monitors
from PIL import Image,ImageTk
def gpi(name,vers):
    global installed
    if vers==None:
        try:
            vers = installed[name]
        except: 
            pass
    root = Tk()
    root.geometry("600x400")
    root.title("pGUIp DEV - "+name[:16]+"...")
    root.resizable(False, False)
    root.configure(background=Colors.Background)
    Label(root,text=name,font=["Calibri",30],background=Colors.Background,fg=Colors.Text).pack(anchor=NW)
    try:
        data = requests.get(f"https://pypi.org/pypi/{name}/json").json()
        data["info"]
    except:
        root.destroy()
        pymsgbox.alert(Strings.serverfail,"pGUIp")
        return 
    versions = Label(root,text=Strings.version_onserver+data["info"]["version"],background=Colors.Background,fg="#999494",font=["Calibri",10])
    if not vers==None:
        versionl = Label(root,text=str(Strings.version_local)+str(vers),background=Colors.Background,fg="#999494",font=["Calibri",10])
        versionl.pack(anchor=NW)
    versions.pack(anchor=NW)
    f = ScrollFrame(root,packpropagate=False,width=600,height=200)
    Label(f.viewPort,text=data["info"]["description"],background=Colors.Background,fg=Colors.Text).pack(anchor=NW)
    rel = ["latest"]
    for i in data["releases"]:
        rel.append(i)
    reles = StringVar(root)
    reles.set(rel[0])
    opmenu = OptionMenu(root,reles,*rel)
    
    f.pack(anchor=NW,expand=Y)
    if vers==None: Button(root,text=Strings.install,background="white",command=lambda: pipings.install(name,reles.get())).pack()
    else:
        Button(root,text=Strings.remove,background="white",command=lambda: rad(pipings.uninstall,root,name)).pack()
        Button(root,text=Strings.update,background="white",command=lambda: rad(pipings.update,root,name,reles.get())).pack()
    opmenu.pack()
def rad(command,window,*args):
    command(*args)
    window.destroy()
def search(name):
    data = requests.get(f"https://pypi.org/pypi/{name}/json").json()
    try:
        data["info"]
    except:
        pymsgbox.alert(Strings.serverfail,"pGUIp")
        return 
    gpi(name,None)
def el():
    app.destroy()
    with open(__file__) as f:
        elevate(lambda: exec(f.read()))
def add_package(parent,name="Lorem Ipsum",version="v2",description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc magna enim, commodo in mi et, tempus semper arcu. Aenean nec consequat neque. Maecenas bibendum imperdiet."):
    if len(name) > 17:
        name = name[:18]+"..."
    description = re.sub("(.{92})", "\\1\n", description, 0, re.DOTALL)
    frame = Frame(parent,width=600,background=Colors.Background,highlightbackground=Colors.Text,highlightthickness=1)
    frame.pack_propagate(0)
    label = Label(parent,text=name,background=Colors.Background,fg=Colors.Text,font=["Calibri",40])
    label.pack(anchor=NW)
    versionss = Label(parent,text=version,background=Colors.Background,fg="#999494",font=["Calibri",10])
    versionss.pack(anchor=NW)
    description = Label(parent,text=description,background=Colors.Background,fg=Colors.Text,font=["Calibri",10])
    description.pack(anchor=NW)
    butt = Button(parent,text=Strings.more,command=lambda: gpi(name,version),background=Colors.Background,fg=Colors.Text,width=20)
    butt.pack(anchor=NW)
    frame.pack()
class ScrollFrame(tkinter.Frame):
    def __init__(self, parent,width=100,height=200,packpropagate=False):
        super().__init__(parent) # create a frame (self)
        if packpropagate: 
            self.canvas = tkinter.Canvas(self, borderwidth=0, background="#ffffff")          #place canvas on self
            self.viewPort = tkinter.Frame(self.canvas, background="#ffffff")  
        else:
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
    search = 'Show'
    remove = 'Uninstall'
    #add space after serverfail string
    serverfail = "Sorry, getting description failed. "
    more = "More"
    # After version add :
    version_onserver = "Latest: "
    version_local = "Installed: "
    install = "Install"
    update = "Update"
    elevate = "Re-run as admin/root"
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
wait = Tk()
wait.title("pGUIp DEV")
wait.geometry("800x450")
wait.overrideredirect(True)
wait.configure(background=Colors.Background)
ima = Image.open("splash.png").resize((800,450))
splash = ImageTk.PhotoImage(master=wait,image=ima)
Label(wait,image=splash,background=Colors.Background).pack()
center(wait)
wait.update()
app = tkinter.Tk()
app.title("pGUIp DEV")
menu = tkinter.Frame(app,width=200, height=600,background=Colors.Background)
menu.pack_propagate(0)
photo = PhotoImage(master=app,file="logo.png")
Label(menu,image=photo,width=200,height=200,background=Colors.Background).pack()
serach = Entry(menu,background=Colors.Background)
serach.pack(fill=tkinter.X)
Button(menu,text=Strings.search,background=Colors.Background,command=lambda: search(serach.get())).pack(fill=tkinter.X)
Button(menu,text=Strings.elevate,background=Colors.Background,command=lambda: el()).pack(fill=tkinter.X)
app.geometry("800x600")
app.resizable(False, False)
menu.pack(side="left")
applist = ScrollFrame(app,600,600)
applist.pack()
installed = {}


for i in "urllib3==1.26\ncryptography==1.0\n838==ooo".split("\n"):#subprocess.getoutput("python3 -m pip freeze").split("\n"):
    i = i.split("==")
    installed[i[0]] = i[1]
    try:
        data = requests.get(f"https://pypi.org/pypi/{i[0]}/json").text
        data = json.loads(data)
        add_package(applist.viewPort,i[0],i[1],data["info"]["summary"])
    except Exception as e:
        add_package(applist.viewPort,i[0],i[1],Strings.serverfail+str(e))

center(app)
wait.destroy()
app.mainloop()