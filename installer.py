import subprocess
import pymsgbox
def install(name:str,version):
    if version=="latest":
        status= subprocess.getstatusoutput("pip install "+name)
    else:
        status= subprocess.getstatusoutput("pip install "+name+"=="+version)
    if status[0]!=0:
        pymsgbox.alert("PIP Error Code: "+str(status[0])+"\n\n"+status[1][:3000].replace("\n","\\n"),"pGUIp DEV")
def uninstall(name:str):
    status= subprocess.getstatusoutput("pip uninstall -y "+name)
    pymsgbox.alert(status)
    if status[0]!=0: pymsgbox.alert("PIP Error Code: "+str(status[0])+"\n\n"+status[1][:3000].replace("\n","\\n"),"pGUIp DEV")
    return
def update(name:str,version):
    pass
def reinstall(name:str,version):
    pass