import os
import zipfile
import shutil

from tkinter import *
from tkinter import ttk
from tkinter import filedialog as FD
from tkinter import messagebox
from tkinter import simpledialog as SD
import time
import re
root = Tk()
root.withdraw()

# gets a list of all files of a given type throughout the hierarchy
def getFiles(folder_path, arr, ext):
    if os.path.isdir(folder_path):
        for f in os.listdir(folder_path):
            f_path = os.path.join(folder_path, f)
            if os.path.isdir(f_path):
                print ("Internal folder: " + f)
                getFiles(os.path.join(folder_path, f), arr, ext)
            elif os.path.isfile(f_path) and f.endswith(ext):
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
    origin = FD.askdirectory(title="Source directory")
    if not origin:
        exit()
    dest = FD.askdirectory(title="Destination directory")
    if not dest:
        exit()

    cwd = origin
    big_folder_path = os.path.join(dest, "ALL" + extension.strip(".").upper())
    if not os.path.exists(big_folder_path):
        os.makedirs(big_folder_path)

    getFiles(cwd, x, extension)

    conf = "Source: {s} \nDestination: {d} \nExtension: {e} \nNum files: {n}"
    answer = messagebox.askokcancel("Confirm",conf.format(s=origin, d=dest, e=extension, n=len(x)))
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