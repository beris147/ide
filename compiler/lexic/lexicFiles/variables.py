from pathlib import Path
posinfile = ""
lineo = 0
TraceScan = ""
directory = ""
output = ""
file = ""
def init(dir, name, trace, out):
    global posinfile
    global TraceScan
    global directory
    global output
    global file
    global lineo
    lineo = 0
    posinfile = 0
    directory = dir
    file = directory+"\\"+name
    TraceScan = trace
    if trace:
        Path(directory+"\\compilador").mkdir(parents=True, exist_ok=True)
        output = open(out,"w+") if out else open(directory+"\\compilador\\listing.txt","w+")
   