import os
import zipfile
import shutil

from tkinter import *
from tkinter import ttk
from tkinter import filedialog as FD
from tkinter import messagebox
from tkinter import simpledialog as SD
from datetime import datetime
# import time
import re
root = Tk()
root.withdraw()

def isCycle(filename, frame_mod):
    return int(filename.split('.')[0].split('_')[-1]) % frame_mod == 0

# gets a list of all files of a given type throughout the hierarchy
def getFiles(folder_path, arr, ext, frame_mod):
    if os.path.isdir(folder_path):
        for f in os.listdir(folder_path):
            f_path = os.path.join(folder_path, f)
            if os.path.isdir(f_path):
                print ("Internal folder: " + f)
                getFiles(os.path.join(folder_path, f), arr, ext, frame_mod)
            elif os.path.isfile(f_path) and f.endswith(ext) and isCycle(f, frame_mod):
                # file_number = int(f.split('.')[0].split('_')[-1])%frame_mod == 0
                arr.append(os.path.join(folder_path, f))
    return x

# copies each file found in above to the new folder, adjusting for duplicates
def addAll(nfp, arr, ext):
    n=0
    processed = []
    for file in arr:
        fname = os.path.basename(file)
        fpath = os.path.join(nfp, fname)
        if os.path.isfile(fpath):
            print("Duplicate: " + fname)
            num_d = 0;
            for proc in processed:
                match = re.findall("%s" % fname.replace(ext, ""), proc)
                if match:
                    num_d +=1
            ending = "({version}){e}"
            fname = fname.replace(ext, "") + ending.format(version=num_d, e=ext)
            fpath = os.path.join(nfp, fname)
            print("New name: " + fname)
        shutil.copy(file, fpath)
        processed.append(fname)
        n+=1
        root.update_idletasks()
        progress_var.set(n)
    return n

progress_var = DoubleVar() #here you have ints but when calc. %'s usually floats
x = []

def main():
    extension = SD.askstring("Ext", "Enter OK for all files, else enter extension")
    now = datetime.now()
    dt_string = now.strftime("%d %m %Y %H %M")
    origin = FD.askdirectory(title="Source directory")
    if not origin:
        exit()
    frame_count_period = int(SD.askstring("FPS", "Enter OK for all frames, else enter a frame count period/modulus"))
    if not frame_count_period:
        frame_count_period = False
    dest = FD.askdirectory(title="Destination directory")
    if not dest:
        exit()

    cwd = origin
    big_folder_path = os.path.join(dest, "KEYS " + extension.strip(".").upper() + " " +dt_string)
    if not os.path.exists(big_folder_path):
        os.makedirs(big_folder_path)

    getFiles(cwd, x, extension, frame_count_period)

    conf = "Source: {s} \nDestination: {d} \nExtension: {e} \nNum files: {n} \nFrame Period: {f}"
    answer = messagebox.askokcancel("Confirm",conf.format(s=origin, d=dest, e=extension, n=len(x), f=frame_count_period))
    if not answer:
        exit()

    root.deiconify()
    theLabel = Label(root, text="Copying...")
    theLabel.pack()
    progressbar = ttk.Progressbar(root, variable=progress_var, maximum=len(x))
    progressbar.pack(fill=X, expand=1)

    print ("+"*50)
    print("Copying:")
    num = addAll(big_folder_path, x, extension)
    root.withdraw()

    final = "{n} files of type {e} copied\nFrom:{s} \nTo: {d}"
    endscreen = messagebox.askokcancel("Operation Complete",final.format(n=num, s=origin, d=dest, e=extension))
    exit()
    root.mainloop()

if __name__ == "__main__":
    main()