"""create and manipulate sqlite databese"""

import sqlite3
import time
import datetime

from Files import scrap_web


def create_tables():
    """create db if don't exists and fill it with tables"""
    connect = sqlite3.connect("db.db")
    conn = connect.cursor()
    conn.execute("""CREATE TABLE IF NOT EXISTS assets(
                 timestamp TEXT,
                 amount REAL,
                 currency TEXT,
                 note TEXT)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS gpw_shares(
                 timestamp TEXT,
                 profile TEXT,
                 quantity INT,
                 buying_price REAL,
                 buying_date TEXT,
                 cost REAL,
                 selling_price REAL,
                 selling_date REAL,
                 div TXT)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS gpw_shares_closed(
                 timestamp TEXT,
                 profile TEXT,
                 quantity INT,
                 buying_price REAL,
                 buying_date TEXT,
                 cost REAL,
                 selling_price REAL,
                 selling_date REAL,
                 div TXT)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS current_price(
                 profile TEXT UNIQUE PRIMARY KEY ,
                 price TEXT)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS reports(
                 profile TEXT,
                 title TEXT,
                 I TEXT,
                 II TEXT,
                 III TEXT,
                 IV TEXT,
                 V TEXT,
                 VI TEXT,
                 VII TEXT,
                 VIII TEXT)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS currency_rates(
                 currency TEXT UNIQUE,
                 value TEXT)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS settings(
                 sms TEXT,
                 mail TEXT,
                 screen TEXT,
                 id TEXT,
                 api TEXT,
                 telephone TEXT,
                 email TEXT,
                 email_pass TEXT,
                 message_from TEXT,
                 message_to TEXT,
                 break TEXT)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS alarms(
                 profile TEXT UNIQUE,
                 high REAL,
                 low REAL)""")
    connect.commit()
    connect.close()


def get_timestamp():
    """get current date and time"""
    unix = time.time()
    timestamp = str(datetime.datetime.fromtimestamp(unix).strftime(
        '%d-%m-%Y %H:%M:%S'))
    return timestamp


def delete_row_from_table(table, column, value):
    """deletes row from given table if 'value' in 'column' matches'"""
    connect = sqlite3.connect("db.db")
    conn = connect.cursor()
    conn.execute("DELETE from " + table + " WHERE " + column + " = :" + column,
                 {column: value})
    connect.commit()
    connect.close()


def fetch_all_from_table(table):
    """^^"""
    connect = sqlite3.connect("db.db")
    conn = connect.cursor()
    conn.execute("SELECT * FROM " + table)
    assets = conn.fetchall()
    connect.close()
    return assets


def fetch_reports(profile):
    """returns quarterly reports of a given share"""
    connect = sqlite3.connect("db.db")
    conn = connect.cursor()
    conn.execute("SELECT * FROM reports WHERE profile=:profile",
                 {'profile': profile})
    val = conn.fetchall()
    connect.close()
    return val


def fetch_current_price(profile):
    """returns current price of given share"""
    connect = sqlite3.connect("db.db")
    conn = connect.cursor()
    conn.execute("SELECT price FROM current_price WHERE profile=:profile",
                 {'profile': profile})
    price = conn.fetchone()
    connect.close()
    if price:
        return price[0]
    else:
        return '40.0000 -1.01% -6.0000 2020-04-09 15:48:37'


def fetch_alarm(profile):
    """returns alarm details of a given profile"""
    connect = sqlite3.connect("db.db")
    conn = connect.cursor()
    conn.execute("SELECT * FROM alarms WHERE profile=:profile",
                 {'profile': profile})
    alarm = conn.fetchone()
    connect.close()
    if alarm is None:
        return (profile, "", "")
    else:
        return alarm


def add_asset(asset_dict):
    """add new asset to the 'assets' table"""
    connect = sqlite3.connect("db.db")
    conn = connect.cursor()
    conn.execute("""INSERT INTO assets VALUES(
        :timestamp, :amount, :currency, :note)""",
                 {'timestamp': get_timestamp(),
                  'amount': asset_dict['Amount'],
                  'currency': asset_dict['Currency'],
                  'note': asset_dict['Note']})
    connect.commit()
    connect.close()


def add_share(table, share_dict):
    """ad new share to the 'gpw_shares' table"""
    connect = sqlite3.connect("db.db")
    conn = connect.cursor()
    conn.execute("INSERT INTO " + table + """ VALUES(
        :timestamp, :profile, :quantity, :buying_price, :buying_date, :cost,
        :selling_price, :selling_date, :div)""",
                 {'timestamp': get_timestamp(),
                  'profile': share_dict['Name'],
                  'quantity': share_dict['Quantity'],
                  'buying_price': share_dict['BuyingPrice'],
                  'buying_date': share_dict['BuyingDate'],
                  'cost': share_dict['Cost'],
                  'selling_price': share_dict['SellingPrice'],
                  'selling_date': share_dict['SellingDate'],
                  'div': share_dict['Dividends']})
    connect.commit()
    connect.close()


def add_current_price(profile, price):
    """ad current price to the 'current_price' table"""
    connect = sqlite3.connect("db.db")
    conn = connect.cursor()
    conn.execute("""INSERT OR REPLACE INTO current_price(profile, price)
                    VALUES ('{0}','{1}');""".format(profile, price))
    connect.commit()
    connect.close()


def add_currency_rates(curr_dict):
    """replace currency rates in the 'currency_rates' table"""
    if curr_dict:
        connect = sqlite3.connect("db.db")
        conn = connect.cursor()
        for key, value in curr_dict.items():
            conn.execute("""INSERT OR REPLACE INTO currency_rates(
                currency, value) VALUES ('{0}','{1}');""".format(key, value))
        connect.commit()
        connect.close()


def add_quarterly_reports(reports_list):
    """add quarterly reports to the 'reports' table'"""
    connect = sqlite3.connect("db.db")
    conn = connect.cursor()
    for _, val in enumerate(reports_list):
        conn.execute("""INSERT INTO reports VALUES(:profile, :title, :I,
        :II, :III, :IV, :V, :VI, :VII, :VIII)""",
                     {'profile': val[0],
                      'title': val[1],
                      'I': val[2],
                      'II': val[3],
                      'III': val[4],
                      'IV': val[5],
                      'V': val[6],
                      'VI': val[7],
                      'VII': val[8],
                      'VIII': val[9]})
    connect.commit()
    connect.close()


def add_settings(settings_dict):
    """replace settings in the 'settings' table"""
    connect = sqlite3.connect("db.db")
    conn = connect.cursor()
    conn.execute("""INSERT INTO settings VALUES(
        :sms, :mail, :screen, :id, :api, :telephone, :email,
        :email_pass, :message_from, :message_to, :break)""",
                 {'sms': settings_dict['sms'],
                  'mail': settings_dict['mail'],
                  'screen': settings_dict['screen'],
                  'id': settings_dict['id'],
                  'api': settings_dict['api'],
                  'telephone': settings_dict['p_number'],
                  'email': settings_dict['email'],
                  'email_pass': settings_dict['email_pass'],
                  'message_from': settings_dict['from'],
                  'message_to': settings_dict['to'],
                  'break': settings_dict['break']})
    connect.commit()
    connect.close()


def add_alarm(profile, high, low):
    """add alarms to the 'alarms' table'"""
    connect = sqlite3.connect("db.db")
    conn = connect.cursor()
    conn.execute("""INSERT OR REPLACE INTO alarms(profile, high, low)
                 VALUES ('{0}', '{1}', '{2}');""".format(profile, high, low))
    connect.commit()
    connect.close()


def check_for_real_numbers(value):
    """check if inputed value is a real number"""
    val = value
    if value[0] == '-':
        val = value[1:len(value)]
    if val.find("."):
        if (val.replace(".", "1", 1)).isnumeric() is False:
            return False
    else:
        if val.isnumeric():
            return False
    return True


def check_if_valid_name(name):
    """compare profile name with the names in the 'gpw_profiles.txt' file"""
    try:
        container = open("gpw_profiles.txt", "r")
        gpw_profiles = container.read()
        container.close()
    except IOError:
        container.close()
    if name in gpw_profiles:
        return True
    else:
        return False


def check_date_format(date):
    """check if date format fits the DD/MM/YYYY format"""
    if len(date) != 10:
        return False
    if(date[0:1].isnumeric() is False or
       date[3:4].isnumeric() is False or
       date[6:9].isnumeric() is False):
        return False
    if date[2] and date[5] != ".":
        return False
    if 0 < int(date[0:1]) <= 31 is False:
        return False
    if 0 < int(date[3:4]) <= 12 is False:
        return False
    return True


def update_current_price():
    """update current price of shares added to 'gpw_shares' and 'watched'
       tables"""
    shares = fetch_all_from_table('current_price')
    for share in shares:
        current_price = scrap_web.pull_current_price(share[0])
        if current_price != 'failed to connect':
            delete_row_from_table('current_price', 'profile', share[0])
            add_current_price(share[0], current_price)


def update_watched_shares():
    """pull new quarterly reports of all shares in 'watched' table"""
    list_of_reports = list()
    for profile in fetch_all_from_table("current_price"):
        prof = fetch_reports(profile[0])
        if prof:
            list_of_reports.append(prof)

    for share in list_of_reports:
        pulled_data = scrap_web.historical_data(share[0][0])
        if pulled_data == "failed to connect":
            pass
            # updated_shares.append(dictionary_to_string(pulled_data))
        else:
            delete_row_from_table("reports", "profile", share[0][0])
            add_quarterly_reports(pulled_data)


def remove_unused_prices_and_alarms():
    """clear 'current_price and 'alarms' tables from profiles that do not exist
    in 'gpw_shares' or 'watched' tables """
    active_profiles = list()
    prices = list()
    alarms = list()
    # get all current_prices
    for price in fetch_all_from_table("current_price"):
        prices.append(price[0])
    # get all alarms
    for alarm in fetch_all_from_table("alarms"):
        alarms.append(alarm[0])
    # get profiles from reports table
    for profile in prices:
        prof = fetch_reports(profile)
        if prof:
            active_profiles.append(prof[0][0])
    # get profiles from gpw_shares table
    for profile in fetch_all_from_table("gpw_shares"):
        if profile[6] == "":
            active_profiles.append(profile[1])
    # remove active profiles from 'prices' list
    for prof in active_profiles:
        if prof in prices:
            prices.remove(prof)
    # remove active profiles from 'alarms' list
    for prof in active_profiles:
        if prof in alarms:
            alarms.remove(prof)
    # delete inactive profiles from 'current_price' table
    for prof in prices:
        delete_row_from_table('current_price', 'profile', prof)
    # delete inactive profiles from 'alarms' table
    for prof in alarms:
        delete_row_from_table('alarms', 'profile', prof)


def check_time(start_time, end_time):
    """check if right time to send the allarm"""
    time_now = time.localtime().tm_hour
    start_time = start_time[0:2].lstrip("0")
    end_time = end_time[0:2].lstrip("0")

    if int(start_time) <= int(time_now) < int(end_time):
        return "alarm on"
    else:
        return "alarm off"

