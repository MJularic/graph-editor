import tkinter as tk
from fastnumbers import fast_float


class TimeInputWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Set simulation time")
        self.root.resizable(False, False)
        self.root.geometry("300x80")
        self._setButtons()
        self._setLabels()
        self._setEntry()
        self.result = None

    def run(self):
        self.root.mainloop()

    def getResult(self):
        return self.result

    def _setLabels(self):
        tk.Label(self.root, text="Time").grid(row=0)


    def _setEntry(self):
        self.time = tk.Entry(self.root)
        self.time.grid(row=0, column=1)

    def _setButtons(self):
        tk.Button(self.root, text="Submit", command=self._submitHandler).grid(row=2, column=1, sticky=tk.E, padx=120)
        tk.Button(self.root, text="Quit", command=self._quit).grid(row=2, column=1, sticky=tk.W, padx=40)

    def _submitHandler(self):
        time = fast_float(self.time.get(), default="invalid")

        if time == "invalid":
            return

        self.result = time
        self._quit()

    def _quit(self):
        self.root.destroy()
        self.root.quit()
