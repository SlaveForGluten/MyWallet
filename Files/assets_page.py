"""create assets frame"""

import tkinter as tk
from tkinter import scrolledtext as st

from Files import (manage_db, shares_page, watched_page, summary_page,
                   settings_page, calculate)

FONT = "Calabria 12"
BFONT = "Calabria 16"


class Assets(tk.Frame):
    """populate assets frame with buttons calling other frames/pages"""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(
            self, text="LIQUID ASSETS:", font="Calabria 12 bold")
        label.grid(row=0, column=0, sticky="w")

        asset_button = tk.Button(self, text="  Liquid Assets  ",
                                 relief=tk.SUNKEN, font=FONT, bg="yellow")
        asset_button.grid(row=1, column=2, sticky="e", padx=10)

        p1_button = tk.Button(
            self, text="   GPW Share    ", font=FONT, bg="lawn green",
            command=lambda: controller.show_frame(shares_page.Shares))
        p1_button.grid(row=2, column=2, sticky="e", padx=10)

        p2_button = tk.Button(
            self, text="Watched shares", font=FONT, bg="seashell3",
            command=lambda: controller.show_frame(watched_page.Watched))
        p2_button.grid(row=3, column=2, sticky="e", padx=10)

        p3_button = tk.Button(
            self, text="      Summary      ", bg="hot pink", font=FONT,
            command=lambda: controller.show_frame(summary_page.Summary))
        p3_button.grid(row=4, column=2, sticky="e", padx=10)

        p4_button = tk.Button(
            self, text="       Settings       ", bg="DeepSkyBlue2", font=FONT,
            command=lambda: controller.show_frame(settings_page.Settings))
        p4_button.grid(row=5, column=2, sticky="e", padx=10)

        add_button = tk.Button(
            self, text="     Add Asset     ", font=FONT,
            command=lambda: Assets.add_asset(self))
        add_button.grid(row=6, column=2, sticky="e", padx=10)

        Assets.populate_canvas(self)

    def add_asset(parent):
        """create another asset then reload canvas to display it"""
        def save():
            content = {"Currency": currency_spinbox.get(),
                       "Amount": amount_entry.get(),
                       "Note": note.get("1.0", "end-1c"),
                       }
            if manage_db.check_for_real_numbers(content["Amount"]):
                manage_db.add_asset(content)
                top_window.destroy()
                Assets.populate_canvas(parent)

        top_window = tk.Toplevel(parent, height=350, width=390)
        top_window.title("Add")

        little_frame = tk.Frame(top_window, height=50, width=200)
        little_frame.grid(sticky="nw")

        amount_label = tk.Label(little_frame, text="Amount:   ", font=FONT)
        amount_label.grid(sticky="nw", padx=5, pady=5)

        amount_entry = tk.Entry(little_frame, width=10, font=FONT)
        amount_entry.grid(row=0, column=1, padx=5, pady=5)

        currency_label = tk.Label(little_frame, text="Currency:   ", font=FONT)
        currency_label.grid(sticky="nw", padx=5)

        currency_tuple = ("USD", "EUR", "GBP", "PLN", "CHF")

        currency_spinbox = tk.Spinbox(
            little_frame, values=currency_tuple, width=5,
            state="readonly", font=FONT)
        currency_spinbox.grid(row=1, column=1)

        note = st.ScrolledText(top_window, width=30, height=5, font=FONT)
        note.grid(row=6, column=0, columnspan=3)

        add_button = tk.Button(
            top_window, text="Add", font=FONT, command=save)
        add_button.grid(sticky="nw", padx=5, pady=5)

    def populate_canvas(parent):
        """create scrollable canvas with child frame bind to it
        to display all the assets """
        list_of_assets = manage_db.fetch_all_from_table("assets")
        added_values = calculate.add_liquid_assets()

        def menu_window(asset):
            def delete_asset():
                manage_db.delete_row_from_table(
                    "assets", "timestamp", asset[0])
                choice_window.destroy()
                Assets.populate_canvas(parent)

            def edit_asset():
                choice_window.destroy()

                def save():
                    new_asset = {"Currency": currency_spinbox.get(),
                                 "Amount": amount_entry.get(),
                                 "Note": note.get("1.0", "end-1c"),
                                 }
                    if manage_db.check_for_real_numbers(new_asset["Amount"]):
                        manage_db.add_asset(new_asset)
                        manage_db.delete_row_from_table(
                            "assets", "timestamp", asset[0])
                        top_window.destroy()
                        Assets.populate_canvas(parent)

                top_window = tk.Toplevel(parent, height=350, width=390)
                top_window.title("Edit")

                little_frame = tk.Frame(top_window, height=50, width=200)
                little_frame.grid(sticky="nw")

                amount_label = tk.Label(
                    little_frame, text="Amount:   ", font=FONT)
                amount_label.grid(sticky="nw", padx=5, pady=5)

                amount_entry = tk.Entry(little_frame, width=10, font=FONT)
                amount_entry.grid(row=0, column=1, padx=5, pady=5)
                amount_entry.insert(0, asset[1])

                currency_label = tk.Label(
                    little_frame, text="Currency:   ", font=FONT)
                currency_label.grid(sticky="nw", padx=5)

                currency_tuple = ("USD", "EUR", "GBP", "PLN", "CHF")

                currency_spinbox = tk.Spinbox(
                    little_frame, values=currency_tuple, width=5,
                    state="readonly", font=FONT)
                currency_spinbox.grid(row=1, column=1)
                currency_spinbox.insert(0, asset[2])

                note = st.ScrolledText(
                    top_window, width=30, height=5, font=FONT)
                note.grid(row=6, column=0, columnspan=3)
                note.insert(1.0, asset[3])

                save_button = tk.Button(
                    top_window, text="Edit", font=FONT, command=save)
                save_button.grid(sticky="nw", padx=5)

            choice_window = tk.Toplevel(master=None, width=400, height=200)

            edit_button = tk.Button(
                choice_window, text="Edit", font=FONT, bg="green",
                command=lambda: edit_asset())
            edit_button.grid(row=0, column=0, pady=20, padx=20)

            delete_button = tk.Button(
                choice_window, text="Delete", font=FONT, bg="red",
                command=lambda: delete_asset())
            delete_button.grid(row=0, column=1, pady=20)

            cancel_button = tk.Button(
                choice_window, text="Cancel", font=FONT,
                command=choice_window.destroy)
            cancel_button.grid(row=0, column=2, pady=20, padx=20)

        def on_frame_configure(canvas):
            '''Reset the scroll region to encompass the inner frame'''
            canvas.configure(scrollregion=canvas.bbox("all"))

        def check_which_asset_you_clicked_on(event):
            if event.y < 80:
                pass
            else:
                asset_num = int((event.y-80)/80)
                menu_window(list_of_assets[asset_num])

        canvas_scrollregion = 100*len(list_of_assets)

        canvas = tk.Canvas(
            parent, width=800, height=300,
            scrollregion=(0, 0, 0, canvas_scrollregion))
        canvas.grid(row=1, column=0, sticky="w", rowspan=20)

        vbar = tk.Scrollbar(
            parent, orient=tk.VERTICAL, command=canvas.yview)
        vbar.grid(row=1, column=1, rowspan=20, sticky="ns")
        canvas.config(yscrollcommand=vbar.set)

        frame = tk.Frame(
            canvas, width=790, height=len(list_of_assets)*100)
        frame.grid(sticky="nw")
        frame.bind("<Configure>", lambda event, canvas=canvas:
                   on_frame_configure(canvas))
        canvas.create_window((0, 0), window=frame, anchor="nw")

        title_label = tk.Label(frame, text="SUMMARY:", font=BFONT)
        title_label.grid(row=0, column=0, sticky="w")

        eur_label = tk.Label(frame, text="EUR = " + str(added_values['eur']), font=BFONT)
        eur_label.grid(row=0, column=1, sticky="w")
        pln_label = tk.Label(frame, text="PLN = " + str(added_values['pln']), font=BFONT)
        pln_label.grid(row=1, column=1, sticky="w")
        gbp_label = tk.Label(frame, text="GBP = " + str(added_values['gbp']), font=BFONT)
        gbp_label.grid(row=0, column=2, sticky="w")
        usd_label = tk.Label(frame, text="USD = " + str(added_values['usd']), font=BFONT)
        usd_label.grid(row=1, column=2, sticky="w")
        chf_label = tk.Label(frame, text="CHF = " + str(added_values['chf']), font=BFONT)
        chf_label.grid(row=0, column=3, sticky="w")

        separator_label = tk.Label(frame, text="_"*300)
        separator_label.grid(sticky="nw", columnspan=15)

        row = 3
        for asset in list_of_assets:
            cash_currency_string = (str(asset[1]) + "    " + asset[2])
            bils_label = tk.Label(
                frame, text=cash_currency_string, font=BFONT)
            bils_label.grid(row=row+1, column=0, sticky="w")

            description_label = tk.Label(frame, text=asset[3], font=BFONT)
            description_label.grid(sticky="nw", columnspan=15)

            separator_label = tk.Label(frame, text="_"*300)
            separator_label.grid(sticky="nw", columnspan=15)

            row += 3

        frame.bind("<Button-3>", check_which_asset_you_clicked_on)
