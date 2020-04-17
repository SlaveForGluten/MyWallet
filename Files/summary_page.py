"""calculate and display total worth of currencies and shares"""

import tkinter as tk

from Files import (calculate, assets_page, shares_page,
                   watched_page, settings_page)


FONT = "Calabria 12"


class Summary(tk.Frame):
    """create a summary page, create buttons invoking other frames/pages"""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="SUMMARY:", font="Calabria 12 bold")
        label.grid(sticky="nw")

        button = tk.Button(
            self, text="  Liquid Assets  ", bg="yellow", font=FONT,
            command=lambda: controller.show_frame(assets_page.Assets))
        button.grid(row=2, column=2, sticky="e")

        p1_button = tk.Button(
            self, text="   GPW Share    ", bg="lawn green", font=FONT,
            command=lambda: controller.show_frame(shares_page.Shares))
        p1_button.grid(row=3, column=2, sticky="e")

        p2_button = tk.Button(
            self, text="Watched shares", bg="seashell3", font=FONT,
            command=lambda: controller.show_frame(watched_page.Watched))
        p2_button.grid(row=4, column=2, sticky="e")

        summary_button = tk.Button(self, text="      Summary      ",
                                   relief=tk.SUNKEN, font=FONT, bg="hot pink")
        summary_button.grid(row=5, column=2, sticky="e")

        p4_button = tk.Button(
            self, text="       Settings       ", bg="DeepSkyBlue2", font=FONT,
            command=lambda: controller.show_frame(settings_page.Settings))
        p4_button.grid(row=6, column=2, sticky="e")

        Summary.populate_frame(self)

    def populate_frame(parent):
        """display all the values"""
        added_values = calculate.add_liquid_assets()
        shares_worth_totaled = calculate.totaled_shares_worth()
        total = calculate.sum_all_wealth()

        frame = tk.Frame(parent, width=800, height=300)
        frame.grid(row=1, column=0, sticky="w", rowspan=20)

        label = tk.Label(
            frame, text="Liquid Assets:"+" "*180, font="Calabria 10 bold")
        label.grid(sticky="nw")
        label = tk.Label(
            frame, text=str(added_values['pln'])+" PLN", font="Calabria 10")
        label.grid(sticky="nw")
        label = tk.Label(
            frame, text=str(added_values['eur'])+" EUR", font="Calabria 10")
        label.grid(sticky="nw")
        label = tk.Label(
            frame, text=str(added_values['gbp'])+" GBP", font="Calabria 10")
        label.grid(sticky="nw")
        label = tk.Label(
            frame, text=str(added_values['usd'])+" USD", font="Calabria 10")
        label.grid(sticky="nw")
        label = tk.Label(
            frame, text=str(added_values['chf'])+" CHF", font="Calabria 10")
        label.grid(sticky="nw")
        label = tk.Label(
            frame, text="Shares:", font="Calabria 10 bold")
        label.grid(sticky="nw")
        label = tk.Label(
            frame, text=str(round(shares_worth_totaled, 2))+"  PLN", font="Calabria 10")
        label.grid(sticky="nw")
        label = tk.Label(frame, text="Total:", font="Calabria 10 bold")
        label.grid(sticky="nw")
        label = tk.Label(
            frame, text=str(round(total, 2))+" PLN", font="Calabria 10")
        label.grid(sticky="nw")
