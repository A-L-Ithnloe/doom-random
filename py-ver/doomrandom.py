# Doom Randomizer v1.1
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
        label.place(relx = 0.5, rely = 0.05, anchor = "center")
        
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
            resultField.configure(state = "disabled")

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
        buttonWAD.place(relx = 0.02, rely = 0.2, relwidth = 0.25, relheight = 0.1, anchor = "w")

        buttonPlay = ttk.Button(self, text = "Playstyle", command = lambda : controller.showFrame(Playstyle))
        buttonPlay.place(relx = 0.5, rely = 0.2, relwidth = 0.25, relheight = 0.1, anchor = "center")

        buttonLoad = ttk.Button(self, text = "Loadout", command = lambda : controller.showFrame(Loadout))
        buttonLoad.place(relx = 0.98, rely = 0.2, relwidth = 0.25, relheight = 0.1, anchor = "e")

        buttonDownload = ttk.Button(self, text = "Download WADs", command = lambda: controller.showFrame(DownloadWADs))
        buttonDownload.place(relx = 0.02, rely = 0.4, relwidth = 0.25, relheight = 0.1, anchor = "w")

        buttonRandom = ttk.Button(self, text = "RANDOMIZE", command = lambda : randomize())
        buttonRandom.place(relx = 0.5, rely = 0.4, relwidth = 0.25, relheight = 0.1, anchor = "center")
        
        buttonChooseDownload = ttk.Button(self, text = "DOWNLOAD", command = lambda : download())
        buttonChooseDownload.place(relx = 0.98, rely = 0.4, relwidth = 0.25, relheight = 0.1, anchor = "e")

        resultField = tk.Text(self, width = 40, height = 5, state = 'disabled', wrap = "word")
        resultField.place(relx = 0.5, rely = 0.65, relwidth = 0.6, relheight = 0.25, anchor = "center")
        
        buttonExit = ttk.Button(self, text = "Exit", command = lambda : confirmExit())
        buttonExit.place(relx = 0.05, rely = 0.9, relwidth = 0.15, relheight = 0.1, anchor = "w")

class WADs(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text = "List of WADs", font = FONT)
        label.place(relx = 0.5, rely = 0.05, anchor = "center")

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

        buttonBack = ttk.Button(self, text = "Back", command = lambda : controller.showFrame(MainFrame))
        buttonBack.place(relx = 0.05, rely = 0.3, relwidth = 0.2, relheight = 0.1)
        
        inputField = tk.Text(self, width = 20, height = 5)
        inputField.place(relx = 0.05, rely = 0.45, relwidth = 0.3, relheight = 0.4)

        listField = tk.Listbox(self, width = 25, height = 5, selectmode = "multiple")
        listField.place(relx = 0.65, rely = 0.43, relwidth = 0.32, relheight = 0.5)
        listField.insert("end", *WADList)
        
        buttonAdd = ttk.Button(self, text = "Add WAD", command = lambda : addWAD())
        buttonAdd.place(relx = 0.5, rely = 0.5, relwidth = 0.25, relheight = 0.1, anchor = "center")
        
        buttonRemove = ttk.Button(self, text = "Delete WAD", command = lambda : deleteWAD())
        buttonRemove.place(relx = 0.5, rely = 0.61, relwidth = 0.25, relheight = 0.1, anchor = "center")
        
        buttonDelete = ttk.Button(self, text = "Delete All", command = lambda : deleteAllWADs())
        buttonDelete.place(relx = 0.5, rely = 0.72, relwidth = 0.25, relheight = 0.1, anchor = "center")
        

class Playstyle(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text = "List of Playstyles", font = FONT)
        label.place(relx = 0.5, rely = 0.05, anchor = "center")
        
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
        buttonBack.place(relx = 0.05, rely = 0.3, relwidth = 0.2, relheight = 0.1)

        inputField = tk.Text(self, width = 20, height = 5)
        inputField.place(relx = 0.05, rely = 0.45, relwidth = 0.3, relheight = 0.4)

        listField = tk.Listbox(self, width = 25, height = 5, selectmode = "multiple")
        listField.place(relx = 0.65, rely = 0.43, relwidth = 0.32, relheight = 0.5)
        listField.insert("end", *playstyleList)
        
        buttonAdd = ttk.Button(self, text = "Add Playstyle", command = lambda : addPlaystyle())
        buttonAdd.place(relx = 0.5, rely = 0.5, relwidth = 0.25, relheight = 0.1, anchor = "center")
        
        buttonRemove = ttk.Button(self, text = "Delete Playstyle", command = lambda : deletePlaystyle())
        buttonRemove.place(relx = 0.5, rely = 0.61, relwidth = 0.25, relheight = 0.1, anchor = "center")
        
        buttonDelete = ttk.Button(self, text = "Delete All", command = lambda : deleteAllPlaystyles())
        buttonDelete.place(relx = 0.5, rely = 0.72, relwidth = 0.25, relheight = 0.1, anchor = "center")


class Loadout(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text = "List of Loadouts", font = FONT)
        label.place(relx = 0.5, rely = 0.05, anchor = "center")
        
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
        buttonBack.place(relx = 0.05, rely = 0.3, relwidth = 0.2, relheight = 0.1)

        inputField = tk.Text(self, width = 20, height = 5)
        inputField.place(relx = 0.05, rely = 0.45, relwidth = 0.3, relheight = 0.4)

        listField = tk.Listbox(self, width = 27, height = 5, selectmode = "multiple")
        listField.place(relx = 0.65, rely = 0.43, relwidth = 0.32, relheight = 0.5)
        listField.insert("end", *loadoutList)
        
        buttonAdd = ttk.Button(self, text = "Add Loadout", command = lambda : addLoadout())
        buttonAdd.place(relx = 0.5, rely = 0.5, relwidth = 0.25, relheight = 0.1, anchor = "center")
        
        buttonRemove = ttk.Button(self, text = "Delete Loadout", command = lambda : deleteLoadout())
        buttonRemove.place(relx = 0.5, rely = 0.61, relwidth = 0.25, relheight = 0.1, anchor = "center")
        
        buttonDelete = ttk.Button(self, text = "Delete All", command = lambda : deleteAllLoadouts())
        buttonDelete.place(relx = 0.5, rely = 0.72, relwidth = 0.25, relheight = 0.1, anchor = "center")


class DownloadWADs(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="List of WADs to Download", font=FONT)
        label.place(relx = 0.5, rely = 0.05, anchor = "center")

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
        
        buttonBack = ttk.Button(self, text="Back", command = lambda : controller.showFrame(MainFrame))
        buttonBack.place(relx = 0.05, rely = 0.3, relwidth = 0.2, relheight = 0.1)

        inputField = tk.Text(self, width = 20, height = 5)
        inputField.place(relx = 0.05, rely = 0.45, relwidth = 0.3, relheight = 0.4)

        listField = tk.Listbox(self, width = 27, height = 5, selectmode="multiple")
        listField.place(relx = 0.65, rely = 0.43, relwidth = 0.32, relheight = 0.5)
        listField.insert("end", *downloadList)

        buttonAdd = ttk.Button(self, text = "Add WAD", command = lambda : addDownload())
        buttonAdd.place(relx = 0.5, rely = 0.5, relwidth = 0.25, relheight = 0.1, anchor = "center")

        buttonRemove = ttk.Button(self, text="Delete WAD", command = lambda : deleteDownload())
        buttonRemove.place(relx = 0.5, rely = 0.61, relwidth = 0.25, relheight = 0.1, anchor = "center")

        buttonDelete = ttk.Button(self, text="Delete All", command = lambda : deleteAllDownloads())
        buttonDelete.place(relx = 0.5, rely = 0.72, relwidth = 0.25, relheight = 0.1, anchor = "center")


app = Application()
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
app.minsize(width = screen_width // 4, height = screen_height // 4)
app.resizable(True, True)
app.mainloop()
