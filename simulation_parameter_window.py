import tkinter as tk
from tkinter import messagebox


class SimulationWindow:
    def __init__(self, mode):
        self.root = tk.Tk()
        self._setMode(mode)
        self.result = None
        self.closed = False
        self.root.protocol("WM_DELETE_WINDOW", self._onClosing)
        self._setTitle(mode)
        self.root.geometry("300x80")
        self.root.resizable(False, False)
        self._setButtons(mode)

    def _setMode(self, mode):
        if mode == "scope":
            self.mode = tk.StringVar(value="entire_network")
        if mode == "path":
            self.mode = tk.StringVar(value="shortest_path")

    def _setTitle(self, mode):
        if mode == "scope":
            self.root.title("Choose simulation mode")
        if mode == "path":
            self.root.title("Choose path mode")

    def run(self):
        self.root.mainloop()

    def getResult(self):
        return self.result

    def wasClosed(self):
        return self.closed

    def _onClosing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.quit()
            self.root.destroy()
            self.closed = True

    def _setButtons(self, mode):
        if mode == "scope":
            tk.Radiobutton(self.root,
                           text="Entire network",
                           variable=self.mode,
                           value="entire_network").grid(row=1, column=2, sticky=tk.W, padx=100)
            tk.Radiobutton(self.root,
                           text="Node pair",
                           variable=self.mode,
                           value="node_pair").grid(row=2, column=2, sticky=tk.W, padx=100)

            tk.Button(self.root, text="Submit", command=self._submit).\
                grid(row=3, column=2, sticky=tk.W, padx=100)
        if mode == "path":
            tk.Radiobutton(self.root,
                           text="Shortest path",
                           variable=self.mode,
                           value="shortest_path").grid(row=1, column=2, sticky=tk.W, padx=100)
            tk.Radiobutton(self.root,
                           text="Select path",
                           variable=self.mode,
                           value="select_path").grid(row=2, column=2, sticky=tk.W, padx=100)

            tk.Button(self.root, text="Submit", command=self._submit). \
                grid(row=3, column=2, sticky=tk.E, padx=50)

            tk.Button(self.root, text="Back", command=self._quit). \
                grid(row=3, column=2, sticky=tk.W, padx=50)

    def _quit(self):
        self.root.quit()
        self.root.destroy()

    def _submit(self):
        self.result = self.mode.get()
        self._quit()
