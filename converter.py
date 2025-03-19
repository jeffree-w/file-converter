import os
import subprocess
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image

filePaths = []

def browseFiles():
    files = filedialog.askopenfilenames(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff;*.gif;*.webp;*.ico")])
    global filePaths
    filePaths = files
    showFilePaths()

def onDrop(event):
    global filePaths
    filePaths = root.tk.splitlist(event.data)
    showFilePaths()

def showFilePaths():
    for widget in scrollableFrame.winfo_children():
        widget.destroy()

    if filePaths:
        for filePath in filePaths:
            fileName = os.path.basename(filePath)
            tk.Label(scrollableFrame, text=fileName).pack(anchor="w", pady=2)

def convertFiles():
    if not filePaths:
        messagebox.showerror("Error", "No files selected!")
        return

    outputFormat = formatVar.get().lower()
    successfulConversions = []
    failedConversions = []

    for filePath in filePaths:
        try:
            img = Image.open(filePath)
            outputFile = getOutputFile(filePath, outputFormat)
            img.save(outputFile, format=outputFormat.upper())
            successfulConversions.append(outputFile)
        except Exception as e:
            failedConversions.append(f"{filePath}: {str(e)}")

    if successfulConversions:
        messagebox.showinfo("Success", f"Files converted:\n" + "\n".join(successfulConversions))
    if failedConversions:
        messagebox.showerror("Failed", f"Failed to convert:\n" + "\n".join(failedConversions))

def getOutputFile(filePath, outputFormat):
    fileDir, fileName = os.path.split(filePath)
    fileNameNoExt = os.path.splitext(fileName)[0]
    return os.path.join(os.path.join(os.environ["USERPROFILE"], "Downloads"), f"{fileNameNoExt}.{outputFormat}")

root = TkinterDnD.Tk()
root.title("File Converter")
root.geometry("500x400")



dropArea = tk.Label(root, text="Drag Files Here", bg="lightgray", width=60, height=4)
dropArea.pack(pady=10)
dropArea.drop_target_register(DND_FILES)
dropArea.dnd_bind('<<Drop>>', onDrop)

tk.Button(root, text="Browse Files", command=browseFiles).pack(pady=5)

formatVar = tk.StringVar()
formatDropdown = ttk.Combobox(root, textvariable=formatVar, values=["JPEG", "PNG", "BMP", "TIFF", "GIF", "WEBP", "ICO"], state="readonly")
formatDropdown.pack(pady=5)
formatDropdown.current(0)

tk.Button(root, text="Convert", command=convertFiles).pack(pady=10)

canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)
scrollableFrame = tk.Frame(canvas)
scrollableFrame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollableFrame, anchor="nw")
scrollbar.pack(side="right", fill="y")
canvas.pack(pady=10)

root.mainloop()
