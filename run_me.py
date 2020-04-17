"""
Main file of InvestmentTracker program.
Creates all the program pages that can be invoked later.
Pulls content from Internet after given time using Tkinter after() method
to repeat the call.
"""

import tkinter as tk

from Files import (manage_db, scrap_web, send_message, assets_page,
                   shares_page, watched_page, summary_page, settings_page,
                   historical_page)


FONT = "Calabria 12"


class InvestmentTracker(tk.Tk):
    """create main frame, call to create db if first run, update db"""
    def __init__(self):
        tk.Tk.__init__(self)

        def repeat_the_call():
            settings = manage_db.fetch_all_from_table("settings")[0]
            pause = settings[10]
            timer = 3600000  # 1 hour in milliseconds
            if pause == "15min":
                timer = 900000
            elif pause == "30min":
                timer = 1800000
            elif pause == "1h":
                timer = 3600000
            elif pause == "2h":
                timer = 7200000
            manage_db.update_current_price()
            check_alarm_conditions(settings)
            self.after(timer, repeat_the_call)

        tk.Tk.iconbitmap(self, default="m-m-m-money.ico")
        tk.Tk.wm_title(self, "InvestmentsTracker")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # create tables if db deleted
        manage_db.create_tables()
        # delete unused current_prices (updating them takes time)
        manage_db.remove_unused_prices_and_alarms()
        # update current share prices
        manage_db.update_current_price()
        # update currency rates
        manage_db.add_currency_rates(scrap_web.pull_currency_rates())

        self.frames = dict()
        for page in (assets_page.Assets,
                     shares_page.Shares,
                     watched_page.Watched,
                     summary_page.Summary,
                     settings_page.Settings,
                     historical_page.History):
            frame = page(container, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(assets_page.Assets)
        repeat_the_call()

    def show_frame(self, cont):
        """raise given frame"""
        frame = self.frames[cont]
        frame.tkraise()


def check_alarm_conditions(settings):
    """check if time and conditions to raise the alarm fit,
    if so, send message"""
    if manage_db.check_time(settings[8], settings[9]) == "alarm on":
        alarms = manage_db.fetch_all_from_table("alarms")

        for alarm in alarms:
            current_price = manage_db.fetch_current_price(alarm[0]).split()[0]
            if float(current_price) >= alarm[1]:
                if settings[0] == "1":
                    send_message.send_sms(alarm[0], current_price, settings)
                if settings[1] == "1":
                    send_message.send_email(alarm[0], current_price, settings)
                if settings[2] == "1":
                    send_message.on_screen(alarm[0], current_price)
            if float(current_price) <= alarm[2]:
                if settings[0] == "1":
                    send_message.send_sms(alarm[0], current_price, settings)
                if settings[1] == "1":
                    send_message.send_email(alarm[0], current_price, settings)
                if settings[2] == "1":
                    send_message.on_screen(alarm[0], current_price)


def run():
    """create main instance"""
    app = InvestmentTracker()
    app.mainloop()

run()
