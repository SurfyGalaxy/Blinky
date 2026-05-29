import functions as func
import tkinter as tk
loaded = func.load_ysws()
if not loaded:
    func.init_ysws()
func.update_days()
if input(f"Update project list? (True or press enter to skip)") != "":
    func.edit_projects()

func.calculate_stats()
func.print_stats()

func.save_ysws()