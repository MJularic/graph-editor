from tkinter import messagebox
import tkinter as tk

class Alert:

    @staticmethod
    def alert(message, title):
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo(title=title, message=message)
        root.destroy()
        root.quit()
