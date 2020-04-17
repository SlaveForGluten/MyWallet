"""
send an sms using telesign service (need to register to get an api key
and id number), an email (your gmail must be set up to allow access
from an app) or a on screen message. Message of preset type is send when you
set an alarm and current stock prices are meeting the conditions in the alarm
"""

import smtplib
from tkinter import messagebox
from telesign.messaging import MessagingClient

from Files import scrap_web


def send_sms(name, price, settings):
    """send an sms"""
    customer_id = settings[3]
    api_key = settings[4]

    phone_number = settings[5]
    message_type = "ARN"
    message = name+" "+"current price: "+price

    messaging = MessagingClient(customer_id, api_key)
    messaging.message(phone_number, message, message_type)

    # "3A0AE77E-CB35-43AF-B6F3-9D84E1DEAFF7"
    # "KpMQ5vXAypT6rNG0eJzh/PIbBVcdPsyFIo/2Lzoh+jCyhR7zS0/r8Y0cswNszXOU3BFK4+DwQa85gjce5IGyxw=="


def send_email(name, price, settings):
    """send an email"""
    if scrap_web.pull_current_price('KERNEL') != 'failed to connect':
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(settings[6], settings[7])

        # Send the mail
        msg = "\n"+name+" "+"current price: "+price
        server.sendmail("investment.tracker@gmail.com", settings[6], msg)


def on_screen(name, price):
    """on screen message"""
    msg = name+" "+"current price: "+price
    messagebox.showinfo("Attencion!", msg)
