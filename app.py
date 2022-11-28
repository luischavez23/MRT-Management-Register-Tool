import tkinter as tk
import getpass
from tkinter import ttk
from frames.register_frame import Register
from frames.search_frame import Search

class ControlFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        
        #Getting PC user
        #user="Alex"
        user=getpass.getuser()
        technical_user= ["jewillis", "rcortese", "lpchavez", "capatric", "mavasque", "ejarredo", "cedelgad"] 
        
        """
        MAIN MENU SECTION
        """
        menu_label = ttk.Label(self, text="Select an option", foreground="gray14")
        menu_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        menu_label_user = ttk.Label(self, text=user)
        menu_label_user.grid(row=0, column=10, padx=20, pady=0, sticky=tk.E)
        
        #Declaration of items to appear in the menu    
        if user in technical_user:
            self.frames_menu_list = ("Register", "Search")
        else:
            self.frames_menu_list = ("Register", "Search")
        self.frames_menu_var = tk.StringVar(self)

        #Settings of the Dropdown menu widget
        frames_menu = ttk.OptionMenu(self, self.frames_menu_var, self.frames_menu_list[0],*self.frames_menu_list, command=self.frames_menu_actions)
        frames_menu.grid(column=1,row=0)

        #setting the root position      
        self.grid(column=0, row=0, padx=5, pady=5, sticky='ew')

        """
        FRAMES COLLECTION
        """     
        self.frames = dict()
        self.frames[Register] = Register(container)
        self.frames[Search] = Search(container)

        #frame would be showed first
        self.change_frame(Register)

        
    def change_frame(self,frame):
        frame = self.frames[frame]
        frame.tkraise()

    def frames_menu_actions(self, selected_frame):
        if selected_frame == "Register":
            self.change_frame(Register)
            SiTrackRoot.geometry("280x350")

        elif selected_frame == "Search":
            self.change_frame(Search)
            SiTrackRoot.geometry("280x340")


class AppRoot(tk.Tk):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        
        #Basic configurations for the app root
        self.title("MRT")             #IRT Items Register and Tracking                  #Material Register and Tracking
        self.geometry("280x350")
        self.iconbitmap("chip.ico")
        self.resizable(False,False)
        self.config(bg="gray96")

if __name__ == "__main__":
    
    SiTrackRoot = AppRoot()
    ControlFrame(SiTrackRoot)
    SiTrackRoot.mainloop()
    