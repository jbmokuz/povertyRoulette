import cPickle as pickle
import os, sys
from glob import glob
rootDir = os.getcwd()

#gameD = {}
#gameD["game"] = {}
#gameD["config"] = ["blank","standard","4button","VGM"]
#gameD["controler"] = ["blackps2","blueps2"]

try:
    gameD = pickle.load( open( "rouletteConfig.pickle", "rb" ) )
except:
    pass

    
reconfigBool = 0 


def startGame(g):
    os.chdir(rootDir)
    loc = "\\".join(g.split("\\")[:-1])+"\\"
    os.chdir(rootDir.replace('/','\\')+'\\'+loc.replace('/','\\'))
    os.system(g.split('\\')[-1])
    os.chdir(rootDir)

def inputGetter(message,l):
    print message
    for i,j in enumerate(l):
        print i,j
    
    select = raw_input(">")
    print select.lower()
    if select.lower() == "exit" or select.lower() == "quit":
        print "exiting"
        #@TODO Close the pickle!
        sys.exit()
    try:
        select = int(select)
        #print "You got",l[select]
    except:
        print "Invalid input. Not adding game to list."
        return ""
    return l[select]

def configGames():
    for a,b,c in os.walk(".\\games"):
        
        if not a in gameD["game"] and reconfigBool == 0:
            exes = []
            for f in c:
                if f[-3:].lower() == "exe": #and not "config" in f.lower() and not "uninst" in f.lower() and not "update" in f.lower():
                    exes.append(a+"\\"+f)
            if exes != [] and not bool(set(exes) & set(gameD["game"].keys())):
                
                #Get Game Exe
                gameLoc = inputGetter("Select Game",exes)
                if gameLoc != "":
                    
        
                    print "Open game? (y = yes) (c = open other exe for config)"
                    reap = raw_input(">").lower()
                    if reap == "y":
                        startGame(gameLoc)
                    elif reap == "c":
                        configLoc = inputGetter("Select Config exe",exes)
                        startGame(configLoc)
                   
                  
                    #Get game config
                    confz = inputGetter("Select Configuration",gameD["config"])

                    if confz != "":
                        print gameLoc
                        print "Tags? (comma seperated)"
                        tags = raw_input(">").lower()
                        if tags != "":
                            tags = [z for z in tags.split(',')]
                        else:
                            tags = []
                        
                        gameD["game"].setdefault(gameLoc,["",[],""])
                        gameD["game"][gameLoc][0] = confz
                        gameD["game"][gameLoc][1] = tags
                        pickle.dump(gameD, open("rouletteConfig.pickle", "wb" ) )
                        

            #print gameD
        
def changeConrolers():
    gameD["controler"][0] = raw_input("Controler 1:")
    gameD["controler"][1] = raw_input("Controler 2:")
    pickle.dump(gameD, open("rouletteConfig.pickle", "wb" ) )
    
#@WARNING This assumes there is a roms dir in the directory of the exe that has all the roms
#@WARNING this assumes the exe is in the first level directory or the emulator folder
def configEmulator():
    emulatorDir = inputGetter("pick and emulator directory",glob(".\\emulators\\*"))
    emulatorExe = inputGetter("select the emulator exe",glob(emulatorDir+"\\*.exe"))
    type = inputGetter("emulator type?",['dir','name'])
    
    for rom in glob(emulatorDir+"\\roms\\*"):
        fullexe = ""
    
        if type == 'dir':
            fullexe = emulatorExe+ ' "roms/'+rom.split("\\")[-1]+'"'
        elif type == 'name':
            fullexe = emulatorExe+" "+rom.split("\\")[-1].split('.')[0]
        else:
            print "HOW?!"
        
        
        if not fullexe in gameD["game"] and reconfigBool == 0:
            print fullexe
            #Get game config
            
            print "Open game? (y = yes)"
            reap = raw_input(">").lower()
            if reap == "y":
                startGame(fullexe)
            
            
            confz = inputGetter("Select Configuration",gameD["config"])
            
            if confz != "":
                print fullexe
                print "Tags? (comma seperated)"
                tags = raw_input(">").lower()
                if tags != "":
                    tags = [z for z in tags.split(',')]
                else:
                    tags = []
                
                gameD["game"].setdefault(fullexe,["",[],""])
                gameD["game"][fullexe][0] = confz
                gameD["game"][fullexe][1] = tags
                pickle.dump(gameD, open("rouletteConfig.pickle", "wb" ) )
                
if __name__ == "__main__":
    print "Welcome to roulette configuration!"
    print "g: configure new games"
    print "c: configure controlers"
    print "e: configure emulators"
    
    select = raw_input(">").lower()
    if select == "g":
        configGames()
    if select == "c":
        changeConrolers()
    if select == "e":
        configEmulator()
    
