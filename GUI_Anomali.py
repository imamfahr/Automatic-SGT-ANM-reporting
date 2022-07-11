from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter.ttk import Progressbar
from tkinter import filedialog
from tkinter import Menu
from turtle import width

from sqlalchemy import column

window = Tk()
window.title('Anomali Report Generator')
window.geometry('500x350')


#label
Welcome = Label(window, text = "Welcome",  justify='left',bg="red")
test1 = Label(window,text='column=1, row=0',bg='green')
test2 = Label(window,text='column=0, row=15',bg='orange')
downtime_limit_label = Label(window,text='Downtime Limit (hours)')
Week_name_label = Label(window, text='Week of report (can be number or range of date)')
Week_name_entry = Entry(window)





#button function
def MER_directory():
    messagebox.showinfo( "Please choose 2")

#button
#size properties

width_button = 18
height_button = 1
padx_button = 4
pady_button = 5


MER_button = Button(window, text ="Upload MER", command = MER_directory, width=width_button, heigh = height_button, padx = padx_button,pady=pady_button)
EMPS_button = Button(window, text ="Upload EMPS", command = MER_directory, width=width_button, heigh = height_button, padx = padx_button,pady=pady_button)
PDTD_button = Button(window, text ="Upload Downtime Detail", command = MER_directory,width=width_button, heigh = height_button, padx = padx_button,pady=pady_button)
FleetDesc_button = Button(window, text ="Upload Fleet Description", command = MER_directory,width=width_button, heigh = height_button, padx = padx_button,pady=pady_button)

#scrolled downtime limit 
var = IntVar()
downtime_limit = Spinbox(window,from_=0, to=100, width=10, textvariable=var)

generate_below_target_report_button =Button(window,text='Generate Report', command=MER_directory)

MER_button.pack
EMPS_button.pack
PDTD_button.pack
FleetDesc_button.pack
generate_below_target_report_button.pack



#arrange widget position allocation
Welcome.grid(column = 0, row = 0,columnspan=7)
test1.grid(column=1, row=0)
test2.grid(column=0,row=10)
Week_name_label.grid(column=0,row=2)
Week_name_entry.grid(column=1,row=2)
MER_button.grid(column=0,row=5)
EMPS_button.grid(column=0,row=6)
PDTD_button.grid(column=0,row=7)
FleetDesc_button.grid(column=0,row=8)
downtime_limit_label.grid(column=0,row=11)
downtime_limit.grid(column=1,row=11)

generate_below_target_report_button.grid(column=2,row=15)

window.mainloop()