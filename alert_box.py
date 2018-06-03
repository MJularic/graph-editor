from tkinter import messagebox
import tkinter as tk

class Alert:

    @staticmethod
    def alert(message):
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo(title="ERROR", message=message)
        root.destroy()
        root.quit()
