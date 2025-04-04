import os
from tkinter.messagebox import showinfo
from threading import Thread
from pytubefix import YouTube
from tkinter import filedialog


class App:

    def __init__(self, entry, progressBar, opt1, opt2, progressLabel):

        self.progressLabel = progressLabel
        self.optionButtons: list = [opt1, opt2]
        self.progressBar = progressBar
        self.entry = entry

        self.currentFile = None
        self.title = None
        self.youtubeObject: YouTube = None

        self.options = {
            "audio": True,
            "video": False
        }

        self.user: str = os.path.expanduser('~')
        self.destination = self.user + "/Desktop/Filmy"

    def updateOptions(self, option: int, optionType: str) -> None:
        option = bool(option)
        if optionType == "audio":
            self.options.update({"audio": option})
        else:
            if not option:
                self.optionButtons[0].configure(state="normal")
            else:
                self.optionButtons[0].configure(state="disabled")
            self.options.update({"video": option})

    def debug(self):
        self.get_youtubeObject()
        self.getTitle()
        self.getDestination()
        self.getBestBitrate()
        self.currentFile.download(output_path=self.destination, filename=self.title)
        pass


    def get_youtubeObject(self) -> int | None:
        try:
            if self.entry.get() == '':
                raise ValueError
            self.youtubeObject = YouTube(self.entry.get(),
                                         client="WEB",
                                         on_progress_callback=self.on_progress,
                                         use_po_token=True
                                         )
        except ValueError:
            showinfo("Error", "Link not entered")
            return -1
        except:
            showinfo('Error', 'Video not found')
            return -1

    @staticmethod
    def getMB(size):
        return size/1_048_576

    def getRemaining(self, size1, size2) -> float:
        return self.getMB(size1)-self.getMB(size2)

    def on_progress(self, stream, chunk, bytes_remaining) -> None:
        totalSize = self.currentFile.filesize
        self.progressLabel.configure(text=f"{self.getMB(totalSize):.1f} MB / {self.getRemaining(totalSize, bytes_remaining):.1f} MB")
        number = (1 - bytes_remaining / totalSize) * 100
        self.progressBar['value'] = number

    def getTitle(self) -> None:
        self.title = self.youtubeObject.title
        self.title += ".wav"
        replacements = [('/', '_'), ('*', '_'), ('"', '_'), ('|', ' ')]
        for char, replacement in replacements:
            if char in self.title:
                self.title = self.title.replace(char, replacement)

    @staticmethod
    def changeDestination(newDestination) -> None:
        file = open("settings.txt", "w")
        file.write("save_space=" + newDestination)
        file.close()

    def getDestination(self) -> str:
        file = open("settings.txt", "r")
        string = file.read()
        index = (string.find("=")) + 1
        destination = string[index:]
        file.close()
        self.destination = destination
        return destination

    def getBestBitrate(self) -> None:
        try:
            err = self.get_youtubeObject()
            if err == -1:
                raise Exception
            file = self.youtubeObject
            streamId = 0
            previousBitrate = 0
            for stream in file.streams.filter(only_audio=True):
                if stream.mime_type =="audio/webm":
                    continue
                bitrate = stream.abr
                bitrate = int(bitrate.removesuffix("kbps"))
                if bitrate > previousBitrate:
                    previousBitrate = bitrate
                    streamId = stream.itag
            file = file.streams.get_by_itag(streamId)
            file = self.youtubeObject.streams.get_audio_only()
            self.currentFile = file
        except Exception:
            showinfo("Wystąpił problem z odczytaniem wartości")
            self.currentFile = None

    def getBestResolution(self) -> None:
        try:
            err = self.get_youtubeObject()
            if err == -1:
                raise Exception
            file = self.youtubeObject
            streamId = 0
            prevRes = 0
            for stream in file.streams:
                if stream.resolution is None:
                    continue
                res = str(stream.resolution).removesuffix("p")
                res = int(res)
                if res > prevRes:
                    prevRes = res
                    streamId = stream.itag
            self.currentFile = file.streams.get_by_itag(streamId)
        except Exception:
            print("Wystąpił problem")
            self.currentFile = None

    def download(self) -> None:
        try:
            if self.options.get("video"):
                #self.getBestResolution()
                pass
            else:
                self.getBestBitrate()
            if self.currentFile is None:
                raise Exception
            self.getTitle()
            self.getDestination()
            self.progressLabel.configure(text=f"{self.currentFile.filesize/1_048_576:.1f} MB / 0.0 MB")
            print(self.currentFile)
            self.currentFile.download(output_path=self.destination, filename=self.title)
        except Exception:
            self.progressBar['value'] = 0
            showinfo("Error", "Could not find given parameters")
            print("Problem z pobraniem właściwego ID")
            return None
        except:
            self.progressBar['value'] = 0
            showinfo("Error", "Something went wrong with download.")
            print("Wystąpił problem z pobieraniem")
            return None
        else:
            self.progressBar['value'] = 0
            self.progressLabel.configure(text=f" 0.0 MB / 0.0 MB")
            showinfo("Success", "Download successful.")

    def thread_start(self):
        thread = Thread(target=self.download)
        thread.start()

