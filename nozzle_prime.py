"""
This tool generates a nozzle prime macro for Klipper.
The GUI includes necessary entries and explainations.
Quesitons or comments can be sent to irtrail@gmail.com
"""

import math
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk

# Set up the main window
root = ThemedTk(theme="breeze")
root.title("Nozzle Prime Macro Maker")

# Create Style object for button
button_style = ttk.Style()
button_style.configure("q.TButton", foreground="red")

# M117 Section
entry_frame = ttk.Frame(root)
m117_start_label = ttk.Label(entry_frame, text="M117 starting text:")
m117_start_label.grid(row=0, column=0, padx=(5, 0), sticky=tk.W)
m117_start_entry = ttk.Entry(entry_frame)
m117_start_entry.grid(row=0, column=1, columnspan=3, sticky=tk.W + tk.E)

m117_end_label = ttk.Label(entry_frame, text="M117 ending text:")
m117_end_label.grid(row=1, column=0, padx=(5, 0), sticky=tk.W)
m117_end_entry = ttk.Entry(entry_frame)
m117_end_entry.grid(row=1, column=1, columnspan=3, sticky=tk.W + tk.E)

# Start and End Section
start_x_label = ttk.Label(entry_frame, text="Starting X postion:")
start_x_label.grid(row=3, column=0, padx=(5, 0))
start_x_entry = ttk.Entry(entry_frame)
start_x_entry.grid(row=3, column=1)

start_y_label = ttk.Label(entry_frame, text="Starting Y position:")
start_y_label.grid(row=4, column=0, padx=(5, 0))
start_y_entry = ttk.Entry(entry_frame)
start_y_entry.grid(row=4, column=1)

ending_x_label = ttk.Label(entry_frame, text="Ending X position:")
ending_x_label.grid(row=3, column=2, padx=(5, 0))
ending_x_entry = ttk.Entry(entry_frame)
ending_x_entry.grid(row=3, column=3)

ending_y_label = ttk.Label(entry_frame, text="Ending Y position:")
ending_y_label.grid(row=4, column=2, padx=(5, 0))
ending_y_entry = ttk.Entry(entry_frame)
ending_y_entry.grid(row=4, column=3)

# Print Parameters Section
layer_height_label = ttk.Label(entry_frame, text="Layer height:")
layer_height_label.grid(row=6, column=0, padx=(5, 0))
layer_height_entry = ttk.Entry(entry_frame)
layer_height_entry.grid(row=6, column=1)

feedrate_label = ttk.Label(entry_frame, text="Feedrate:")
feedrate_label.grid(row=7, column=0, padx=(5, 0))
feedrate_entry = ttk.Entry(entry_frame)
feedrate_entry.grid(row=7, column=1)

rapid_feedrate_label = ttk.Label(entry_frame, text="Rapid feedrate:")
rapid_feedrate_label.grid(row=8, column=0, padx=(5, 0))
rapid_feedrate_entry = ttk.Entry(entry_frame)
rapid_feedrate_entry.grid(row=8, column=1)

nozzle_diameter_label = ttk.Label(entry_frame, text="Nozzle diameter:")
nozzle_diameter_label.grid(row=6, column=2, padx=(5, 0))
nozzle_diameter_entry = ttk.Entry(entry_frame)
nozzle_diameter_entry.grid(row=6, column=3)

line_width_factor_label = ttk.Label(entry_frame, text="Line width factor:")
line_width_factor_label.grid(row=7, column=2, padx=(5, 0))
line_width_factor_entry = ttk.Entry(entry_frame)
line_width_factor_entry.grid(row=7, column=3)

retract_label = ttk.Label(entry_frame, text="Retract distance:")
retract_label.grid(row=8, column=2, padx=(5, 0))
retract_entry = ttk.Entry(entry_frame)
retract_entry.grid(row=8, column=3)

# Create Separators
m117_separator = ttk.Separator(entry_frame, orient=tk.HORIZONTAL)
m117_separator.grid(row=2, columnspan=4, pady=4, sticky=tk.EW)

start_position_separator = ttk.Separator(entry_frame, orient=tk.HORIZONTAL)
start_position_separator.grid(row=5, columnspan=4, pady=4, sticky=tk.EW)

entry_frame.grid(row=0, column=0)


# Create text box
gcode_frame = ttk.LabelFrame(root, text="G Code")
output_text_box = tk.Text(gcode_frame, height=14, wrap='none')
output_text_box.grid(row=0, column=0, sticky=tk.N + tk.S + tk.W)
scrollbar = ttk.Scrollbar(
    gcode_frame, orient=tk.VERTICAL, command=output_text_box.yview
)
scrollbar.grid(row=0, column=1, sticky=tk.NS)
gcode_frame.grid(row=0, column=4, pady=(0, 5))

# Create Buttons
button_frame = ttk.Frame(root)

calculate_button = ttk.Button(button_frame, text="Calculate")
calculate_button.grid(row=0, column=0)

copy_button = ttk.Button(button_frame, text="Copy")
copy_button.grid(row=0, column=1)

quit_button = ttk.Button(button_frame, text="Quit", style="q.TButton")
quit_button.grid(row=0, column=2, sticky=tk.E)

button_frame.grid(row=10, column=4, sticky=tk.E, padx=(0,5), pady=(0,5))


def make_macro():
    """Puts all the lines in the output text widget
    """    
    e_move = extrusion_calculation()
    x_start = float(start_x_entry.get())
    y_start = float(start_y_entry.get())
    x_end = float(ending_x_entry.get())
    y_end = float(ending_y_entry.get())
    z_height = float(layer_height_entry.get())
    rapid = float(rapid_feedrate_entry.get())
    feed = float(feedrate_entry.get())
    retract = float(retract_entry.get())
    tab = "\t"

    file_text = [
        f"[gcode_macro NOZZLE_PRIME]",
        f"# Nozzle Prime Macro created by:",
        f"# Nozzle Prime Macro Maker",
        f"# https://github.com/IRTrail/Apps",
        f"gcode:",
        f"{tab}M117 {m117_start_entry.get()}",
        f"{tab}G92 E0{tab * 9};Reset Extruder",
        f"{tab}G0 X{x_start} Y{y_start} Z10. F{rapid * 60}{tab * 5}; Move to start position",
        f"{tab}G1 X{x_start} Y{y_start} Z2. F{(rapid * 60)/2}",
        f"{tab}G1 X{x_start} Y{y_start} Z{z_height:.3g} F{feed * 60}",
        f"{tab}G1 X{x_end} Y{y_end} Z{z_height:.3g} F{feed * 60} E{e_move:.3f}{tab * 3}; Purge nozzle",
        f"{tab}E-{retract:.3g} F1800{tab * 8}; Retract",
        f"{tab}G92 E0{tab * 9}; Reset Extruder",
        f"{tab}G1 Z2. F{rapid * 60}{tab * 7}; Move Z up to prevent scratching",
        f"{tab}M117 {m117_end_entry.get()}",
    ]
    output_text_box.insert(tk.END, "\n".join(file_text))


def extrusion_calculation():
    """Calculates extrusion number

    Returns:
        e (float): extrusion distance
    """    
    try:
        D = float(nozzle_diameter_entry.get())
        W = float(line_width_factor_entry.get()) * D
        T = float(layer_height_entry.get())
        L = line_length()

        print(L)
        print(type(L))
        if T < D:
            e = ((math.pi * T**2) / 4 + T * W - T**2) * L
            return e
        else:
            output_text_box.configure(
                text="The extrusion height is greater than nozzle diameter."
            )
    except ValueError:
        output_text_box.configure(text="Error: One of the entries is not numeric!")


def line_length():
    """Calculates line distance

    Returns:
        float: line distance
    """    
    x1 = float(start_x_entry.get())
    y1 = float(start_y_entry.get())
    x2 = float(ending_x_entry.get())
    y2 = float(ending_y_entry.get())
    return ((x2 - x1) ** 2 + (y2 - y1**2)) ** (1 / 2)


def copy_result():
    """Copies result to clipboard
    """    
    result = output_text_box.get("1.0", tk.END)
    root.clipboard_clear()
    root.clipboard_append(result)

def set_width(text_box):
    """Calculates length in characters of the longest line in the text box widget

    Args:
        text_box (tk text widget): Text box widget

    Returns:
        m (int): length of longest line
    """    
    line_num = int(text_box.index('end-1c').split('.')[0])
    m = 0
    for i in range(line_num):
        l = len(text_box.get(f"{i}.0", f"{i}.0 lineend"))
        if l > m:
            m = l
        return m


# Control textbox with scrollbar
output_text_box["yscrollcommand"] = scrollbar.set

copy_button.configure(command=copy_result)
calculate_button.configure(command=make_macro)
quit_button.configure(command=root.destroy)


root.mainloop()