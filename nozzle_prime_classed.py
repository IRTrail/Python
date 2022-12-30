"""
This tool generates a nozzle prime macro for Klipper.
The GUI includes necessary entries and explainations.
Quesitons or comments can be sent to irtrail@gmail.com
"""

import math
import tkinter as tk
from tkinter import ttk
import customtkinter

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # Create frames
        self.entry_frame = customtkinter.CTkFrame(self)
        self.entry_frame.grid(row=0, column=0)
        self.gcode_frame = customtkinter.CTkFrame(self)
        self.gcode_frame.grid(row=0, column=4, pady=(0, 5))
        self.button_frame = customtkinter.CTkFrame(self, border_width=2)
        self.button_frame.grid(row=10, column=3, columnspan=2, sticky=tk.W, padx=(0, 5), pady=(0, 5))

        self.title("Nozzle Prime Macro Maker")

        # configure grid layout (4x4)
        self.grid_columnconfigure(4, weight=1)
        self.grid_columnconfigure((0, 1, 2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # M117 Section
        self.m117_start_label = customtkinter.CTkLabel(self.entry_frame, text="M117 starting text:")
        self.m117_start_label.grid(row=0, column=0, padx=(5, 0), sticky=tk.W)
        self.m117_start_entry = customtkinter.CTkEntry(self.entry_frame, placeholder_text="Display this text while running.")
        self.m117_start_entry.grid(row=0, column=1, columnspan=3, sticky=tk.W + tk.E)

        self.m117_end_label = customtkinter.CTkLabel(self.entry_frame, text="M117 ending text:")
        self.m117_end_label.grid(row=1, column=0, padx=(5, 0), sticky=tk.W)
        self.m117_end_entry = customtkinter.CTkEntry(self.entry_frame, placeholder_text="Display this text when complete.")
        self.m117_end_entry.grid(row=1, column=1, columnspan=3, sticky=tk.W + tk.E)

        # Start and End Section
        self.start_label = customtkinter.CTkLabel(self.entry_frame, text="Starting postion:")
        self.start_label.grid(row=3, column=0, padx=(5, 0))
        self.start_entry = customtkinter.CTkEntry(self.entry_frame, placeholder_text="X, Y")
        self.start_entry.grid(row=3, column=1)

        self.ending_label = customtkinter.CTkLabel(self.entry_frame, text="Ending position:")
        self.ending_label.grid(row=3, column=2, padx=(5, 0))
        self.ending_entry = customtkinter.CTkEntry(self.entry_frame, placeholder_text="X, Y")
        self.ending_entry.grid(row=3, column=3)

        # Print Parameters Section
        self.layer_height_label = customtkinter.CTkLabel(self.entry_frame, text="Layer height:")
        self.layer_height_label.grid(row=6, column=0, padx=(5, 0))
        self.layer_height_entry = customtkinter.CTkEntry(self.entry_frame, placeholder_text="in mm")
        self.layer_height_entry.grid(row=6, column=1)

        self.feedrate_label = customtkinter.CTkLabel(self.entry_frame, text="Feedrate:")
        self.feedrate_label.grid(row=7, column=0, padx=(5, 0))
        self.feedrate_entry = customtkinter.CTkEntry(self.entry_frame, placeholder_text="in mm/s")
        self.feedrate_entry.grid(row=7, column=1)

        self.rapid_feedrate_label = customtkinter.CTkLabel(self.entry_frame, text="Rapid feedrate:")
        self.rapid_feedrate_label.grid(row=8, column=0, padx=(5, 0))
        self.rapid_feedrate_entry = customtkinter.CTkEntry(self.entry_frame, placeholder_text="in mm/s")
        self.rapid_feedrate_entry.grid(row=8, column=1)

        self.nozzle_diameter_label = customtkinter.CTkLabel(self.entry_frame, text="Nozzle diameter:")
        self.nozzle_diameter_label.grid(row=6, column=2, padx=(5, 0))
        self.nozzle_diameter_entry = customtkinter.CTkEntry(self.entry_frame, placeholder_text="in mm")
        self.nozzle_diameter_entry.grid(row=6, column=3)

        self.line_width_factor_label = customtkinter.CTkLabel(self.entry_frame, text="Line width factor:")
        self.line_width_factor_label.grid(row=7, column=2, padx=(5, 0))
        self.line_width_factor_entry = customtkinter.CTkEntry(self.entry_frame, placeholder_text="* nozzle diameter")
        self.line_width_factor_entry.grid(row=7, column=3)

        self.retract_label = customtkinter.CTkLabel(self.entry_frame, text="Retract distance:")
        self.retract_label.grid(row=8, column=2, padx=(5, 0))
        self.retract_entry = customtkinter.CTkEntry(self.entry_frame, placeholder_text="in mm")
        self.retract_entry.grid(row=8, column=3)

        # Create Separators
        self.m117_separator = ttk.Separator(self.entry_frame, orient=tk.HORIZONTAL)
        self.m117_separator.grid(row=2, columnspan=4, pady=4, sticky=tk.EW)
        self.start_position_separator = ttk.Separator(self.entry_frame, orient=tk.HORIZONTAL)
        self.start_position_separator.grid(row=5, columnspan=4, pady=4, sticky=tk.EW)

        # Create text box
        self.output_text_box = customtkinter.CTkTextbox(self.gcode_frame, width=254, wrap="none")
        self.output_text_box.grid(row=0, column=0, sticky=tk.N + tk.S + tk.W)

        # Create Buttons
        self.calculate_button = customtkinter.CTkButton(self.button_frame, text="Calculate")
        self.calculate_button.grid(row=0, column=0, padx=4)

        self.copy_button = customtkinter.CTkButton(self.button_frame, text="Copy")
        self.copy_button.grid(row=0, column=1, padx=4)

        self.quit_button = customtkinter.CTkButton(self.button_frame, text="Quit")
        self.quit_button.grid(row=0, column=2, padx=4, sticky=tk.NSEW)

        self.copy_button.configure(command=copy_result)
        self.calculate_button.configure(command=make_macro)
        self.quit_button.configure(command=self.destroy)


def make_macro():
    """Puts all the lines in the output text widget"""
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
    """Copies result to clipboard"""
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
    line_num = int(text_box.index("end-1c").split(".")[0])
    m = 0
    for i in range(line_num):
        l = len(text_box.get(f"{i}.0", f"{i}.0 lineend"))
        if l > m:
            m = l
        return m

# Set up the main window
if __name__ == "__main__":
    app = App()
    app.mainloop()
