"""displays quarterly reports of a given share pulled from bankier.pl website,
allows you to add alarms to a share"""

import tkinter as tk

from Files import (manage_db, scrap_web, assets_page, shares_page,
                   summary_page, settings_page)


FONT = "Calabria 12"
SFON = "Calabria 10"


class Watched(tk.Frame):
    """create a watched frame, create buttons invoking other frames/pages"""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def update_wathched_shares():
            manage_db.update_watched_shares()
            Watched.populate_canvas(self)

        label = tk.Label(self, text="WATCHED SHARES:", font="Calabria 12 bold")
        label.grid(row=0, column=0, sticky="w")

        sp_button = tk.Button(
            self, text="  Liquid Assets  ", font=FONT, bg="yellow",
            command=lambda: controller.show_frame(assets_page.Assets))
        sp_button.grid(row=1, column=2, sticky="e", padx=10)

        p1_button = tk.Button(
            self, text="  GPW Shares   ", font=FONT, bg="lawn green",
            command=lambda: controller.show_frame(shares_page.Shares))
        p1_button.grid(row=2, column=2, sticky="e", padx=10)

        shares_button = tk.Button(self, text="Watched shares",
                                  relief=tk.SUNKEN, font=FONT, bg="seashell3")
        shares_button.grid(row=3, column=2, sticky="e", padx=10)

        p3_button = tk.Button(
            self, text="      Summary      ", bg="hot pink", font=FONT,
            command=lambda: controller.show_frame(summary_page.Summary))
        p3_button.grid(row=4, column=2, sticky="e", padx=10)

        p4_button = tk.Button(
            self, text="       Settings       ", bg="DeepSkyBlue2", font=FONT,
            command=lambda: controller.show_frame(settings_page.Settings))
        p4_button.grid(row=5, column=2, sticky="e", padx=10)

        add_button = tk.Button(
            self, text="   Watch profile   ", font=FONT,
            command=lambda: Watched.add_to_watched(self))
        add_button.grid(row=6, column=2, sticky="e", padx=10)

        update_button = tk.Button(self, text="        Update        ",
                                  font=FONT, command=update_wathched_shares)
        update_button.grid(row=7, column=2, sticky="e", padx=10)

        # manage_db.update_price("WatchedShares")
        Watched.populate_canvas(self)

    def add_to_watched(parent):
        """pull quarterly reports of a new share and display them"""
        def save():
            profile = entry.get()
            if(manage_db.check_if_valid_name(profile) is True and
               manage_db.fetch_reports(profile) == []):
                top_window.destroy()
                manage_db.add_quarterly_reports(
                    scrap_web.historical_data(profile))
                manage_db.add_current_price(
                    profile, scrap_web.pull_current_price(profile))
                Watched.populate_canvas(parent)

        top_window = tk.Toplevel(parent, height=600, width=390)

        label = tk.Label(top_window, text="Profile name: ", font=FONT)
        label.grid(sticky="nw", pady=10, padx=10)

        entry = tk.Entry(top_window, width=15, font=FONT)
        entry.grid(row=0, column=1, pady=10, padx=10)

        add_button = tk.Button(
            top_window, text="Watch profile", font=FONT, command=save)
        add_button.grid(sticky="nw", pady=10, padx=10)

    def populate_canvas(parent):
        """create a scrollable canvas with frame binded to it"""
        list_of_reports = list()
        for profile in manage_db.fetch_all_from_table("current_price"):
            prof = manage_db.fetch_reports(profile[0])
            if prof:
                list_of_reports.append(prof)

        def choose_action(event):
            """"""
            def delete_asset(to_delete):
                manage_db.delete_row_from_table(
                    "reports", "profile", to_delete[0][0])
                choice_window.destroy()
                Watched.populate_canvas(parent)

            def set_alarm(share):
                prof = share[0][0]
                alarm = manage_db.fetch_alarm(prof)
                choice_window.destroy()

                def save():
                    high = high_price_entry.get()
                    low = low_price_entry.get()
                    if(manage_db.check_for_real_numbers(high) and
                       manage_db.check_for_real_numbers(low)):
                        manage_db.add_alarm(prof, high, low)
                        Watched.populate_canvas(parent)
                        top_window.destroy()
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
            asset_num = int(event.y/196)
            choice_window = tk.Toplevel(master=None, width=400, height=200)

            alarm_button = tk.Button(
                choice_window, text="Add alarm", font=FONT, bg="green",
                command=lambda: set_alarm(list_of_reports[asset_num]))
            alarm_button.grid(row=0, column=0, pady=20, padx=20)

            delete_button = tk.Button(
                choice_window, text="Delete", font=FONT, bg="red",
                command=lambda: delete_asset(list_of_reports[asset_num]))
            delete_button.grid(row=0, column=1, pady=20)

            cancel_button = tk.Button(
                choice_window, text="Cancel", font=FONT,
                command=choice_window.destroy)
            cancel_button.grid(row=0, column=2, pady=20, padx=20)

        def on_frame_configure(canvas):
            '''Reset the scroll region to encompass the inner frame'''
            canvas.configure(scrollregion=canvas.bbox("all"))
        canvas_scrollregion = 100*len(list_of_reports)

        canvas = tk.Canvas(
            parent, width=800, height=300,
            scrollregion=(0, 0, 0, canvas_scrollregion))
        canvas.grid(row=1, column=0, sticky="w", rowspan=20)

        vbar = tk.Scrollbar(
            parent, orient=tk.VERTICAL, command=canvas.yview)
        vbar.grid(row=1, column=1, rowspan=20, sticky="ns")
        canvas.config(yscrollcommand=vbar.set)

        frame = tk.Frame(
            canvas, width=705, height=len(list_of_reports)*100)
        frame.grid(sticky="nw")
        frame.bind("<Configure>", lambda event, canvas=canvas:
                   on_frame_configure(canvas))
        canvas.create_window((0, 0), window=frame, anchor="nw")

        row = 0
        for report in list_of_reports:
            current_price = manage_db.fetch_current_price(report[0][0])
            # first column
            rows = 0
            list_of_labels = [report[0][0], "  ", "Av. Price:", "BV/Share:",
                              "Price/BV:", "Net Profit(k):", "Shares(k):", "NMP:"]
            for txt in list_of_labels:
                label = tk.Label(frame, text=txt, font=SFON)
                label.grid(row=0+rows+row, column=0, sticky="w")
                rows += 1
            # first row
            price_label = tk.Label(frame, text=current_price.split(" ")[0], font=SFON)
            price_val_label = tk.Label(frame, text=current_price.split(" ")[1], font=SFON)
            price_prc_label = tk.Label(frame, text=current_price.split(" ")[2], font=SFON)
            if float(current_price.split(" ")[2]) > 0:
                price_val_label.configure(fg="green")
                price_prc_label.configure(fg="green")
            elif float(current_price.split(" ")[2]) < 0:
                price_val_label.configure(fg="red")
                price_prc_label.configure(fg="red")
            list_of_labels = [price_label, price_val_label, price_prc_label]
            col = 1
            for label in list_of_labels:
                label.grid(row=0+row, column=col, sticky='w')
                col += 1
            label = tk.Label(frame, text="P/BV:", font=SFON)
            label.grid(row=0+row, column=4, sticky="w")
            current_price_per_bv = (float(current_price.split(" ")[0]) /
                                    ((float(report[4][9])*1000) /
                                    int(report[5][9])))
            label = tk.Label(frame, text=round(current_price_per_bv, 2), font=SFON)
            label.grid(row=0+row, column=5, sticky="w")

            for i in range(2, 10):
                # second row
                label = tk.Label(frame, text=report[0][i], font=SFON)
                label.grid(row=1+row, column=i-1, sticky="w")
                # third row (quartal average share price)
                label = tk.Label(frame, text=round(float(report[1][i]), 2), font=SFON)
                label.grid(row=2+row, column=i-1, sticky="w")
                # 4th row (BV/Share - book_value/share_numbers)
                bv_per_share = (float(report[4][i])*1000) / int(report[5][i])
                label = tk.Label(frame, text=round(bv_per_share, 2), font=SFON)
                label.grid(row=3+row, column=i-1, sticky="w")
                # 5th row (P/BV - price/(book_value/shares_number))
                price_per_bv = (float(report[1][i]) /
                                ((float(report[4][i])*1000) /
                                 int(report[5][i])))
                label = tk.Label(frame, text=round(price_per_bv, 2), font=SFON)
                label.grid(row=4+row, column=i-1, sticky="w")
                # 6th row (net profit[k])
                label = tk.Label(frame, text=report[3][i], font=SFON)
                label.grid(row=5+row, column=i-1, sticky="w")
                # 7th row (number of shares[k]):
                label = tk.Label(
                    frame, text=str(round(int(report[5][i])/1000)), font=SFON)
                label.grid(row=6+row, column=i-1, sticky="w")
                # 8th row (NMP - net profit margin (net_profit/net_income)*100%)
                nmp = (int(report[3][i])/int(report[2][i]))*100
                label = tk.Label(frame, text=str(round(nmp, 2))+"%", font=SFON)
                label.grid(row=7+row, column=i-1, sticky="w")

            # separator
            note_label = tk.Label(frame, text="_"*200)
            note_label.grid(sticky="nw", columnspan=15)

            row += 9
        frame.bind("<Button-3>", choose_action)
