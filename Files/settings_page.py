"""
this module manages user settings, on first run (or after deleting database)
settings are set to default, current settings are displayed and after any
changes page is refreshed
"""
import tkinter as tk

from Files import (manage_db, assets_page, shares_page, watched_page,
                   summary_page)


FONT = "Calabria 12"
SFON = "Calabria 10"


class Settings(tk.Frame):
    """init creates new frame and populates it wit buttons to invoke other
    frames"""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="SETTINGS:", font="Calabria 12 bold")
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

        p3_button = tk.Button(
            self, text="      Summary      ", bg="hot pink", font=FONT,
            command=lambda: controller.show_frame(summary_page.Summary))
        p3_button.grid(row=5, column=2, sticky="e")

        summary_button = tk.Button(
            self, text="       Settings       ",
            relief=tk.SUNKEN, font=FONT, bg="DeepSkyBlue2")
        summary_button.grid(row=6, column=2, sticky="e")

        Settings.populate_frame(self)

    def populate_frame(parent):
        """display current settings"""
        if manage_db.fetch_all_from_table('settings'):
            # if len(manage_db.fetch_all_from_table('settings')) == 0:
            settings_dict = {
                "sms": '0', "mail": '0', "screen": '0', "id": "", "api": "",
                "p_number": "", "email": "", "from": "09:00", "to": "17:00",
                "break": "30min", "email_pass": ""}
            manage_db.add_settings(settings_dict)
            current_settings = manage_db.fetch_all_from_table('settings')[0]
        else:
            current_settings = manage_db.fetch_all_from_table('settings')[0]

        def save():
            """save settings"""
            settings_dict = {"sms": str(sms_var.get()),
                             "mail": str(email_var.get()),
                             "screen": str(screen_var.get()),
                             "id": id_entry.get(),
                             "api": api_entry.get(),
                             "p_number": number_entry.get(),
                             "email": email_entry.get(),
                             "from": from_time.get(),
                             "to": to_time.get(),
                             "break": break_time.get()
                             }
            if email_pass.get().rstrip("*"):
                settings_dict["email_pass"] = email_pass.get()
            else:
                settings_dict["email_pass"] = current_settings[7]
            manage_db.delete_row_from_table(
                'settings', 'sms', current_settings[0])
            manage_db.add_settings(settings_dict)
            Settings.populate_frame(parent)
        frame = tk.Frame(parent, width=800, height=300)
        frame.grid(row=1, column=0, sticky="w", rowspan=20)

        save_changes = tk.Button(
            frame, text="Save", font=FONT, command=save)
        save_changes.grid(row=8, column=2, sticky="e", padx=10)

        label = tk.Label(frame, text="customer id:", font=FONT)
        label.grid(row=1, column=0, sticky="w")
        label = tk.Label(frame, text="api key:", font=FONT)
        label.grid(row=2, column=0, sticky="w")

        label = tk.Label(frame, text=" "*30, font=FONT)
        label.grid(row=2, column=2, sticky="w")

        label = tk.Label(frame, text="phone number:         +", font=FONT)
        label.grid(row=3, column=0, sticky="w")
        label = tk.Label(frame, text="email:", font=FONT)
        label.grid(row=4, column=0, sticky="w")
        label = tk.Label(frame, text="password:", font=FONT)
        label.grid(row=4, column=1)
        label = tk.Label(frame, text="message time:", font=FONT)
        label.grid(row=5, column=0, sticky="w")
        label = tk.Label(frame, text="from:", font=FONT)
        label.grid(row=6, column=0, sticky="e")
        label = tk.Label(frame, text="to:", font=FONT)
        label.grid(row=7, column=0, sticky="e")
        label = tk.Label(frame, text="send every:", font=FONT)
        label.grid(row=8, column=0, sticky="ne")

        sms_var = tk.IntVar()

        def disable_widgets():
            """unables to make changes in the inputed 'api_entry' and 'id_entry'
            widgets to avoid erasing input, widgets will respond after
            unlocking them with 'sms_button' checkbutton"""
            if sms_var.get() == 0:
                id_entry.configure(state=tk.DISABLED)
                api_entry.configure(state=tk.DISABLED)
                number_entry.configure(state=tk.DISABLED)
            else:
                id_entry.configure(state=tk.NORMAL)
                api_entry.configure(state=tk.NORMAL)
                number_entry.configure(state=tk.NORMAL)
        sms_button = tk.Checkbutton(
            frame, text="SMS", variable=sms_var, onvalue=1, offvalue=0,
            height=5, width=20, command=disable_widgets, pady=1, padx=1)
        sms_button.grid(row=0, column=1, sticky="w")

        id_entry = tk.Entry(frame, width=40, font=FONT)
        id_entry.grid(row=1, column=1, sticky="nw")

        api_entry = tk.Entry(frame, width=60, font=FONT)
        api_entry.grid(row=2, column=1, sticky="nw")

        number_entry = tk.Entry(frame, width=12, font=FONT)
        number_entry.grid(row=3, column=1, sticky="nw")

        email_var = tk.IntVar()

        def disable_widgets_2():
            """unables to make changes in the inputed 'email_entry' and
            'email_pass' widgets to avoid erasing input, widgets will respond
            after unlocking them with 'email_button' checkbutton"""
            if email_var.get() == 0:
                email_entry.configure(state=tk.DISABLED)
                email_pass.configure(state=tk.DISABLED)
            else:
                email_entry.configure(state=tk.NORMAL)
                email_pass.configure(state=tk.NORMAL)

        email_button = tk.Checkbutton(
            frame, text="EMAIL", variable=email_var, onvalue=1, offvalue=0,
            height=5, width=20, command=disable_widgets_2)
        email_button.grid(row=0, column=1)

        email_entry = tk.Entry(frame, width=20, font=FONT)
        email_entry.grid(row=4, column=1, sticky="nw")

        email_pass = tk.Entry(frame, width=20, font=FONT)
        email_pass.grid(row=4, column=1, sticky="ne")

        screen_var = tk.IntVar()
        on_screen_button = tk.Checkbutton(
            frame, text="ON SCREEN NOTIFICATION", variable=screen_var,
            onvalue=1, offvalue=0, height=5, width=20)
        on_screen_button.grid(row=0, column=1, sticky="e")

        from_time_tuple = (
            current_settings[8], "01:00", "02:00", "03:00", "04:00", "05:00",
            "06:00", "07:00", "07:00", "08:00", "09:00", "10:00", "11:00",
            "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00",
            "19:00", "20:00", "21:00", "22:00", "23:00", "24:00")

        to_time_tuple = (
            current_settings[9], "01:00", "02:00", "03:00", "04:00", "05:00",
            "06:00", "07:00", "07:00", "08:00", "09:00", "10:00", "11:00",
            "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00",
            "19:00", "20:00", "21:00", "22:00", "23:00", "24:00")

        break_tuple = (current_settings[10], "15min", "30min", "1h", "2h")

        from_time = tk.Spinbox(frame, values=from_time_tuple, width=5)
        from_time.grid(row=6, column=1, sticky="nw")
        to_time = tk.Spinbox(frame, values=to_time_tuple, width=5)
        to_time.grid(row=7, column=1, sticky="nw")
        break_time = tk.Spinbox(frame, values=break_tuple, width=6)
        break_time.grid(row=8, column=1, sticky="nw")

        sms_var.set(int(current_settings[0]))
        email_var.set(int(current_settings[1]))
        screen_var.set(int(current_settings[2]))
        id_entry.insert(0, current_settings[3])
        api_entry.insert(0, current_settings[4])
        number_entry.insert(0, current_settings[5])
        email_entry.insert(0, current_settings[6])
        email_pass.insert(0, "*"*len(current_settings[7]))

        id_entry.configure(state=tk.DISABLED)
        api_entry.configure(state=tk.DISABLED)
        number_entry.configure(state=tk.DISABLED)
        email_entry.configure(state=tk.DISABLED)
        email_pass.configure(state=tk.DISABLED)
