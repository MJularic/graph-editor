import tkinter as tk
from fastnumbers import fast_float
from tkinter import messagebox


class NetworkParameterInput:
    def __init__(self, graph, selected, object):
        self.graph = graph
        self.selected = selected
        self.object = object
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self._onClosing)
        self._setLabels()
        self._setEntry()
        self._setButtons()
        self._customizeRoot()
        self.closed = False

    def _setLabels(self):
        tk.Label(self.root, text="Failure intensity").grid(row=0)
        tk.Label(self.root, text="Repair intensity").grid(row=1)

        if self.object == "edge":
            tk.Label(self.root, text="Weight").grid(row=2)

    def _onClosing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.quit()
            self.root.destroy()
            self.closed = True

    def wasClosed(self):
        return self.closed

    def _setEntry(self):
        self.failure_intensity = tk.Entry(self.root)
        self.failure_intensity.grid(row=0, column=1)

        self.repair_intensity = tk.Entry(self.root)
        self.repair_intensity.grid(row=1, column=1)

        if self.object == "node":
            self._nodeEntry()
        else:
            self._linkEntry()

    def _setButtons(self):
        tk.Button(self.root, text="Submit", command=self._submitHandler).grid(row=3, column=0, sticky=tk.W, pady=4)
        tk.Button(self.root, text="Quit", command=self._quit).grid(row=3, column=1, sticky=tk.W, pady=4)

    def _submitHandler(self):
        failure = self._stringToFloat(self.failure_intensity.get())
        repair = self._stringToFloat(self.repair_intensity.get())

        if failure == "invalid" or repair == "invalid":
            return

        if self.object == "node":
            self.graph.node[self.selected]['failure_intensity'] = failure
            self.graph.node[self.selected]['repair_intensity'] = repair
        else:
            weight = self._stringToFloat(self.weight.get())
            if weight == "invalid":
                return
            self.graph[self.selected[0]][self.selected[1]]['failure_intensity'] = failure
            self.graph[self.selected[0]][self.selected[1]]['repair_intensity'] = repair
            self.graph[self.selected[0]][self.selected[1]]['weight'] = weight

        self._quit()

    def _customizeRoot(self):
        self.root.title("Edit " + self.object)
        self.root.resizable(False, False)

    def _nodeEntry(self):
        if 'failure_intensity' in self.graph.node[self.selected]:
            self.failure_intensity.insert(tk.END, self.graph.node[self.selected]['failure_intensity'])

        if 'repair_intensity' in self.graph.node[self.selected]:
            self.repair_intensity.insert(tk.END, self.graph.node[self.selected]['repair_intensity'])

    def _linkEntry(self):
        edge = self.graph[self.selected[0]][self.selected[1]]
        if 'failure_intensity' in edge:
            self.failure_intensity.insert(tk.END, edge['failure_intensity'])

        if 'repair_intensity' in edge:
            self.repair_intensity.insert(tk.END, edge['repair_intensity'])

        self.weight = tk.Entry(self.root)
        self.weight.grid(row=2, column=1)
        if 'weight' in edge:
            self.weight.insert(tk.END, edge['weight'])

    def run(self):
        self.root.mainloop()

    def _quit(self):
        self.root.quit()
        self.root.destroy()

    def _stringToFloat(self, string):
        return fast_float(string, default="invalid")