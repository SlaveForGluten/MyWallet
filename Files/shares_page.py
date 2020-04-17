"""
this module displays information about added shares, allows you to edit
and delete them. Lets you add alarm to a share which will check current share
price and let you know if the price matches the one set in the alarm.
Contains a subpage 'closed shares' in which historical transactions
are displayed.
"""

import tkinter as tk

from Files import (add_edit_delete_share, manage_db, calculate, assets_page,
                   watched_page, summary_page, settings_page, historical_page)


FONT = "Calabria 12"
SFON = "Calabria 10"


class Shares(tk.Frame):
    """Creates shares frame and populates it with buttons invoking
    other pages/frames. 'Shares' frame contains scrollable canvas binded
    to a frame on which shares are displayed."""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="GPW SHARES:", font="Calabria 12 bold")
        label.grid(row=0, column=0, sticky="w")

        assets_button = tk.Button(
            self, text="  Liquid Assets  ", font=FONT, bg="yellow",
            command=lambda: controller.show_frame(assets_page.Assets))
        assets_button.grid(row=1, column=2, sticky="e", padx=10)

        shares_button = tk.Button(self, text="  GPW Shares   ",
                                  relief=tk.SUNKEN, font=FONT, bg="lawn green")
        shares_button.grid(row=2, column=2, sticky="e", padx=10)

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

        closed_s_button = tk.Button(
            self, text=" Closed Shares ", font=FONT,
            command=lambda: controller.show_frame(historical_page.History))
        closed_s_button.grid(row=6, column=2, sticky="e", padx=10)

        add_button = tk.Button(
            self, text="    Add Shares    ", font=FONT,
            command=lambda: add_edit_delete_share.add_shares(self))
        add_button.grid(row=7, column=2, sticky="e", padx=10)

        # active_s_button = tk.Button(
        #     self, text="  Active Shares  ", font=FONT,
        #     command=lambda: Shares.curent_canvas(self))
        # active_s_button.grid(row=7, column=2, sticky="e", padx=10)



        Shares.curent_canvas(self)

    def curent_canvas(parent):
        """displays active (not sold) shares"""
        list_of_shares = manage_db.fetch_all_from_table("gpw_shares")
        top_seven_shares = calculate.seven_biggest_shares(calculate.shares_worth(list_of_shares))
        total_worth = calculate.totaled_shares_worth()

        def on_frame_configure(canvas):
            '''Reset the scroll region to encompass the inner frame'''
            canvas.configure(scrollregion=canvas.bbox("all"))

        def check_which_share_you_clicked_on(event):
            if event.y < 217:
                pass
            else:
                share_num = int((event.y-217)/217)
                add_edit_delete_share.menu_window(parent, list_of_shares[share_num])

        canvas_scrollregion = 110*len(list_of_shares)
        canvas = tk.Canvas(
            parent, width=800, height=300,
            scrollregion=(0, 0, 0, canvas_scrollregion))
        canvas.grid(row=1, column=0, sticky="w", rowspan=20)

        vbar = tk.Scrollbar(
            parent, orient=tk.VERTICAL, command=canvas.yview)
        vbar.grid(row=1, column=1, rowspan=20, sticky="ns")
        canvas.config(yscrollcommand=vbar.set)

        frame = tk.Frame(
            canvas, width=805, height=len(list_of_shares)*110)
        frame.grid(sticky="nw")
        frame.bind("<Configure>", lambda event, canvas=canvas:
                   on_frame_configure(canvas))
        canvas.create_window((0, 0), window=frame, anchor="nw")

        # SHARES PAGE, TOP OF SCROLABLE CANVAS, FIRST COLUMN (LABELS)
        title_label = tk.Label(frame, text="WALLET SUMMARY:", font=SFON)
        title_label.grid(sticky="nw")
        label = tk.Label(frame, text="TOP 7 SHARES:", font=SFON)
        label.grid(sticky="nw")
        counter = 1
        for share in top_seven_shares:
            label = tk.Label(frame, text=share[0]+':', font=SFON)
            label.grid(sticky="nw")
            counter += 1
        while counter <= 7:
            label = tk.Label(frame, text=' '*5, font=SFON)
            label.grid(sticky="nw")
            counter += 1

        # SHARES PAGE, TOP OF SCROLABLE CANVAS, SECOND COLUMN (WORTH)
        total_worth_label = tk.Label(
            frame, font=SFON, text="total worth: " + str(total_worth))
        total_worth_label.grid(row=0, column=1, sticky="w")
        counter = 1
        for share in top_seven_shares:
            label = tk.Label(frame, text="worth: " + str(share[1]), font=SFON)
            label.grid(row=counter+1, column=1, sticky="w")
            counter += 1
        while counter <= 7:
            label = tk.Label(frame, text=" "*5, font=SFON)
            label.grid(row=counter+1, column=1, sticky="w")
            counter += 1

        # SHARES PAGE, TOP OF SCROLABLE CANVAS, THIRD COLUMN (PROFIT)
        total_profit_label = tk.Label(frame, font=SFON)
        total_profit_label.grid(row=0, column=2, sticky="w")
        profit_totaled = 0
        for share in list_of_shares:
            profit_totaled += calculate.profit_per_share(share)
        profit_totaled = round(profit_totaled, 2)
        if profit_totaled > 0:
            total_profit_label.configure(fg="green", text="total profit: " +
                                         str(profit_totaled))
        if profit_totaled < 0:
            total_profit_label.configure(fg="red", text="total profit: " +
                                         str(profit_totaled))
        counter = 1
        profit_per_packet = calculate.profit_per_packet(list_of_shares)
        for top in top_seven_shares:
            profit = round(profit_per_packet[top[0]], 2)
            label = tk.Label(frame, text="profit: " + str(profit), font=SFON)
            label.grid(row=counter+1, column=2, sticky="w")
            counter += 1
        while counter <= 7:
            label = tk.Label(frame, text=" "*5, font=SFON)
            label.grid(row=counter+1, column=2, sticky="w")
            counter += 1

        # SHARES PAGE, TOP OF SCROLABLE CANVAS, 4 COLUMN (% OF WHOLE WALLET)
        counter = 1
        for share in top_seven_shares:
            percentage = calculate.calculate_percentage(total_worth, share[1])
            label = tk.Label(frame, text="% of wallet: " + str(percentage) +
                             "%", font=SFON)
            label.grid(row=counter+1, column=3, sticky="w")
            counter += 1
        while counter <= 7:
            label = tk.Label(frame, text=" "*5, font=SFON)
            label.grid(row=counter+1, column=3, sticky="w")
            counter += 1

        # separator
        note_label = tk.Label(frame, text="_"*200)
        note_label.grid(sticky="nw", columnspan=15)

        row = 10
        for share in list_of_shares:
            curent_price = manage_db.fetch_current_price(share[1])

            # TITLE LABELS:
            list_of_labels = [
                "NAME:", "QUANTITY:", "PRICE PER S.:", "ENTRY DATE:",
                "CURRENT PRICE:", "COSTS:", "DIVIDENDS:", "ANNUAL RoR:",
                "PROFIT:"]
            for txt in list_of_labels:
                label = tk.Label(frame, text=txt, font=SFON)
                label.grid(sticky="nw")
            # VALUES
            curent_val_per_s = float(curent_price.split(" ")[0])
            total_buying_price = share[2]*share[3]
            total_selling_price = share[2]*curent_val_per_s
            total_div = calculate.total_dividend(share[8])
            total_costs = calculate.total_costs(
                total_buying_price, total_selling_price)
            annual_ror = calculate.annual_ror(
                share, curent_val_per_s, total_costs, total_div)
            profit = (total_selling_price - total_buying_price +
                      total_div - total_costs)

            label = tk.Label(frame, text=share[1], font=SFON)
            label.grid(row=row+0, column=1, sticky="w")
            label = tk.Label(frame, text=share[2], font=SFON)
            label.grid(row=row+1, column=1, sticky="w")
            label = tk.Label(frame, text=share[3], font=SFON)
            label.grid(row=row+2, column=1, sticky="w")
            label = tk.Label(frame, text=share[4], font=SFON)
            label.grid(row=row+3, column=1, sticky="w")
            label = tk.Label(
                frame, text=curent_price.split(" ")[0], font=SFON)
            label.grid(row=row+4, column=1, sticky="w")
            label = tk.Label(
                frame, text=curent_price.split(" ")[1], font="Calabria 8")
            label.grid(row=row+4, column=2, sticky="w")
            percent_change = float(curent_price.split(" ")[1].strip("%"))
            if percent_change > 0:
                label.configure(fg="green")
            if percent_change < 0:
                label.configure(fg="red")
            val_change = curent_price.split(" ")[2]
            label = tk.Label(
                frame, text=val_change, font="Calabria 8")
            label.grid(row=row+4, column=3, sticky="w")
            if float(val_change) > 0:
                label.configure(fg="green")
            if float(val_change) < 0:
                label.configure(fg="red")
            time = (curent_price.split(" ")[3] +
                    " "+curent_price.split(" ")[4])
            label = tk.Label(
                frame, text=time, font="Calabria 8")
            label.grid(row=row+4, column=4, sticky="w")
            label = tk.Label(frame, text=round(total_costs, 2), font=SFON)
            label.grid(row=row+5, column=1, sticky="w")
            label = tk.Label(frame, text=total_div, font=SFON)
            label.grid(row=row+6, column=1, sticky="w")
            label = tk.Label(frame, text=str(annual_ror)+"%", font=SFON)
            label.grid(row=row+7, column=1, sticky="w")
            label = tk.Label(frame, text=round(profit, 2), font=SFON)
            if profit > 0:
                label.configure(fg="green")
            if profit < 0:
                label.configure(fg="red")
            label.grid(row=row+8, column=1, sticky="w")
            row += 10

            # separator
            note_label = tk.Label(frame, text="_"*200)
            note_label.grid(sticky="nw", columnspan=15)

        frame.bind("<Button-3>", check_which_share_you_clicked_on)
