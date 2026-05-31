import functions as func
import tkinter as tk
import os
import datetime


def ysws_init_load_answer(): # From binary choice
    selection = selected.get()
    for widget in root.winfo_children():
        widget.destroy()
    if selection == "True": # Load a YSWS profile
        ysws_profile_load()
    elif selection == "False": # Make a new profile
        ysws_profile_init(0)
    else:
        tk.Label(root, text="You've got to pick one!").pack()
        binary_choice("Load an existing YSWS profile?", selected, ysws_init_load_answer)

def ysws_profile_load():
    tk.Label(root, text="Which profile would you like to load?").pack()
    ysws = tk.Listbox(root)

    for file in os.listdir():
        if file.endswith(".json"):
            name = file.removesuffix(".json")
            name = name.replace("_", " ")
            ysws.insert(tk.END, name)
    ysws.pack()
    tk.Button(root, text="Submit", command=lambda: ysws_profile_load_answer(ysws)).pack()

def ysws_profile_load_answer(listbox):
    selection = listbox.get(tk.ACTIVE)
    for widget in root.winfo_children():
        widget.destroy()
    if selection:
        func.load_ysws(selection)
        binary_choice("Edit / Add some projects?", selected, project_choice_answer)
    else:
        tk.Label(root, text="Got to pick one, or use the manual loading").pack()
        binary_choice("Load an existing YSWS profile?", selected, ysws_init_load_answer)

def ysws_profile_init(offset):
    tk.Label(root, text="Hackatime Username: ").grid(row=0+offset, column=0)
    tk.Label(root, text="YSWS Hour Goal:").grid(row=1+offset, column=0)

    username_entry = tk.Entry(root)
    hours_entry = tk.Entry(root)
    
    username_entry.grid(row=0+offset, column=2)
    hours_entry.grid(row=1+offset, column=2)
    tk.Button(root, text="Submit", command=lambda: ysws_profile_init_answer(username_entry, hours_entry)).grid(row=2+offset, column=1)

def ysws_profile_init_answer(username_entry, hours_entry):
    username = username_entry.get()
    hours = hours_entry.get()

    for widget in root.winfo_children():
        widget.destroy()
    
    if username and hours:
        if func.init_ysws(username, hours) == False:
            tk.Label(root, text="Invalid Hackatime Username!").grid(row=0, column=1)
            ysws_profile_init(1)
        else:
            # After init, ask about editing projects
            binary_choice("Edit / Add some projects?", selected, project_choice_answer)
    else:
        tk.Label(root, text="You've got to fill in both!").grid(row=0, column=1)
        ysws_profile_init(1)

def binary_choice(header, variable, answer_function):
    tk.Label(root, text=header).pack()
    tk.Radiobutton(root, text="Yes", variable=variable, value="True").pack()
    tk.Radiobutton(root, text="No", variable=variable, value="False").pack()
    tk.Button(root, text="Submit", command=answer_function).pack()

def project_choice_answer(): # From binary choice
    selection = selected.get()
    for widget in root.winfo_children():
        widget.destroy()
    if selection == "True": # Edit the project list
        project_editing()
    elif selection == "False": # Skip Project setup
        get_days_left(0)
    else:
        tk.Label(root, text="You've got to pick one!").pack()
        binary_choice("Edit / Add some projects?", selected, project_choice_answer)

def project_editing():
    for widget in root.winfo_children():
        widget.destroy()
    func.init_project_list()
    scope = func.scope
    projects = func.names

    tk.Label(root, text="Which projects are being used in this YSWS?").pack()

    project_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
    
    for proj in projects: 
        project_listbox.insert(tk.END, proj)

    for i in range(project_listbox.size()):
        project_name = project_listbox.get(i)  
        if project_name in scope:
            project_listbox.selection_set(i)
    
    project_listbox.pack()
    tk.Button(root, text="Save", command=lambda: save_projects(project_listbox)).pack()

def save_projects(project_listbox):
    new_scope = [project_listbox.get(i) for i in project_listbox.curselection()]
    func.scope = new_scope
    for widget in root.winfo_children():
        widget.destroy()
    
    get_days_left(0)

def get_days_left(offset):
    tk.Label(root, text="How many days do you have till your hours are due? ").grid(row=0+offset, column=0)
    tk.Label(root, text="Pick one:").grid(row=1+offset, column=0)
    tk.Label(root, text="How many days ago did you start?").grid(row=2+offset, column=0)
    tk.Label(root, text="How many days did you have to start with?").grid(row=3+offset, column=0)

    days_left_entry = tk.Entry(root)
    days_ago_entry = tk.Entry(root)
    start_days_entry = tk.Entry(root)

    days_left_entry.grid(row=0+offset, column=2)
    days_ago_entry.grid(row=2+offset, column=2)
    start_days_entry.grid(row=3+offset, column=2)

    tk.Button(root, text="Submit", command=lambda: render_stats(days_left_entry, days_ago_entry, start_days_entry)).grid(row=4+offset, column=1)

def render_stats(days_left_entry, days_ago_entry, start_days_entry):
    global days_left, days_ago, start_days
    days_left = days_left_entry.get()
    days_ago = days_ago_entry.get()
    start_days = start_days_entry.get()
    
    for widget in root.winfo_children():
        widget.destroy()
    
    func.set_days_left(days_left)
      
    data = func.calculate_stats(days_left, days_ago, start_days)
    
    if data != False:
        tk.Label(root, text=f"Banked time: {datetime.timedelta(seconds=int(data[0]))}").pack()
        tk.Label(root, text=f"Target time: {datetime.timedelta(seconds=int(data[1]))}").pack()
        tk.Label(root, text=f"Time left: {datetime.timedelta(seconds=int(data[2]))}").pack()
        tk.Label(root, text=f"Required Daily code time: {datetime.timedelta(seconds=int(data[3]))}").pack()
        tk.Label(root, text=f"Percent complete: {round(data[4])}%").pack()   
        tk.Button(root, text="Save YSWS Profile", command=lambda: save_profile_init(0, days_left)).pack()
    else:
        tk.Label(root, text="Something's gone wrong...")

def save_profile_init(offset, days_left):
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="YSWS Name: ").grid(row=0+offset, column=0)
    tk.Label(root, text=f"Days left at the start (leave empty for {days_left}):").grid(row=1+offset, column=0)

    ysws_name_entry = tk.Entry(root)
    days_entry = tk.Entry(root)
    
    ysws_name_entry.grid(row=0+offset, column=2)
    days_entry.grid(row=1+offset, column=2)
    tk.Button(root, text="Submit", command=lambda: save_profile_init_answer(ysws_name_entry, days_entry, days_left)).grid(row=2+offset, column=1)

def save_profile_init_answer(ysws_name_entry, start_day_entry, default_days):
    ysws_name = ysws_name_entry.get()
    start_days = start_day_entry.get()
    
    for widget in root.winfo_children():
        widget.destroy()
    
    if ysws_name:  
        if start_days == "":
            start_days = default_days
        func.save_ysws(start_days, ysws_name)
        tk.Label(root, text="Saved!").pack()
        tk.Button(root, text="Back to Dashboard", command=lambda: render_stats_from_saved()).pack()
    else:
        tk.Label(root, text="You've got to fill in the YSWS name!").pack()
        root.after(1500, lambda: save_profile_init(1, default_days))

def render_stats_from_saved():
    for widget in root.winfo_children():
        widget.destroy()
    global days_left, days_ago, start_days
    func.calculate_stats(days_left, days_ago, start_days)
    
    total_time = func.total_time
    target = func.target
    delta = func.delta
    time_daily = func.time_daily
    percent_done = func.percent_done
    
    tk.Label(root, text=f"Banked time: {datetime.timedelta(seconds=int(total_time))}").pack()
    tk.Label(root, text=f"Target time: {datetime.timedelta(seconds=int(target))}").pack()
    tk.Label(root, text=f"Time left: {datetime.timedelta(seconds=int(delta))}").pack()
    tk.Label(root, text=f"Required Daily code time: {datetime.timedelta(seconds=int(time_daily))}").pack()
    tk.Label(root, text=f"Percent complete: {round(percent_done)}%").pack()

root = tk.Tk()
root.title("Blinky YSWS status thing")
selected = tk.StringVar(value="")
binary_choice("Load an existing YSWS profile?", selected, ysws_init_load_answer)
root.mainloop()