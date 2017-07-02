import os, sys, random, glob
import cPickle as pickle

rootDir = os.getcwd()

gameD = {}
#Test
try:
    gameD = pickle.load( open( "rouletteConfig.pickle", "rb" ) )
except:
    pass

"""
for l in open("games/loc.txt").readlines():
    if not l[0] == '#':
        g,setting,tag = l.split("|")
        tag = tag.replace('\n','').replace('\r','').split(',')
        loc = "games/"+'/'.join(g.split("/")[:-1])
        exe = g.split("/")[-1]
        
        if exe == "nfba.exe":
            for rom in glob.glob(loc+"/ROMs/*"):
                exe = "nfba.exe "+'.'.join(rom.split('\\')[-1].split('.')[:-1])
                if not exe.split(' ')[1] == 'neogeo':
                    game[(loc,setting,exe)] = tag

                    
        elif exe == "zsnesw.exe":
            for rom in glob.glob(loc+"/roms/*"):
                exe = "zsnesw.exe ./roms/"+'.'.join(rom.split('\\')[-1].split('.'))
                game[(loc,setting,exe)] = tag        

                    
        else:
            game[(loc,setting,exe)] = tag
"""

def startGame(g):
    os.chdir(rootDir)
    config = gameD['game'][g][0]
    tags = gameD['game'][g][1]
    args = gameD['game'][g][2]
    player1 = gameD["controler"][0] + config
    player2 = gameD["controler"][1] + config
    
    if "blank" == config:
        print "\nWarning: This game may need manual configuration\n"
    
    if "vgm" in tags:
        print "\nWARNING: This needs to be set for both players to be keyboard in the configuration menue of this game\n"
    
    print g.split('\\')[-1]+args
    os.system(".\\utils\\xpadder\\Xpadder.exe %s %s"%(player1,player2))
    loc = "\\".join(g.split("\\")[:-1])+"\\"
    os.chdir(rootDir.replace('/','\\')+'\\'+loc.replace('/','\\'))
    os.system(g.split('\\')[-1]+" "+args)
    
    
def genList(played,tagS):    
    tag = [i for i in tagS if i != '']
    
    culled = []
    
    for g in gameD["game"]:
        if not g in played:
            good = 1
            for t in tag:
                if t[0] == '!':
                    t = t[1:]
                    if t in gameD["game"][g][1]:
                        good = 0
                        break
                else:
                    if not t in gameD["game"][g][1]:
                        good = 0
                        break
            if good:
                culled.append(g)
            
    return culled
        
    
    
def main():
    print "Welcome to poverty rulet!"
    help = """    g <[!]gametag> : play a random game! 
    i <[!]gametag>: info
    l <[!]gametag>: list games 
    t : list tags
    r: replay
    h: print help
    q : quit
    """
    print "Make sure xpadder is running!"
    played = []
    print help
    last = ""
    
    #@TODO start up xpadder automaticaly
    #os.system(".\\utils\\xpadder\\Xpadder.exe ")
    #os.system("utils\\xpadder\\Xpadder.exe")
    
    while(1==1):
        try:
            c = raw_input(">")
            
            if len(c) < 1:
                print help
            
            elif c[0] == "q":
                sys.exit(0)
                
            elif c[0] == "g":
                cul = genList(played,c.split(' ')[1:])
                if cul == []:
                    print "No more games of that type"
                else:
                    g = random.choice(cul)
                    last = g
                    played.append(g)
                    startGame(g)
                    
                    
            elif c[0] == "i":
                cul = genList(played,c.split(' ')[1:])
                print "Total   :",len(gameD["game"])
                print "Played  :",len(played)
                print "Selected:",len(cul)
                
                
            elif c[0] == "l":
                cul = genList(played,c.split(' ')[1:])
                if cul == []:
                    print "No more games of that type"
                for i in cul:
                    print i,"--",gameD["game"][i][1]
                    
                    
            elif c[0] == "t":
                tags = {}
                for i in gameD["game"]:
                    for t in gameD["game"][i][1]:
                        tags.setdefault(t,0)
                        tags[t] += 1
                        
                for i in tags:
                    print i,tags[i]
            
            elif c[0] == "r":
                if last == "":
                    print "No game played yet"
                else:
                    startGame(last)
                
            else:
                print help
        except Exception as e:
            print e
        
        
if __name__ == "__main__":
    main()
