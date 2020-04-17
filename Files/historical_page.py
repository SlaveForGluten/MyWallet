import tkinter as tk

from Files import (add_edit_delete_share, manage_db, calculate, assets_page,
                   watched_page, summary_page, settings_page, shares_page)


FONT = "Calabria 12"
SFON = "Calabria 10"


class History(tk.Frame):
    """Creates shares frame and populates it with buttons invoking
    other pages/frames. 'Shares' frame contains scrollable canvas binded
    to a frame on which shares are displayed."""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="PAST TRANSACTIONS:", font="Calabria 12 bold")
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

        active_s_button = tk.Button(
            self, text="  Active Shares  ", font=FONT,
            command=lambda: controller.show_frame(shares_page.Shares))
        active_s_button.grid(row=7, column=2, sticky="e", padx=10)

        History.historical_canvas(self)

    def historical_canvas(parent):
        """displays all the closed shares with final calculations on
        profit, costs. Edits or deleting possible."""
        list_of_shares = manage_db.fetch_all_from_table("gpw_shares_closed")

        def on_frame_configure(canvas):
            '''Reset the scroll region to encompass the inner frame'''
            canvas.configure(scrollregion=canvas.bbox("all"))

        def check_which_share_you_clicked_on(event):
            print(event.y)
            if event.y < 190:
                pass
            else:
                share_num = int((event.y - 190)/240)
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

        # SUMMARY ON PAST TRANSACTIONS, FIRST COLUMN
        label_tuple = ['WALLET SUMMARY:', 'TOTAL PROFIT:', 'TOTAL COSTS:',
                       'AVERAGE ANN. ROR:', 'BIGGEST PROFIT:',
                       '(single transaction)', 'BIGGEST LOSE:',
                       '(single transaction)']
        row = 0
        for label in label_tuple:
            title_label = tk.Label(frame, text=label, font=SFON)
            title_label.grid(row=row, column=0, sticky="w")
            row += 1

        separator_label = tk.Label(frame, text="_"*200)
        separator_label.grid(sticky="nw", columnspan=15)

        # SUMMARY ON PAST TRANSACTIONS, SECOND COLUMN
        values_dict = calculate.values_for_historical_transactions()

        title_label = tk.Label(frame, text='VALUES:', font=SFON)
        title_label.grid(row=0, column=1, sticky='w')
        profit_label = tk.Label(frame, text=values_dict['total_profit'], font=SFON)
        profit_label.grid(row=1, column=1, sticky='w')
        costs_label = tk.Label(frame, text=values_dict['total_costs'], font=SFON)
        costs_label.grid(row=2, column=1, sticky='w')
        ror_label = tk.Label(frame, text=str(values_dict['average_annual_ror']) + "%", font=SFON)
        ror_label.grid(row=3, column=1, sticky='w')
        big_label = tk.Label(frame, text=str(values_dict['biggest_profit']) + " " + values_dict['biggest_profit_profile'], font=SFON)
        big_label.grid(row=4, column=1, sticky='w')
        big_label = tk.Label(frame, text=" ", font=SFON)
        big_label.grid(row=5, column=1, sticky='w')
        low_label = tk.Label(frame, text=str(values_dict['biggest_lose']) + " " + values_dict['biggest_lose_profile'], font=SFON)
        low_label.grid(row=6, column=1, sticky='w')

        row = 9
        for share in list_of_shares:
            if share[6] != "":
                # TITLE LABELS:
                list_of_labels = [
                    "NAME:", "QUANTITY:", "ENTRY DATE:", "EXIT DATE:",
                    "ENTRY PRICE:", "EXIT PRICE:", "COSTS:", "DIVIDENTS:",
                    "ANNUAL ROR:", "PROFIT:"]
                for txt in list_of_labels:
                    label = tk.Label(frame, text=txt, font=SFON)
                    label.grid(sticky="nw")
                # VALUES
                total_buying_price = share[2]*share[3]
                total_selling_price = share[2]*share[6]
                total_div = calculate.total_dividend(share[8])
                annual_ror = calculate.annual_ror(
                    share, share[6], share[5], total_div)
                profit = (total_selling_price - total_buying_price +
                          total_div - share[5])

                label = tk.Label(frame, text=share[1], font=SFON)
                label.grid(row=row+0, column=1, sticky="w")
                label = tk.Label(frame, text=share[2], font=SFON)
                label.grid(row=row+1, column=1, sticky="w")
                label = tk.Label(frame, text=share[4], font=SFON)
                label.grid(row=row+2, column=1, sticky="w")
                label = tk.Label(frame, text=share[7], font=SFON)
                label.grid(row=row+3, column=1, sticky="w")
                label = tk.Label(frame, text=share[3], font=SFON)
                label.grid(row=row+4, column=1, sticky="w")
                label = tk.Label(frame, text=share[6], font=SFON)
                label.grid(row=row+5, column=1, sticky="w")
                label = tk.Label(
                    frame, text=round(share[5], 2), font=SFON)
                label.grid(row=row+6, column=1, sticky="w")
                label = tk.Label(frame, text=total_div, font=SFON)
                label.grid(row=row+7, column=1, sticky="w")
                label = tk.Label(frame, text=str(annual_ror)+"%", font=SFON)
                label.grid(row=row+8, column=1, sticky="w")
                label = tk.Label(frame, text=round(profit, 2), font=SFON)
                if profit > 0:
                    label.configure(fg="green")
                if profit < 0:
                    label.configure(fg="red")
                label.grid(row=row+9, column=1, sticky="w")
                row += 11

                # separator
                note_label = tk.Label(frame, text="_"*200)
                note_label.grid(sticky="nw", columnspan=15)

        frame.bind("<Button-3>", check_which_share_you_clicked_on)