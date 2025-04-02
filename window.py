import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from app import App


class Window:

    def __init__(self) -> None:
        # Zmień debugMode na False przy robieniu pliku
        self.debugMode: bool = True
        self.window = tk.Tk()
        self.window.title("YT Downloader")
        self.var1 = tk.IntVar()
        self.var2 = tk.IntVar()
        self.spaceLabel = tk.Label(self.window, text="                            ")
        self.mainLabel = tk.Label(self.window, text="Rozpocznij pobieranie")
        self.mainEntry = tk.Entry(self.window)
        self.progressLabel = tk.Label(self.window, text="")
        self.progressBar = ttk.Progressbar(self.window, length=125, mode='determinate')
        self.option1 = tk.Checkbutton(self.window, text="Audio")
        self.option2 = tk.Checkbutton(self.window, text="Video")
        self.downloadButton = tk.Button(self.window, text="Pobierz")
        self.debugButton = tk.Button(self.window, text="Debuguj")
        self.resetButton = tk.Button(self.window, text="Wyczyść")
        self.destinationButton = tk.Button(self.window, text="Zmień miejsce pobierania")

        self.logic = App(self.mainEntry,
                         self.progressBar,
                         self.option1,
                         self.option2,
                         self.progressLabel)

        self.setGrid()
        self.setCommands()
        self.setDefaults()

        self.window.geometry("300x200")
        self.window.mainloop()

    def setGrid(self) -> None:
        self.spaceLabel.grid(row=0, column=0)
        self.mainLabel.grid(row=0, column=1)
        self.mainEntry.grid(row=1, column=1)
        self.progressLabel.grid(row=4, column=1)
        self.progressBar.grid(row=3, column=1)
        self.option1.grid(row=1, column=0)
        self.option2.grid(row=2, column=0)
        self.downloadButton.grid(row=2, column=1, sticky='W')
        if self.debugMode:
            self.debugButton.grid(row=6, column=1)
        self.destinationButton.grid(row=5, column=1)
        self.resetButton.grid(row=2, columnspan=2, sticky='E')

    def setCommands(self) -> None:
        self.option1.configure(variable=self.var1, command=lambda: self.logic.updateOptions(self.var1.get(), "audio"))
        self.option2.configure(variable=self.var2, command=lambda: self.logic.updateOptions(self.var2.get(), "video"))
        self.downloadButton.configure(command=self.logic.thread_start)
        self.debugButton.configure(command=self.logic.debug)
        self.resetButton.configure(command=lambda: self.reset(self.mainEntry))
        self.destinationButton.configure(command=lambda: self.logic.changeDestination(filedialog.askdirectory()))

    def setDefaults(self) -> None:
        self.progressLabel.configure(text=f" 0.0 MB / 0.0 MB")
        self.option1.select()

    @staticmethod
    def reset(entry: any) -> None:
        last_num = len(entry.get()) + 1
        entry.delete(0, last_num)


if __name__ == '__main__':
    Window().debugMode = False

