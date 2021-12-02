import re 
import pandas as pd
from fuzzywuzzy import fuzz
import webbrowser
import urllib.request
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def add_done_anime(df):
    rfile = open("done.txt")
    possible = []
    s = input("Enter anime name : ")
    for k in list(df['title']):
        
        temp = fuzz.partial_ratio(s.lower(), k.strip().lower()) 
        if temp > 99:
            possible.append((temp, k))
    
    print()

    found =  True

    if len(possible)==0:
        print("\033[1;36mNo results found for the anime you watched! (check Japanese name once) :(")
        print()
        print("But still adding it to the list..uwu\033[0m")
        print()
        found = False
    
    tar = ""
    n = 0
    
    if found:
        for i in range(len(possible)):
            print(str(i+1) + " : " + possible[i][1])

        print("\033[1;33m------------------------------------------------------------------")
        n = int(input("Enter the search result number (-1 if not present): "))
        print("------------------------------------------------------------------\033[0m")
    
    
        if n!=-1:
        
            decl = (df.loc[df['title'] == possible[n-1][1]])
            tar= str(list(decl['title'])[0])
    
    if not found or n == -1:
        tar = s



    toWrite = True

    watch_num = 0
    bakup = []

    for line in rfile.readlines():
        x = line.split(",")

        if x[0]==tar:
            watch_num =  int(x[2])
        else:
            bakup.append(line)
    
    print()

    print("\033[1;36mNumber of episodes watches of " + s + " are " + str(watch_num) + "\033[0m")

    print()

    x = input("Enter \"m new ep no.\" to modify.. (ex. m 14) : ").strip().split()
    file = open("done.txt", "w")
    for i in bakup:
        file.write(i)
    if x[0] =="m":
        file.write(tar + "," + s + "," + str(x[1]) +"\n")
        print()
        print("\033[1;36mAnime added to your watchlist!\033[0m")


def show_done_anime():
    watchlist = open('done.txt')

    ancodes = []

    for line in watchlist.readlines():
        x = line.split(",")
        ancodes.append((x[0], x[2]))
    
    print()
    for i in range(len(ancodes)):
        print(str(i+1) + ") " + ancodes[i][0] + " : " + ancodes[i][1])
        print()

def add_anime(df):
    s = input("Enter anime name : ")
    file = open("watchlist.txt", "a")
    rfile = open("watchlist.txt")
    possible = []
    for k in list(df['title']):
        temp = fuzz.partial_ratio(s.lower(), k.strip().lower()) 
        if temp > 99:
            possible.append((temp, k))
    
    print()

    if len(possible)==0:
        print("\033[1;36mNo results found! :(")
        print()
        print("I suggest using the Japanese name of the anime :)\033[0m")
        print()
        return
    
    print()
    for i in range(len(possible)):
        print(str(i+1) + " : " + possible[i][1])
    

    print("\033[1;33m------------------------------------------------------------------")
    n = int(input("Enter the search result number you want to add to your watchlist (-1 if not present):  "))
    
    print("------------------------------------------------------------------\033[0m")

    if n == -1:
        print()
        print("\033[1;31mSorry this anime is not yet in our database!\033[0m")
        print()
        return
    decl = (df.loc[df['title'] == possible[n-1][1]])

    toWrite = True


    for line in rfile.readlines():
        x = line.split(",")
        if x[0]==str(list(decl['title'])[0]):
            print("\033[1;36mThis anime is already in your watchlist!\033[0m")
            toWrite = False
            break
    if toWrite:
        file.write(str(list(decl['title'])[0]) + "," + s + "\n")
        print("\033[1;36mAnime added to your watchlist!\033[0m")

def sort_by(df, crit):

    watchlist = open('watchlist.txt')

    ancodes = []

    for line in watchlist.readlines():
        x = line.split(",")
        ancodes.append((x[0], x[1]))
    
    fin = []
    for i in ancodes:

        td = df.loc[df['title'] == i[0].strip()]

        fin.append((float(list(td[crit])[0]), i[0].strip()))
    fin.sort()
    if crit=="score":
        fin.reverse()
    
    for i in range(len(fin)):
        print(str(i+1) + ". " + fin[i][1] + " (" + str(fin[i][0]) + ")")
        print()

def show_watchlist_chronological():
    watchlist = open('watchlist.txt')

    ancodes = []

    for line in watchlist.readlines():
        x = line.split(",")
        ancodes.append((x[0], x[1]))
    
    print()
    for i in range(len(ancodes)):
        print(str(i+1) + ". " + ancodes[i][0])
        print()

def display(df,where):
    watchlist = open('watchlist.txt')

    ancodes = []

    for line in watchlist.readlines():
        x = line.split(",")
        ancodes.append((x[0], x[1]))
    
    print()
    for i in range(len(ancodes)):
        print(str(i+1) + ". " + ancodes[i][0])
        print()  
    
    com = int(input("Which anime's MAL do you want to visit? , Enter the serial number : "))

    

    decl = (df.loc[df['title'] == ancodes[com-1][0]])

    if where =="mal":
        webbrowser.open("https://myanimelist.net/anime/" + str(list(decl['uid'])[0]))
    elif where =="watch":
        sitname = (re.sub(r'[^\w\s]', '', list(decl['title'])[0].lower()))
        webbrowser.open( "https://www1.gogoanime.cm/category/"+ (sitname.replace(" ", "-")))


df = pd.read_csv('animes.csv')
print()
print("\033[1;34mInstructions :\n")
print("\033[1;32m\"-a\" to add an anime to the watchlist!\n")
print("\"-sr\" to sort the watchlisted anime by any category!\n")
print("\"-d\" to display your watchlist!\n")
print("\"-aw\" to add an anime to the watched list!\n")
print("\"-dw\" to display your watched list!\n")
print("\"-ra\" to add multiple anime to the watchlist!\n")
print("\"-raw\" to add multiple anime to the watched list!\n\033[0m ")
print()
inp = input("=>")
print("-------------------------------------------------")
print()

if inp == "-a":
    
    add_anime(df)
elif inp == "-aw":
    add_done_anime(df)
elif inp== "-d":
    show_watchlist_chronological()
elif inp=="-dw":
    show_done_anime()
elif inp == "-sr":
    print()
    print("\033[1;33m\"r\" for ratings")
    print("\"p\" for popularity")
    print("\"rk\" for rank\033[0m")
    print()
    cat = input("Enter category : ")
    print()
    if cat=="r":
        sort_by(df, 'score')
    elif cat== "p":
        sort_by(df, 'popularity')
    elif cat =="rk":
        sort_by(df, 'ranked')
    else:
        print("\033[1;31mYou baka! This category does not exist! :3\033[0m")

elif inp == "-ra":
    n = int(input("Number of anime you want to add :"))
    print()
    for i in range(n):
        add_anime(df)
        print()
        print("------------------------------------------------------------------")
        print()
elif inp == "-raw":
    n = int(input("Number of anime you want to add :"))
    print()
    for i in range(n):
        add_done_anime(df)
        print()
        print("------------------------------------------------------------------")
        print()
else:
    print("\033[1;31mNO SUCH FLAG ! You SAKURA ass bitch!\033[0m")




