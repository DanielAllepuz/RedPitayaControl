import tkinter as tk

class Window(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        #set title of window
        self.winfo_toplevel().title("Red Pitaya Control")

        #make window widget fill window
        self.grid(column = 0, row = 0, sticky = (tk.N, tk.W, tk.E, tk.S))
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)

        # creating a button instance
        quitButton = tk.Button(self, text="Quit", command = self.adieu)

        quitButton.grid(column = 2, row = 1, sticky = (tk.W, tk.E))

    def adieu(self):
        exit()

root = tk.Tk()

app = Window(root)
root.mainloop()
