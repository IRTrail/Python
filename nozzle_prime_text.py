"""
This tool generates a nozzle prime macro for Klipper.
Quesitons or comments can be sent to irtrail@gmail.com
"""

import math


class Prime_Line:
    """
    This is an easy container for all the attributes, so they can be called anywhere.
    """

    def __init__(self, *args):
        self._m117_start_text = m117_start_text
        self._m117_end_text = m117_end_text
        self._start_position = start_position
        self._end_position = end_position
        self._layer_height = layer_height
        self._feedrate = feedrate
        self._rapid_feedrate = rapid_feedrate
        self._nozzle_diameter = nozzle_diameter
        self._line_width_factor = line_width_factor
        self._retract_distance = retract_distance


def main():
    """
    Get inputs from user and stashes it in Prime_Line
    """

    # M117 Section
    Prime_Line.m117_start_text: str = input("M117 starting text: ")
    Prime_Line.m117_end_text: str = input("M117 ending text: ")

    # Start and End Section
    while True:
        start_position: list = input("Starting position: ").split()
        end_position: list = input("Ending position: ").split()
        try:
            Prime_Line.start_position = list(map(float, start_position))
            Prime_Line.end_position = list(map(float, end_position))
            if not len(start_position) == 2 or not len(end_position) == 2:
                raise IndexError
            break
        except ValueError:
            print("X and Y start positions must be two numbers separated by a space.")
        except IndexError:
            print("X and Y start positions must have two numbers.")
        except Illegal:
            print("Something isn't entered correctly, let's try again.")

    # Print Parameters Section
    while True:
        try:
            Prime_Line.layer_height = float(input("Layer height: "))
            Prime_Line.feedrate = float(input("Feedrate: "))
            Prime_Line.rapid_feedrate = float(input("Rapid feedrate: "))
            Prime_Line.nozzle_diameter = float(input("Nozzle diameter: "))
            if Prime_Line.layer_height > Prime_Line.nozzle_diameter:
                raise ValueError("Layer height cannot be larger than nozzle diameter")
            Prime_Line.line_width_factor = float(input("Line width factor: "))
            Prime_Line.retract_distance = float(input("Retract distance: "))
            break
        except ValueError:
            print(
                "Layer height, Feedrate, Rapid feedrate, Nozzle diameter, Line width factor, and Retract distance must all be floating type numbers."
            )
        except Illegal:
            print("Something went wrong. Let's try again.")

    make_macro(Prime_Line)


def make_macro(pl):
    """
    Outputs Prime_Line attributes to a text file formatted as a Klipper Macro
    """

    e_move = extrusion_calculation(pl)
    x_start = pl.start_position[0]
    y_start = pl.start_position[1]
    x_end = pl.end_position[0]
    y_end = pl.end_position[1]
    z_height = pl.layer_height
    rapid = pl.rapid_feedrate
    feed = pl.feedrate
    retract = pl.retract_distance
    tab = "\t"
    file_text = [
        f"[gcode_macro NOZZLE_PRIME]",
        f"# Nozzle Prime Macro created by:",
        f"# Nozzle Prime Macro Maker",
        f"# https://github.com/IRTrail/Apps",
        f"gcode:",
        f"{tab}M117 {pl.m117_start_text}",
        f"{tab}G92 E0{tab * 9};Reset Extruder",
        f"{tab}G0 X{x_start} Y{y_start} Z10. F{rapid * 60}{tab * 4}; Move to start position",
        f"{tab}G1 X{x_start} Y{y_start} Z2. F{int(rapid * 60)/2}",
        f"{tab}G1 X{x_start} Y{y_start} Z{z_height} F{feed * 60}",
        f"{tab}G1 X{x_end} Y{y_end} Z{z_height} F{feed * 60} E{e_move:.3f}{tab * 2}; Purge nozzle",
        f"{tab}E-{retract} F1800{tab * 8}; Retract",
        f"{tab}G92 E0{tab * 9}; Reset Extruder",
        f"{tab}G1 Z2. F{rapid * 60}{tab * 7}; Move Z up to prevent scratching",
        f"{tab}M117 {pl.m117_end_text}",
    ]

    with open("nozzle_prime.cfg", "w") as f:
        f.writelines("\n".join(file_text))


def extrusion_calculation(pl):
    """Calculates extrusion number
    Returns:
        e (float): extrusion distance
    """
    D = pl.nozzle_diameter
    W = pl.line_width_factor * D
    T = pl.layer_height
    L = line_length(pl)

    e = ((math.pi * T**2) / 4 + T * W - T**2) * L
    return e


def line_length(pl):
    """Calculates line distance...because Pythagorus.
    Returns:
        float: line distance
    """
    x1 = pl.start_position[0]
    y1 = pl.start_position[1]
    x2 = pl.end_position[0]
    y2 = pl.end_position[1]
    return ((x2 - x1) ** 2 + (y2 - y1)**2) ** (1 / 2)

if __name__ == "__main__":
    main()