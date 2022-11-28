import tkinter as tk
from tkinter import ttk
from tkinter import ACTIVE, StringVar 
from tkinter import messagebox as mb
import tkinter.scrolledtext as st
from idlelib.tooltip import Hovertip
import connection_db, re
import pandas as pd
from datetime import datetime
import getpass
import os

class Search(tk.Frame):
    def __init__(self,container):
        super().__init__(container)
        self.app = connection_db.Asset()

        #Search box
        self.search_box_label = tk.Label(self, text="BARCODES to search: ", fg="midnightblue", font =('Arial', 9, 'bold'))
        self.search_box_label.grid(row=1, column=0, padx=30, pady=(5,5))
        self.search_box =st.ScrolledText(self, width=25, height=9) 
        self.search_box.grid(row=2, column=0, pady=0, padx=30, ipady=2)
        self.search_box.focus()
        Hovertip(self.search_box, text="GDC's, MCODES or SN", hover_delay=150)

        #Checkbox for full history
        self.full_history_status = StringVar() 
        self.full_history = ttk.Checkbutton(self, text="Full History", var=self.full_history_status ,onvalue="Yes")
        if self.full_history_status.get()=="Yes":
            self.full_history.config(state=ACTIVE)
        self.full_history.grid(row=3, column=0, padx=70, pady=7, ipadx=0, ipady=8)
        Hovertip(self.full_history, text="SELECT TO SHOW FULL HISTORY OF BARCODES TYPED", hover_delay=150)
        #lambda : [self.search_db(), self.clear_search_inputs()]
        #Search button
        self.search_button = tk.Button(self, text="SEARCH", command=self.search_db, bg = "gray69", font =('calibri', 9, 'bold'))
        self.search_button.grid(row=4, column=0, padx=0, pady=8, ipadx=32, ipady=8)

        self.grid(column=0, row=1, padx=5, pady=0, sticky="nsew")
########################################################################### METHODS of ACTION
    def input_validation(self,input_datas):
        barcode_regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]') #This is a set of references of what not to have in the barcodes.
        
        return all(barcode_regex.search(barcode)==None for barcode in input_datas)      #This return TRUE if all items in a list match an evaluation, in this case, the correct format  
        
    def search_db(self):
        
        list_bti = ["silicon","platform","host","drawer","scope","thermal head","ttk3","nevo","power supply","power splitter","xdp","dci","dbc","switch matrix","hdd","graphic card"]
        remove = self.search_box.get("1.0", tk.END).translate('\t\n ').upper().strip()
        datas = (tuple(remove.splitlines()),)
        
        for data in datas:

            bti_data = data[0].lower()
            data_cap = data[0].capitalize()
            self.find_bti = [bti for bti in list_bti if bti_data in bti] 

            if data == ('',):  #Void entry validation
                mb.showerror('Error', 'Please, type GDC\'s, MCODE or VID.')
            
            elif not self.input_validation(data): #Correct Format entry validation
                mb.showerror('Error', 'The barcodes were entered incorrectly. Please double-check your list.')
            
            elif self.find_bti:
                self.category = self.app.category_list(data_cap)
                self.show_allhistory_search_info()
                for data in range(len(self.category)):
                    self.results_header.insert("", tk.END, values=self.category[data])
            
            else:
                
                if self.full_history_status.get()=='Yes':
                    self.select_query = self.app.select_db(data, True) #This returns all requested data
                    self.list_length = len(self.select_query)+1 #This returns the lenght of the requested data list
                    print(self.list_length)
                    if self.list_length > 1:
                        self.show_allhistory_search_info()
                        for data in range(self.list_length):
                            self.results_header.insert("", tk.END, values=self.select_query[data])
                    else:
                       mb.showwarning('Warning', 'The barcode is not found in the database.') 
                else:
                    self.last_location_list_query = self.app.select_db(data, False) #This returns all requested data
                    self.list_length = len(self.last_location_list_query)+1 #This returns the lenght of the requested data list
                    if self.list_length > 1:
                        self.show_search_info()
                        for data in range(self.list_length):
                            self.results_header.insert("", tk.END, values=self.last_location_list_query[data])
                    else:
                       mb.showwarning('Warning', 'The barcode is not found in the database.')
                
                self.clear_search_inputs() #Clear the data that user typed into the search box

    def show_search_info(self):
        self.search_results_Window = tk.Toplevel()
        self.search_results_Window.title("SEARCH RESULTS") 
        self.search_results_Window.geometry("789x265")
        self.search_results_Window.resizable(False, False)
        self.search_results_Window.grab_set()
        self.search_results_Window.bind('<Escape>', lambda x : self.close_win())
        self.search_results_Window.focus()
        
        self.report_button = tk.Button(self.search_results_Window, text="Excel export", bg = "SpringGreen2", font =('calibri', 10, 'bold', 'underline'), command=self.Report_file)
        self.report_button.grid(row=6,column=0, padx=30, pady=4)

        self.results_header = ttk.Treeview(self.search_results_Window) 
        self.results_header.grid(row=0, column=0, padx=1, pady=1)

        vsb = ttk.Scrollbar(self.search_results_Window, orient="vertical")  
        vsb.grid(row=0, column=5, padx=0, sticky=tk.NS)
        self.results_header.configure(yscrollcommand=vsb.set)

        self.results_header["columns"] = ("1","2","3","4","5")
        self.results_header['show']='headings'
        self.results_header.column("#1", anchor=tk.CENTER, width=120)
        self.results_header.heading("#1", text="BARCODE")
        self.results_header.column("#2", anchor=tk.CENTER, width=210)
        self.results_header.heading("#2", text="LAST LOCATION")
        self.results_header.column("#3", anchor=tk.CENTER, width=120)
        self.results_header.heading("#3", text="RECENT USER")
        self.results_header.column("#4", anchor=tk.CENTER, width=190)
        self.results_header.heading("#4", text="LAST USED ON")
        self.results_header.column("#5", anchor=tk.CENTER, width=120)
        self.results_header.heading("#5", text="ASSET TYPE")

    def show_allhistory_search_info(self):
        self.search_results_Window = tk.Toplevel()
        self.search_results_Window.title("SEARCH RESULTS") 
        self.search_results_Window.geometry("789x265")
        self.search_results_Window.resizable(False, False)
        self.search_results_Window.grab_set()
        self.search_results_Window.bind('<Escape>', lambda x : self.close_win())
        self.search_results_Window.focus()
        
        self.report_button = tk.Button(self.search_results_Window, text="Excel export", bg = "SpringGreen2", font =('calibri', 10, 'bold', 'underline'), command=self.Report_file)
        self.report_button.grid(row=6,column=0, padx=30, pady=4)

        self.results_header = ttk.Treeview(self.search_results_Window) 
        self.results_header.grid(row=0, column=0, padx=1, pady=1)

        vsb = ttk.Scrollbar(self.search_results_Window, orient="vertical")  
        vsb.grid(row=0, column=5, padx=0, sticky=tk.NS)
        self.results_header.configure(yscrollcommand=vsb.set)

        self.results_header["columns"] = ("1","2","3","4","5")
        self.results_header['show']='headings'
        self.results_header.column("#1", anchor=tk.CENTER, width=120)
        self.results_header.heading("#1", text="BARCODE")
        self.results_header.column("#2", anchor=tk.CENTER, width=210)
        self.results_header.heading("#2", text="LOCATION")
        self.results_header.column("#3", anchor=tk.CENTER, width=120)
        self.results_header.heading("#3", text="USER")
        self.results_header.column("#4", anchor=tk.CENTER, width=190)
        self.results_header.heading("#4", text="DATE")
        self.results_header.column("#5", anchor=tk.CENTER, width=120)
        self.results_header.heading("#5", text="ASSET TYPE")


    def Report_file(self):
        if self.find_bti:
            df = pd.DataFrame(self.category,columns=['BARCODE','LOCATION','USER','DATE','TYPE'])
        elif self.full_history_status.get()=='Yes':
            df = pd.DataFrame(self.select_query, columns=['BARCODE','LOCATION','USER','DATE','TYPE'])
        else:
            df = pd.DataFrame(self.last_location_list_query, columns=['BARCODE','LAST LOCATION','RECENT USER','LAST USED ON','ASSET TYPE'])
        
        self.date_time = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
        file = f'cave_ave_local_invetory_{self.date_time}.xlsx'
        file_dir = 'C:\\Users\\'+getpass.getuser()+'\\Downloads\\'+file

         # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(file_dir, engine='xlsxwriter')

        # Convert the dataframe to an XlsxWriter Excel object.
        df.to_excel(writer, sheet_name='Items', index=False)

        worksheet = writer.sheets['Items']
        worksheet.set_column(1, 1, 30)
        worksheet.set_column(2, 2, 20)
        worksheet.set_column(3, 3, 20)
        worksheet.set_column(4, 4, 15)

        #Open the file with os library
        os.startfile(file_dir)

        # Close the Pandas Excel writer and output the Excel file.
        writer.close()
        
    def clear_search_inputs(self):  
        self.search_box.delete("1.0","end")
        
    def close_win(self):
        self.search_results_Window.destroy()
        self.clear_search_inputs()
        