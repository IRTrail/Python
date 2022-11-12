"""
This is a quick tool to calculate extrusion length based on nozzle width,
layer height, and line length.
"""

import tkinter as tk
import math

from ttkthemes import ThemedTk, THEMES
from tkinter import ttk

root = ThemedTk(theme="plastik")
root.title("Extrusion Length Calculator")
root.columnconfigure(1, weight=1)

# Create Style object for button
button_style = ttk.Style()
button_style.configure("q.TButton", foreground="red")

# Create Labels
nozzle_dia_label = ttk.Label(root, text="Nozzle Diameter:")
nozzle_dia_label.grid(row=0, column=0, sticky=tk.E, pady=2.5)

line_width_label = ttk.Label(root, text="Line Width Factor:")
line_width_label.grid(row=1, column=0, sticky=tk.E, pady=2.5)

line_note_label = ttk.Label(root, text="(Factor of Nozzle Diameter)")
line_note_label.grid(
    row=2,
    column=0,
    columnspan=2,
    sticky=tk.W + tk.E,
)
line_note_label.configure(anchor="center")

layer_thickness_label = ttk.Label(root, text="Layer Thickness:")
layer_thickness_label.grid(row=3, column=0, sticky=tk.E, pady=2.5)

line_length_label = ttk.Label(root, text="Line Length:")
line_length_label.grid(row=4, column=0, sticky=tk.E, pady=2.5)

# Create Entry Widgets
nozzle_dia_entry = ttk.Entry(root)
nozzle_dia_entry.grid(row=0, column=1, sticky=tk.W + tk.E)

line_width_entry = ttk.Entry(root)
line_width_entry.grid(row=1, column=1, sticky=tk.W + tk.E)

layer_thickness_entry = ttk.Entry(root)
layer_thickness_entry.grid(row=3, column=1, sticky=tk.W + tk.E)

line_length_entry = ttk.Entry(root)
line_length_entry.grid(row=4, column=1, sticky=tk.W + tk.E)

# Create results label
results_label = ttk.Label(root, text="")
results_label.grid(row=5, column=0, columnspan=3, sticky=tk.E + tk.W)
results_label.configure(anchor="center")

# Create Calculate Button
calculate_button = ttk.Button(root, text="Calculate")
calculate_button.grid(
    row=99, column=1, padx=5, pady=5, ipadx=1, ipady=1
)

# Create Copy Button
copy_button = ttk.Button(root, text="Copy Result to Clipboard")
copy_button.grid(row=99, column=0, sticky=tk.E + tk.W, padx=5, pady=5, ipadx=1, ipady=1)

# Create quit button
quit_button = ttk.Button(root, text="Quit", style="q.TButton")
quit_button.grid(row=99, column=2, padx=5, pady=5, ipadx=1, ipady=1)


def extrusion_calculation():
    """Calculates the resulting extrusion number"""
    try:
        D = float(nozzle_dia_entry.get())
        W = float(line_width_entry.get()) * D
        T = float(layer_thickness_entry.get())
        L = float(line_length_entry.get())

        if T < D:
            e_length = ((math.pi * T**2) / 4 + T * W - T**2) * L
            results_label.configure(text="Extruder Move: E" + str(e_length))
        else:
            results_label.configure(text="The extrusion height is greater than nozzle diameter.")
    except ValueError:
        results_label.configure(text="Error: One of the entries is not numeric!")


def copy_result():
    result = results_label.cget("text")
    result = result.split(':')
    result = result[1].strip()

    root.clipboard_clear()
    root.clipboard_append(result)


calculate_button.configure(command=extrusion_calculation)
copy_button.configure(command=copy_result)
quit_button.configure(command=root.destroy)

root.mainloop()
