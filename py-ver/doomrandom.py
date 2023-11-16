# Doom Randomizer v1.02
# Personal Project focused on creating a customizable randomizer for Doom

import os, pickle, random
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno

FONT = ("Fixedsys", 16)

dataFile = "doomrandom.dat"
path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname("doomrandom.py")))

WADList = []
playstyleList = []
loadoutList = []
downloadList = []


class StorageData:
    global WADList
    global playstyleList
    global loadoutList
    global downloadList
    
    if not os.path.isfile(dataFile):
        if dataFile not in path:
            with open(dataFile, "wb") as f:
                pickle.dump(WADList, f)
                pickle.dump(playstyleList, f)
                pickle.dump(loadoutList, f)
                pickle.dump(downloadList, f)
                f.close()
    
    with open(dataFile, "rb") as f:
        WADList = pickle.load(f)
        playstyleList = pickle.load(f)
        loadoutList = pickle.load(f)
        downloadList = pickle.load(f)
        f.close()


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
        self.winfo_toplevel().title("Doom Randomizer")

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.frames = {}

        for F in (MainFrame, WADs, Playstyle, Loadout, DownloadWADs):
            frame = F(container, self)
            self.frames[F] = frame

            frame.grid(row = 0, column = 0, sticky = "NEWS")

        self.showFrame(MainFrame)

    def showFrame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
                

class MainFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text = "Welcome to Doom Randomizer!", font = FONT)  # Creates text
        label.grid(row = 0, column = 2, padx = 10, pady = 10)
        
        def randomize():
            result = ""
            resultField.configure(state = "normal")
            resultField.delete(1.0, "end")
            if WADList or playstyleList or loadoutList:
                result += str("WAD: " + random.choice(WADList) +
                              "\nPlaystyle: " + random.choice(playstyleList) +
                              "\nLoadout: " + random.choice(loadoutList))
                resultField.insert(1.0, result)
            elif not WADList or not playstyleList or not loadoutList:
                resultField.insert(1.0, "There are empty lists! Result unavailable.")
            else:
                resultField.insert(1.0, "Wait, what just happened? There maybe be an error in the code.")
            resultField.configure(state = "disabled")
            
        def download():
            result = ""
            resultField.configure(state="normal")
            resultField.delete(1.0, "end")
            if downloadList:
                result += str("Download: " + random.choice(downloadList))
                resultField.insert(1.0, result)
            elif not downloadList:
                resultField.insert(1.0, "Download list is empty! Result unavailable.")
            else:
                resultField.insert(1.0, "Wait, what just happened? There maybe be an error in the code.")
            resultField.configure(state="disabled")

        def confirmExit():
            answer = askyesno(title = 'Confirmation',
                              message = 'Are you sure you want to exit?')
            if answer is True:
                with open(dataFile, "wb") as f:
                    pickle.dump(WADList, f)
                    pickle.dump(playstyleList, f)
                    pickle.dump(loadoutList, f)
                    pickle.dump(downloadList, f)
                    f.close()
                exit()

        buttonWAD = ttk.Button(self, text = "WADs", command = lambda : controller.showFrame(WADs))
        buttonWAD.grid(row = 1, column = 1, padx = 10, pady = 10)

        buttonPlay = ttk.Button(self, text = "Playstyle", command = lambda : controller.showFrame(Playstyle))
        buttonPlay.grid(row = 1, column = 2, padx = 20, pady = 10)

        buttonLoad = ttk.Button(self, text = "Loadout", command = lambda : controller.showFrame(Loadout))
        buttonLoad.grid(row = 1, column = 3, padx = 30, pady = 10)

        buttonDownload = ttk.Button(self, text="Download WADs", command = lambda: controller.showFrame(DownloadWADs))
        buttonDownload.grid(row=2, column=3, pady=10)

        buttonRandom = ttk.Button(self, text = "RANDOMIZE", command = lambda : randomize())
        buttonRandom.grid(row = 2, column = 1, padx = 20, pady = 10)
        
        buttonChooseDownload = ttk.Button(self, text = "DOWNLOAD", command = lambda : download())
        buttonChooseDownload.grid(row = 2, column = 2, pady = 10)

        resultField = tk.Text(self, width = 40, height = 5, state = 'disabled', wrap = "word")
        resultField.grid(row = 3, column = 2, padx = 10, pady = 10)
        
        buttonExit = ttk.Button(self, text = "Exit", command = lambda : confirmExit())
        buttonExit.grid(row = 3, column = 3)


class WADs(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text = "List of WADs", font = FONT)
        label.place(x = 220, y = 10)
            
        buttonBack = ttk.Button(self, text = "Back", command = lambda : controller.showFrame(MainFrame))
        buttonBack.place(x = 10, y = 54)
        
        inputField = tk.Text(self, width = 20, height = 5)
        inputField.place(x = 25, y = 100)

        listField = tk.Listbox(self, width = 27, height = 5, selectmode = "multiple")
        listField.place(x = 380, y = 100)
        listField.insert("end", *WADList)

        def addWAD():
            moveList = []
            WADText = inputField.get(1.0, "end-1c")
            if WADText:
                line = WADText.split("\n")
                for l in line:
                    WADList.append(l)
                for l in line:
                    moveList.append(l)
                listField.insert("end", *moveList)
                inputField.delete(1.0, "end")

        def deleteWAD():
            select = listField.curselection()
            for i in select[::-1]:
                listField.delete(i)
                WADList.remove(WADList[i])

        def deleteAllWADs():
            answer = askyesno(title="Confirmation",
                              message="Are you sure you want to delete everything?")
            if answer is True:
                WADList.clear()
                listField.delete("0", "end")
        
        buttonAdd = ttk.Button(self, text = "Add WAD", command = lambda : addWAD())
        buttonAdd.place(x = 245, y = 100)
        
        buttonRemove = ttk.Button(self, text = "Delete WAD", command = lambda : deleteWAD())
        buttonRemove.place(x = 245, y = 125)
        
        buttonDelete = ttk.Button(self, text = "Delete All", command = lambda : deleteAllWADs())
        buttonDelete.place(x = 245, y = 150)
        

class Playstyle(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text = "List of Playstyles", font = FONT)
        label.place(x = 190, y = 10)
        
        def addPlaystyle():
            moveList = []
            playstyleText = inputField.get(1.0, "end-1c")
            if playstyleText:
                line = playstyleText.split("\n")
                for l in line:
                    playstyleList.append(l)
                for l in line:
                    moveList.append(l)
                listField.insert("end", *moveList)
                inputField.delete(1.0, "end")

        def deletePlaystyle():
            select = listField.curselection()
            for i in select[::-1]:
                listField.delete(i)
                playstyleList.remove(playstyleList[i])
        
        def deleteAllPlaystyles():
            answer = askyesno(title = "Confirmation",
                              message = "Are you sure you want to delete everything?")
            if answer is True:
                playstyleList.clear()
                listField.delete("0", "end")

        buttonBack = ttk.Button(self, text = "Back", command = lambda : controller.showFrame(MainFrame))
        buttonBack.place(x = 10, y = 54)

        inputField = tk.Text(self, width = 20, height = 5)
        inputField.place(x = 25, y = 100)

        listField = tk.Listbox(self, width = 27, height = 5, selectmode = "multiple")
        listField.place(x = 380, y = 100)
        listField.insert("end", *playstyleList)
        
        buttonAdd = ttk.Button(self, text = "Add Playstyle", command = lambda : addPlaystyle())
        buttonAdd.place(x = 243, y = 100)
        
        buttonRemove = ttk.Button(self, text = "Delete Playstyle", command = lambda : deletePlaystyle())
        buttonRemove.place(x = 238, y = 125)
        
        buttonDelete = ttk.Button(self, text = "Delete All", command = lambda : deleteAllPlaystyles())
        buttonDelete.place(x = 245, y = 150)


class Loadout(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text = "List of Loadouts", font = FONT)
        label.place(x = 200, y = 10)
        
        def addLoadout():
            moveList = []
            loadoutText = inputField.get(1.0, "end-1c")
            if loadoutText:
                line = loadoutText.split("\n")
                for l in line:
                    loadoutList.append(l)
                for l in line:
                    moveList.append(l)
                listField.insert("end", *moveList)
                inputField.delete(1.0, "end")
        
        def deleteLoadout():
            select = listField.curselection()
            for i in select[::-1]:
                listField.delete(i)
                loadoutList.remove(loadoutList[i])
        
        def deleteAllLoadouts():
            answer = askyesno(title = "Confirmation",
                              message = "Are you sure you want to delete everything?")
            if answer is True:
                loadoutList.clear()
                listField.delete("0", "end")

        buttonBack = ttk.Button(self, text = "Back", command = lambda : controller.showFrame(MainFrame))
        buttonBack.place(x = 10, y = 54)

        inputField = tk.Text(self, width = 20, height = 5)
        inputField.place(x = 25, y = 100)

        listField = tk.Listbox(self, width = 27, height = 5, selectmode = "multiple")
        listField.place(x = 380, y = 100)
        listField.insert("end", *loadoutList)
        
        buttonAdd = ttk.Button(self, text = "Add Loadout", command = lambda : addLoadout())
        buttonAdd.place(x = 244, y = 100)
        
        buttonRemove = ttk.Button(self, text = "Delete Loadout", command = lambda : deleteLoadout())
        buttonRemove.place(x = 239, y = 125)
        
        buttonDelete = ttk.Button(self, text = "Delete All", command = lambda : deleteAllLoadouts())
        buttonDelete.place(x = 245, y = 150)


class DownloadWADs(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="List of WADs to Download", font=FONT)
        label.place(x=220, y=10)

        buttonBack = ttk.Button(self, text="Back", command = lambda : controller.showFrame(MainFrame))
        buttonBack.place(x=10, y=54)

        inputField = tk.Text(self, width=20, height=5)
        inputField.place(x=25, y=100)

        listField = tk.Listbox(self, width=27, height=5, selectmode="multiple")
        listField.place(x=380, y=100)
        listField.insert("end", *downloadList)

        def addDownload():
            moveList = []
            downloadText = inputField.get(1.0, "end-1c")
            if downloadText:
                line = downloadText.split("\n")
                for l in line:
                    downloadList.append(l)
                for l in line:
                    moveList.append(l)
                listField.insert("end", *moveList)
                inputField.delete(1.0, "end")

        def deleteDownload():
            select = listField.curselection()
            for i in select[::-1]:
                listField.delete(i)
                downloadList.remove(downloadList[i])

        def deleteAllDownloads():
            answer = askyesno(title="Confirmation",
                              message="Are you sure you want to delete everything?")
            if answer is True:
                WADList.clear()
                listField.delete("0", "end")

        buttonAdd = ttk.Button(self, text = "Add WAD", command = lambda : addDownload())
        buttonAdd.place(x=245, y=100)

        buttonRemove = ttk.Button(self, text="Delete WAD", command = lambda : deleteDownload())
        buttonRemove.place(x=245, y=125)

        buttonDelete = ttk.Button(self, text="Delete All", command = lambda : deleteAllDownloads())
        buttonDelete.place(x=245, y=150)


app = Application()
app.resizable(False, False)
app.mainloop()
