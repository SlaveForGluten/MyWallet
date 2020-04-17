import tkinter as tk
from tkinter import messagebox

from Files import (shares_page, manage_db, calculate, scrap_web)

FONT = "Calabria 12"


def add_shares(parent):
    """allows you to add share"""
    def save():
        if(manage_db.check_if_valid_name(name.get()) and
           manage_db.check_for_real_numbers(entry_price.get()) and
           manage_db.check_date_format(date.get())):
            share = {"Name": name.get(),
                     "Quantity": quantity.get(),
                     "BuyingPrice": entry_price.get(),
                     "BuyingDate": date.get(),
                     "Cost": "",
                     "SellingPrice": "",
                     "SellingDate": "",
                     "Dividends": ""}
            manage_db.add_share("gpw_shares", share)
            manage_db.add_current_price(
                name.get(), scrap_web.pull_current_price(name.get()))
            shares_page.Shares.curent_canvas(parent)
            top_window.destroy()

    top_window = tk.Toplevel(parent, height=600, width=390)
    # LABELS:
    list_of_labels = ["Name:", "Quantity:", "Entry price (per share):",
                      "Entry date:", ]
    for txt in list_of_labels:
        label = tk.Label(top_window, text=txt, font=FONT)
        label.grid(sticky="nw")
    # ENTRIES:
    name = tk.Entry(top_window, width=9, font=FONT)
    name.grid(row=0, column=1, padx=10)
    quantity = tk.Entry(top_window, width=9, font=FONT)
    quantity.grid(row=1, column=1, padx=10)
    entry_price = tk.Entry(top_window, width=9, font=FONT)
    entry_price.grid(row=2, column=1, padx=10)
    date = tk.Entry(top_window, width=9, font=FONT)
    date.grid(row=3, column=1, padx=10)

    add_button = tk.Button(
        top_window, text="Add", font=FONT, command=save)
    add_button.grid(sticky="nw", padx=5, pady=5)


def menu_window(parent, share):
    """right clicking on a closed or active share opens a menu windows
    with buttons allowing you to edit/add alarm/delete share
    """
    menu_window = tk.Toplevel(master=None, width=400, height=200)

    edit_button = tk.Button(
        menu_window, text="Edit", font=FONT, bg="green",
        command=lambda: edit(parent, share, menu_window))
    edit_button.grid(row=0, column=0, pady=20, padx=20)

    alarm_button = tk.Button(
        menu_window, text="Alarm", font=FONT, bg="green",
        command=lambda: set_alarm(parent, share, menu_window))
    alarm_button.grid(row=0, column=1, pady=20)

    delete_button = tk.Button(
        menu_window, text="Delete", font=FONT, bg="red",
        command=lambda: delete(parent, share, menu_window))
    delete_button.grid(row=0, column=2, pady=20, padx=20)

    cancel_button = tk.Button(
        menu_window, text="Cancel", font=FONT,
        command=menu_window.destroy)
    cancel_button.grid(row=0, column=3, pady=20, )


def delete(parent, to_delete, choice_window):
    """deletes unwanted share"""
    if messagebox.askyesno(
            "Delete", "Are you sure you want to delete this?"):
        if to_delete[6] == "":
            manage_db.delete_row_from_table(
                "gpw_shares", "timestamp", to_delete[0])
            shares_page.Shares.curent_canvas(parent)
        else:
            manage_db.delete_row_from_table(
                "gpw_shares_closed", "timestamp", to_delete[0])
            shares_page.Shares.historical_canvas(parent)
        choice_window.destroy()


def edit(parent, old_share, choice_window):
    """display edit window for active or sold shares. After viewing or
    editing you can save changes """
    def save():
        share = {"Name": name.get(),
                 "Quantity": quantity.get(),
                 "BuyingPrice": entry_price.get(),
                 "BuyingDate": entry_date.get(),
                 "SellingPrice": exit_price.get(),
                 "SellingDate": exit_date.get(),
                 "Cost": ''
                 }
        # cost depends on changing current share price but if a
        # share was sold, you need to consider fixed selling price.
        # Therefore sold cost can be calculated and added to dictionary
        # without the need of calculating it all over again:
        if exit_price.get() != "":
            total_buying_price = int(
                share["Quantity"])*float(share["BuyingPrice"])
            total_selling_price = int(
                share["Quantity"])*float(share["SellingPrice"])
            share["Cost"] = str(calculate.total_costs(
                total_buying_price, total_selling_price))

        # Collect and save in order all user input from dividend
        # and dividend_date entries.

        # If no previous inputs:
        if old_share[8] == "":
            list_of_entries = (div_2, div_3, div_4, div_5)
            list_of_dates = (div_date_2, div_date_3,
                             div_date_4, div_date_5)
            share["Dividends"] = ""
            if div_1.get():
                share["Dividends"] = (
                    div_1.get()+"-"+div_date_1.get())

            for counter, entrie in enumerate(list_of_entries):
                if entrie.get():
                    share["Dividends"] = (share["Dividends"]+"|" +
                                          entrie.get()+"-" +
                                          list_of_dates[counter].get())

        # If previous entries exist, replace the ones displayed
        # (up to 4 latest) with the new ones (in case edits were made)

        else:
            list_of_entries = (div_1, div_2, div_3, div_4, div_5)
            list_of_dates = (div_date_1, div_date_2, div_date_3,
                             div_date_4, div_date_5)
            number_of_entries_to_clear = 4
            all_dividents = old_share[8].split("|")
            for __ in range(0, number_of_entries_to_clear):
                if all_dividents:
                    # if len(all_dividents) > 0:
                    all_dividents.remove(
                        all_dividents[len(all_dividents)-1])

            for counter, entrie in enumerate(list_of_entries):
                if entrie.get():
                    all_dividents.append(entrie.get() + "-" +
                                         list_of_dates[counter].get())

            share["Dividends"] = '|'.join(all_dividents)

        # check if all input correct
        if(manage_db.check_if_valid_name(name.get()) and
           manage_db.check_for_real_numbers(entry_price.get()) and
           manage_db.check_for_real_numbers(exit_price.get()) or
           exit_price.get() == '' and
           manage_db.check_date_format(entry_date.get()) and
           manage_db.check_date_format(exit_date.get()) or
           exit_date.get() == ''):
            top_window.destroy()

            if old_share[6] == "":
                manage_db.delete_row_from_table(
                    "gpw_shares", "timestamp", old_share[0])
            else:
                manage_db.delete_row_from_table(
                    "gpw_shares_closed", "timestamp", old_share[0])

            if share["SellingDate"] == "":
                manage_db.add_share("gpw_shares", share)
                manage_db.add_current_price(
                    share["Name"], scrap_web.pull_current_price(share["Name"]))
                shares_page.Shares.curent_canvas(parent)
            else:
                manage_db.add_share("gpw_shares_closed", share)
                shares_page.Shares.historical_canvas(parent)

    choice_window.destroy()
    top_window = tk.Toplevel(parent, height=600, width=390)
    # LABELS
    list_of_labels = ["Name:", "Quantity:", "Entry price (per share):",
                      "Entry date:", "Divident:", "Divident date:",
                      "Exit price (per share):", "Exit dete:"]
    for txt in list_of_labels:
        label = tk.Label(top_window, text=txt, font=FONT)
        label.grid(sticky="nw")
    # ENTRIES
    name = tk.Entry(top_window, width=9, font=FONT)
    name.grid(row=0, column=1, padx=5)
    name.insert(0, old_share[1])
    quantity = tk.Entry(top_window, width=9, font=FONT)
    quantity.grid(row=1, column=1, padx=5)
    quantity.insert(0, old_share[2])
    entry_price = tk.Entry(top_window, width=9, font=FONT)
    entry_price.grid(row=2, column=1, padx=5)
    entry_price.insert(0, old_share[3])
    entry_date = tk.Entry(top_window, width=9, font=FONT)
    entry_date.grid(row=3, column=1, padx=5)
    entry_date.insert(0, old_share[4])
    div_1 = tk.Entry(top_window, width=9, font=FONT)
    div_1.grid(row=4, column=1, padx=5)
    div_date_1 = tk.Entry(top_window, width=9, font=FONT)
    div_date_1.grid(row=5, column=1, padx=5)
    div_2 = tk.Entry(top_window, width=9, font=FONT)
    div_2.grid(row=4, column=2, padx=5)
    div_date_2 = tk.Entry(top_window, width=9, font=FONT)
    div_date_2.grid(row=5, column=2, padx=5)
    div_3 = tk.Entry(top_window, width=9, font=FONT)
    div_3.grid(row=4, column=3, padx=5)
    div_date_3 = tk.Entry(top_window, width=9, font=FONT)
    div_date_3.grid(row=5, column=3, padx=5)
    div_4 = tk.Entry(top_window, width=9, font=FONT)
    div_4.grid(row=4, column=4, padx=5)
    div_date_4 = tk.Entry(top_window, width=9, font=FONT)
    div_date_4.grid(row=5, column=4, padx=5)
    # if share does have a dividend inputed, insert up to four last
    # dividend entries and leave last (5th) field empty for a new
    # entry, this allows you to view and edit previous entries

    if old_share[8]:
        list_of_entries = (div_4, div_3, div_2, div_1)
        list_of_notes = (
            div_date_4, div_date_3, div_date_2, div_date_1)
        last_dividends = old_share[8].split("|")
        last_dividends.reverse()
        if len(last_dividends) >= 4:
            dividends_to_display = 4
            for counter in range(0, dividends_to_display):
                for div_or_date, value in enumerate(
                        last_dividends[counter].split("-")):
                    # first run of last for loop gives you dividend and
                    # last gives this dividend's date
                    if div_or_date == 0:
                        list_of_entries[counter].insert(0, value)
                    else:
                        list_of_notes[counter].insert(0, value)
        else:
            list_of_entries = (div_1, div_2, div_3)
            list_of_notes = (div_date_1, div_date_2, div_date_3)
            last_dividends = old_share[8].split("|")
            number_of_dividends = len(last_dividends)
            for counter in range(0, number_of_dividends):
                for div_or_date, value in enumerate(
                        last_dividends[counter].split("-")):
                    # first run of last for loop gives you dividend and
                    # last gives this dividend's date
                    if div_or_date == 0:
                        list_of_entries[counter].insert(0, value)
                    else:
                        list_of_notes[counter].insert(0, value)
    div_5 = tk.Entry(top_window, width=9, font=FONT)
    div_5.grid(row=4, column=5, padx=5)
    div_date_5 = tk.Entry(top_window, width=9, font=FONT)
    div_date_5.grid(row=5, column=5, padx=5)
    exit_price = tk.Entry(top_window, width=9, font=FONT)
    exit_price.grid(row=6, column=1, padx=5)
    exit_price.insert(0, old_share[6])
    exit_date = tk.Entry(top_window, width=9, font=FONT)
    exit_date.grid(row=7, column=1, padx=5)
    exit_date.insert(0, old_share[7])

    frame = tk.Frame(top_window, width=200, height=30)
    frame.grid(sticky="nw", columnspan=5)

    add_button = tk.Button(frame, text="Edit", font=FONT, command=save)
    add_button.grid(row=0, column=0, padx=10, pady=5)

    close_button = tk.Button(
        frame, text="Close", font=FONT, command=top_window.destroy)
    close_button.grid(row=0, column=1, pady=5)

    help_button = tk.Button(frame, text="?", font=FONT)
    help_button.grid(row=0, column=2, padx=10, pady=5)


def set_alarm(parent, share, choice_window):
    """adds alarm to a share"""
    prof = share[1]
    alarm = manage_db.fetch_alarm(prof)
    choice_window.destroy()

    def save():
        high = high_price_entry.get()
        low = low_price_entry.get()
        if(manage_db.check_for_real_numbers(high) and
           manage_db.check_for_real_numbers(low)):
            manage_db.add_alarm(prof, high, low)
            top_window.destroy()
            if share[6] == "":
                shares_page.Shares.curent_canvas(parent)
            else:
                shares_page.Shares.historical_canvas(parent)
    top_window = tk.Toplevel(parent, height=350, width=390)
    top_window.title("Edit")

    amount_label = tk.Label(
        top_window, text=prof, font=FONT)
    amount_label.grid(sticky="nw", padx=5, pady=5)

    amount_label = tk.Label(
        top_window, text="Let me know when:", font=FONT)
    amount_label.grid(sticky="nw", padx=5, pady=5)

    label = tk.Label(
        top_window, text="Price is higher or equal to:", font=FONT)
    label.grid(sticky="nw", padx=5, pady=5)

    label = tk.Label(
        top_window, text="Price is lower or equal to:", font=FONT)
    label.grid(sticky="nw", padx=5, pady=5)

    high_price_entry = tk.Entry(top_window, width=10, font=FONT)
    high_price_entry.grid(row=2, column=1, padx=5, pady=5)

    low_price_entry = tk.Entry(top_window, width=10, font=FONT)
    low_price_entry.grid(row=3, column=1, padx=5, pady=5)

    high_price_entry.insert(0, alarm[1])
    low_price_entry.insert(0, alarm[2])
    add_button = tk.Button(
        top_window, text="Add", font=FONT, command=save)
    add_button.grid(sticky="nw", padx=5)
