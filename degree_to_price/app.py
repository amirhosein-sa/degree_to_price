import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from tkinter.messagebox import *

from tksheet import Sheet

from main import *


class App:
    def __init__(self, root):
        self.selected_system_var = tk.BooleanVar()
        self.global_background = "#fcf5e1"
        # setting title
        root.title("Degree To Price - by Amirhosein Salari - t.me/amirhosein_sa")
        ft = tkFont.Font(family='Times', size=10)
        # setting window size
        width = 700
        height = 500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        align_str = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(align_str)
        root.resizable(width=False, height=False)
        root.configure(background=self.global_background)

        # planet longitudes
        self.planet_longitudes = Sheet(root,
                                       empty_vertical=0, empty_horizontal=0,
                                       show_top_left=False,
                                       show_header=False,
                                       column_width=70,
                                       show_row_index=False
                                       )
        self.planet_longitudes.change_theme(theme ="light_green")
        self.planet_longitudes.place(x=135, y=20, width=550, height=60)

        tk.Label(root, font=ft, text="Date:", bg=self.global_background, fg="black").place(x=20, y=20, width=35, height=25)
        # start date entry
        self.start_date_entry = ttk.Entry(root)
        self.start_date_entry["font"] = ft
        self.start_date_entry["justify"] = "center"
        self.start_date_entry["text"] = "Start date"
        self.start_date_entry.place(x=60, y=20, width=70, height=25)

        tk.Label(root, font=ft, text="Price:", bg=self.global_background, fg="black").place(x=20, y=50, width=35, height=25)
        # price value entry
        self.price_value_entry = ttk.Entry(root)
        ft = tkFont.Font(family='Times', size=10)
        self.price_value_entry["font"] = ft
        self.price_value_entry["justify"] = "center"
        self.price_value_entry["text"] = "Price"
        self.price_value_entry.place(x=60, y=50, width=70, height=25)

        # heliocentric/ geocentric radio buttons
        systems = (("helio", True), ("geo", False))
        self.helio_radio_button = tk.Radiobutton(root, bg=self.global_background, fg="black", borderwidth=0, border=0,
                                                 text=systems[0][0], value=systems[0][1],
                                                 variable=self.selected_system_var)
        self.geo_radio_button = tk.Radiobutton(root, bg=self.global_background, fg="black", borderwidth=0, border=0,
                                               text=systems[1][0], value=systems[1][1],
                                               variable=self.selected_system_var)
        self.helio_radio_button.place(x=20, y=85, width=110, height=25)
        self.geo_radio_button.place(x=20, y=115, width=110, height=25)

        # submit values and get data button
        self.submit_values_button = ttk.Button(root, text="submit values",
                                               command=self.submit_values)
        self.submit_values_button.place(x=20, y=145, width=110, height=25)

        # prices list
        self.prices = Sheet(root, show_header=False,
                            row_index=[' ' for i in range(360)],
                            row_index_width=15,
                            column_width=70,
                            show_top_left=False)
        self.prices.hide(canvas="row_index")
        self.prices.enable_bindings("row_select","single_select")

        self.prices.change_theme(theme = "light_green")
        self.prices.place(x=135, y=85, width=550, height=366)

    def submit_values(self):
        start_date_str = self.start_date_entry.get()
        split_date = start_date_str.split(".")
        is_helio = self.selected_system_var.get()
        price = self.price_value_entry.get()

        if len(start_date_str) == 0:
            showwarning(title="Start Date Error",message="start date can't be empty !")
            return
        if not re.fullmatch(r"^[\d|.]+", start_date_str):
            showwarning(title="Start Date Error", message="start date can only contain digits and dot (.) character")
            return
        if len(price) == 0:
            showwarning(title="Price Value Error", message="price can't be empty !")
            return
        if not price.isdigit():
            showwarning(title="Price Value Error", message="price must be digits only !")
            return
        elif int(price) <= 360:
            showwarning(title="Price Value Error", message="price must greater than 360 !")
            return

        planet_longitudes = get_planet_longitudes(is_heliocentric=is_helio, year=int(split_date[0]),
                                                  month=int(split_date[1]),
                                                  day=int(split_date[2]))
        prices = get_values(price=int(price))
        self.planet_longitudes.set_sheet_data(data=planet_longitudes)
        self.prices.set_sheet_data(data=add_longitudes(prices,planet_longitudes))
        self.prices.show(canvas="row_index")

def add_longitudes(values: list,planet_longitudes:list):
    planets = planet_longitudes[0]
    longitudes = planet_longitudes[-1]
    new_planets = []
    # sorting longitudes
    sorted_planet_longitudes = sorted(longitudes)
    # sorting planets based on their longitudes
    for index,long in enumerate(sorted_planet_longitudes):
        longitude_index_in_main_list = longitudes.index(long)
        new_planets.append(planets[longitude_index_in_main_list])
    # rounding
    ceiled_longitudes = [HalfRoundUp(c) for c in sorted_planet_longitudes]
    # replacing 360 with 0 to resolve the bug [Bug: if a planet degree was 360, app would crash]
    ceiled_longitudes = [0 if long == 360 else long for long in ceiled_longitudes]
    # creating a 360 items list from character "-"
    planet_longitudes_placeholder = ["-" for char in range(360)]
    for index in range(len(ceiled_longitudes)):
        planet_longitudes_placeholder[ceiled_longitudes[index]] = str(ceiled_longitudes[index]) + " " + str(new_planets[index])
    values.append(planet_longitudes_placeholder)
    transposed_values = transpose_values(values)
    return transposed_values

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
