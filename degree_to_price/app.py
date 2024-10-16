import os
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from tkinter.messagebox import *

from tksheet import Sheet

from main import *


class App:
    def __init__(self, root):
        self.longitude_equivalents = None
        self.selected_system_var = tk.BooleanVar()
        self.selected_factor_var = tk.IntVar(value=360)
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

        tk.Label(root, font=ft, text="upper lim", bg=self.global_background, fg="black").place(x=20, y=85, width=60,
                                                                                               height=25)
        # indicator upper limit value entry
        self.upper_lim_value_entry = ttk.Entry(root)
        ft = tkFont.Font(family='Times', size=10)
        self.upper_lim_value_entry["font"] = ft
        self.upper_lim_value_entry["justify"] = "left"
        self.upper_lim_value_entry.place(x=85, y=85, width=45, height=25)

        tk.Label(root, font=ft, text="lower lim", bg=self.global_background, fg="black", ).place(x=20, y=115, width=60,
                                                                                                 height=25)
        # indicator lower limit value entry
        self.lower_lim_value_entry = ttk.Entry(root)
        ft = tkFont.Font(family='Times', size=10)
        self.lower_lim_value_entry["font"] = ft
        self.lower_lim_value_entry["justify"] = "left"
        self.lower_lim_value_entry.place(x=85, y=115, width=45, height=25)

        # heliocentric/ geocentric radio buttons
        systems = (("helio", True), ("geo", False))
        self.helio_radio_button = tk.Radiobutton(root, bg=self.global_background, fg="black", borderwidth=0, border=0,
                                                 text=systems[0][0], value=systems[0][1],
                                                 variable=self.selected_system_var)
        self.geo_radio_button = tk.Radiobutton(root, bg=self.global_background, fg="black", borderwidth=0, border=0,
                                               text=systems[1][0], value=systems[1][1],
                                               variable=self.selected_system_var)
        self.helio_radio_button.place(x=20, y=145, width=110, height=25)
        self.geo_radio_button.place(x=20, y=175, width=110, height=25)

        tk.Label(root, font=ft, text="Factor:", bg=self.global_background, fg="black", anchor="w").place(x=20, y=205,
                                                                                                         width=110,
                                                                                                         height=25)

        # factors
        factors = (("Conj(360)", 360),("Opp(180)", 180),("Sq(90)",90))
        self.conj_radio_button = tk.Radiobutton(root,bg=self.global_background,fg="black",borderwidth=0,border=0,
                                               text=factors[0][0],value=factors[0][1],variable=self.selected_factor_var)
        self.opp_radio_button = tk.Radiobutton(root, bg=self.global_background, fg="black", borderwidth=0, border=0,
                                               text=factors[1][0], value=factors[1][1],variable=self.selected_factor_var)
        self.sq_radio_button = tk.Radiobutton(root, bg=self.global_background, fg="black", borderwidth=0, border=0,
                                               text=factors[2][0], value=factors[2][1],variable=self.selected_factor_var)
        self.conj_radio_button.place(x=20, y=235, width=110, height=25)
        self.opp_radio_button.place(x=20, y=265, width=110, height=25)
        self.sq_radio_button.place(x=20, y=295, width=110, height=25)

        # submit values
        self.submit_values_button = ttk.Button(root, text="submit values",
                                               command=self.submit_values)
        self.submit_values_button.place(x=20, y=325, width=110, height=25)

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
        factor = self.selected_factor_var.get()
        upper_limit = self.upper_lim_value_entry.get()
        lower_limit = self.lower_lim_value_entry.get()

        # error handling
        if len(start_date_str) == 0:
            showwarning(title="Start Date Error",message="start date can't be empty !")
            return
        if not re.fullmatch(r"^[\d|.]+", start_date_str):
            showwarning(title="Start Date Error", message="start date can only contain digits and dot (.) character")
            return
        if len(price) == 0 or len(upper_limit) == 0 or len(lower_limit) == 0:
            showwarning(title="Price Value Error", message="Fill in all price fields !")
            return
        elif not price.isdigit() or not upper_limit.isdigit() or not lower_limit.isdigit():
            showwarning(title="Price Value Error", message="price fields must be digits only !")
            return

        planet_longitudes = get_planet_longitudes(is_heliocentric=is_helio, year=int(split_date[0]),
                                                  month=int(split_date[1]),
                                                  day=int(split_date[2]))
        self.planet_longitudes.set_sheet_data(data=planet_longitudes)

        self.prices.set_sheet_data(data=self.add_only_planetary_squares(int(price), planet_longitudes, factor))
        self.prices.show(canvas="row_index")
        self.export_indicator()

    def export_indicator(self):
        flatted_data = [val for sublist in self.longitude_equivalents for val in sublist]
        upper_limit = int(self.upper_lim_value_entry.get())
        lower_limit = int(self.lower_lim_value_entry.get())
        values_in_range = [x for x in flatted_data if lower_limit <= x <= upper_limit]
        indicator_placeholder = f"//@version=5\nindicator(\"Degree to Price-{self.start_date_entry.get()}-{get_selected_system(self.selected_system_var.get())}\", overlay = true)"
        for index, long_equal in enumerate(values_in_range):
            indicator_placeholder += f"\nval{index} = input.float(title = \"value {index}\", defval = {long_equal}, step = 0.01)\nplot( val{index} , title = \"Degree to Price\", color = color.white, show_last=1, linewidth = 2, trackprice=true)"
        if os.path.exists("indicator.txt"):
            os.remove("indicator.txt")
        with open('indicator.txt', 'w') as f:
            f.write(indicator_placeholder)
            f.close()


    def add_only_planetary_squares(self,price, planet_longitudes, factor):
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
        values = get_only_planetary_squares(ceiled_longitudes,price,factor)
        self.longitude_equivalents = get_only_planetary_squares(ceiled_longitudes,price,factor)
        planet_labels = [str(ceiled_longitudes[index]) + " " + str(new_planets[index]) for index, _ in enumerate(ceiled_longitudes)]
        values.insert(0,planet_labels)
        return values

def get_selected_system(value:bool):
    return "Helio" if value else "Geo"

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
