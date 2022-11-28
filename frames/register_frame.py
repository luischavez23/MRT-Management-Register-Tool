import tkinter as tk
from tkinter import StringVar, ttk
import tkinter.scrolledtext as st
from tkinter import messagebox as mb
import getpass,re
import datetime
from idlelib.tooltip import Hovertip
import connection_db

class Register(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.app = connection_db.Asset()

        #For Barcodes inputs
        self.label_barcode= ttk.Label(self, text="BARCODE:", foreground="midnightblue")                             
        self.label_barcode.grid(row=0, column=0, padx=1, pady=1)
        Hovertip(self.label_barcode, text="GDC's, MCODES or SN", hover_delay=500)
        self.text_barcode = st.ScrolledText(self, width=26, height=5)              
        self.text_barcode.grid(row=1, column=0, pady=6, padx=20, ipady=2)
        self.text_barcode.focus()
        Hovertip(self.text_barcode, text="GDC's, MCODES or SN", hover_delay=100)

        #For Location inputs
        self.label_locality= ttk.Label(self, text="LOCATION:", foreground="navy")   
        self.label_locality.grid(row=2, column=0, padx=5, pady=2)
        self.locality_str = tk.StringVar()
        self.text_locality = ttk.Entry(self, textvariable=self.locality_str, width=22)
        self.text_locality.grid(row=3, pady=5, padx=5, ipady=4,ipadx=25)

        #For Type of ASSET inputs
        self.label_asset = ttk.Label(self, text='ASSET:', foreground="navy")
        self.label_asset.grid(column=0, row=4, padx=80, ipady = 5 )
    
        self.type_asset = ttk.Combobox(self,
            state = "readonly",
            values=["Silicon","Platform","Host","Drawer","Scope","Thermal head","TTK3","NEVO","Power supply","Power splitter","XDP","DCI","DBC","Switch Matrix","HDD","Graphic Card"]
        )
        self.type_asset.current(0)
        self.type_asset.grid(column=0, row=5)

        #Button for SUBMIT RECORD
        self.submit_register = ttk.Button(self, text="Submit", command=self.submit_register_inputs)
        self.submit_register.grid(row=6, column=0, padx=0, pady=17, ipadx=40, ipady=10)

        self.grid(column=0, row=1, padx=5, pady=0, sticky="nsew")
        
########################################################################### METHODS of ACTION
    def clear_register_inputs(self):  
        self.text_barcode.delete("1.0","end")
        self.text_locality.delete('0','end')
        self.type_asset.set('Silicon')
        self.text_barcode.focus()
    
    def input_validation(self,input_barcodes, locality):
        barcode_regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]') #This is a set of references of what not to have in the barcodes.
        locality_regex = ''
        # '^\\d+$'    This was used for evaluating the entry data, but for this firt realease will be okay to not evaluate.
        barcode_status = False
        locality_status = False

        #Check the barcode data box
        barcode_status = all(barcode_regex.search(barcode)==None for barcode in input_barcodes) #This return TRUE if all items in a list match an evaluation, in this case, the correct format
        #Check the locality data box
        if re.search(locality_regex, locality) != None:
            locality_status = True
        else:
            locality_status = False

        return barcode_status,locality_status
        
    def submit_register_inputs(self):
        remove = self.text_barcode.get("1.0", "end-1c").translate('\t\n ').upper()
        split_barcodes = remove.split()
        locality = self.text_locality.get()
        db_date= datetime.datetime.now()
        db_user= getpass.getuser()
        barcode_entry_status = self.input_validation(split_barcodes, locality)[0]
        locality_entry_status = self.input_validation(split_barcodes, locality)[1]


        if split_barcodes == [] or locality == '': #Void Entry Evaluation
            mb.showerror('Error', 'Please fill out all the fields form.')
        elif not barcode_entry_status: #Correct Format Evaluation on the Barcodes Entry Box
            mb.showerror('Error', 'The barcode was entered incorrectly. Please double-check it.')
        elif not locality_entry_status: #Correct Format Evaluation on the Locality Entry Box
            mb.showerror('Error', 'The locality was entered incorrectly. Please double-check it.')
        else:
            for row in split_barcodes:
                datas = (row, self.type_asset.get(), self.text_locality.get(), db_user, db_date)
                self.app.insert_db(datas)
            mb.showinfo('Registered', f'Registration has been succesfully completed.')
            self.clear_register_inputs()
            
