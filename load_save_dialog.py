from tkinter import filedialog
import tkinter as tk


class FileDialog:

    @staticmethod
    def loadFile():
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(parent=root, title="Select file", filetypes=[("graphml files", "*.graphml")])
        root.quit()
        root.destroy()
        return file_path

    @staticmethod
    def saveFile():
        root=tk.Tk()
        root.withdraw()
        file_path = filedialog.asksaveasfilename(parent=root, title="Save file", filetypes=[("graphml files", "*.graphml")])
        root.quit()
        root.destroy()
        return file_path

