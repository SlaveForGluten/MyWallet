"""do math for other modules"""

import datetime

from Files import manage_db

COMMISSION = 0.0039
COMMISSION_TWO = 3
INCOME_TAX = 0.19


def total_dividend(all_dividends):
    """
    calculate total dividends from a single share by adding all the entries
    """
    tot_div = 0
    if all_dividends == "":
        return 0
    else:
        for div_and_date in all_dividends.split("|"):
            for div_or_date in div_and_date.split("-"):
                # filter date
                if div_or_date.count(".") == 2:
                    pass
                # add dividend
                else:
                    tot_div += float(div_or_date)
    return round(float(tot_div), 2)


def total_costs(total_price_when_bought, total_price_when_sold):
    """
    Calculate all costs of buying and selling shares.
    Bank commission is 0.0039 (mBank) of transaction, unless,
    it's less than 3 PLN, then it's 3 PLN
    income tax in Poland is 0.19 of profit made
    """
    # calculate buying commission
    buing_cost = 0
    if total_price_when_bought*COMMISSION < 3:
        buing_cost = COMMISSION_TWO
    else:
        buing_cost = total_price_when_bought*COMMISSION
    # calculate selling commission
    selling_cost = 0
    if total_price_when_sold*COMMISSION < 3:
        selling_cost = COMMISSION_TWO
    else:
        selling_cost = total_price_when_sold*COMMISSION
    # calculate income tax
    tax_cost = 0
    if total_price_when_sold > total_price_when_bought:
        tax_cost = (total_price_when_sold - total_price_when_bought)*0.19

    return buing_cost + selling_cost + tax_cost


def count_days(bought_day, sold_day):
    """
    Calculate how long investment lasted by comparing start and end date.
    For investments that did not ended end date is current date.
    """
    if sold_day == "":
        sold_day = datetime.date.today()
    else:
        d_m_y_list = sold_day.split(".")
        sold_day = datetime.date(
            int(d_m_y_list[2]), int(d_m_y_list[1]), int(d_m_y_list[0]))

    d_m_y_list = bought_day.split(".")
    bought_day = datetime.date(
        int(d_m_y_list[2]), int(d_m_y_list[1]), int(d_m_y_list[0]))
    diff = sold_day - bought_day
    if diff.days == 0:
        return 1
    return int(diff.days)


def annual_ror(share, curent_price_per_share, costs, total_div):
    """calculate annual rate of return"""
    # rate of return = (result/when_bought)-1
    # annual rate of return = ((1+rate of return)^(365/days investment lasted)-1)
    total_price_now = share[2]*curent_price_per_share
    total_price_when_bought = share[2]*share[3]

    rate_of_return = (
        (total_price_now - float(costs) + total_div)/total_price_when_bought-1)

    investment_time = count_days(share[4], share[7])

    annual_rate_of_return = ((1+rate_of_return) ** (365/investment_time)-1)*100
    return round(annual_rate_of_return, 2)


def shares_worth(list_of_shares):
    """return list of tuples containing (name_of_the_share, total_worth_of_packet)
    and sorted from smallest to biggest (by worth)"""

    # merge packets of same shares, produce dictionary with share name as key
    # and current total value as value
    name_and_value = dict()
    for share in list_of_shares:
        if name_and_value.get(share[1]):
            name_and_value[share[1]] = name_and_value[share[1]] + round(
                float(manage_db.fetch_current_price(share[1]).split(" ")[0]) * share[2], 2)
        else:
            print(manage_db.fetch_current_price(share[1]))
            print(manage_db.fetch_current_price(share[1]).split(" "))
            print(manage_db.fetch_current_price(share[1]).split(" ")[0])
            name_and_value[share[1]] = round(
                float(manage_db.fetch_current_price(share[1]).split(" ")[0]) * share[2], 2)

    return (sorted(name_and_value.items(), key=lambda kv: (kv[1], kv[0])))


def seven_biggest_shares(list_of_shares):
    """return list containing up to seven most valuable shares in the wallet
    (by total worth). Single share is a tuple with [0]name and [1]worth.
    The tuples are sorted in the list from biggest to smallest"""
    top_seven = list()
    for i in range(0, len(list_of_shares)):
        if len(top_seven) < 7:
            top_seven.append(list_of_shares[len(list_of_shares) - 1 - i])
    return top_seven


def totaled_shares_worth():
    list_of_shares = manage_db.fetch_all_from_table("gpw_shares")
    worth_totaled = 0
    for share in list_of_shares:
        current_price = float(
            manage_db.fetch_current_price(share[1]).split(" ")[0])
        worth_totaled += (share[2] * current_price)
    return round(worth_totaled, 2)


def profit_per_share(share):

    curent_price = manage_db.fetch_current_price(share[1])

    curent_val_per_s = float(curent_price.split(" ")[0])
    total_buying_price = share[2]*share[3]
    total_selling_price = share[2]*curent_val_per_s
    total_div = total_dividend(share[8])
    total_cost_of_share = total_costs(total_buying_price, total_selling_price)

    profit = round((total_selling_price - total_buying_price +
                    total_div - total_cost_of_share), 2)
    return profit


def profit_per_packet(list_of_shares):
    """different packets of same share are added so I can display totaled profit"""

    # list of tuples containing name[0] of the share and profit[1] it made
    packet_profit = dict()
    # calculate profit for single share
    for share in list_of_shares:
        curent_price = manage_db.fetch_current_price(share[1])

        curent_val_per_s = float(curent_price.split(" ")[0])
        total_buying_price = share[2]*share[3]
        total_selling_price = share[2]*curent_val_per_s
        total_div = total_dividend(share[8])
        total_cost_of_share = total_costs(total_buying_price, total_selling_price)
        profit = round((total_selling_price - total_buying_price +
                        total_div - total_cost_of_share), 2)
        if packet_profit.get(share[1]):
            packet_profit[share[1]] = packet_profit[share[1]] + round(profit, 2)
        else:
            packet_profit[share[1]] = round(profit, 2)

    return packet_profit


def calculate_percentage(total_worth, share_worth):
    return round((share_worth/total_worth)*100, 2)


def add_liquid_assets():
    list_of_assets = manage_db.fetch_all_from_table("assets")
    added_values = {'pln': 0, 'eur': 0, 'gbp': 0, 'usd': 0, 'chf': 0}

    # add same currencies
    for asset in list_of_assets:
        if asset[2] == "USD":
            added_values['usd'] += asset[1]
        elif asset[2] == "EUR":
            added_values['eur'] += asset[1]
        elif asset[2] == "GBP":
            added_values['gbp'] += asset[1]
        elif asset[2] == "PLN":
            added_values['pln'] += asset[1]
        elif asset[2] == "CHF":
            added_values['chf'] += asset[1]
    return added_values


def sum_all_wealth():
    assets = add_liquid_assets()
    shares_worth_totaled = totaled_shares_worth()
    rates_list = manage_db.fetch_all_from_table("currency_rates")

    total = (assets['pln'] + assets['eur']*float(rates_list[1][1]) +
             assets['gbp'] * float(rates_list[2][1]) + assets['usd'] *
             float(rates_list[0][1]) + assets['chf'] * float(rates_list[3][1])
             + shares_worth_totaled)
    return total


def add_profit_of_given_shares(list_of_shares):
    """takes in string 'gpw_shares' or 'gpw_shares_closed' and returns their
    summarized profit"""
    shares_to_count = manage_db.fetch_all_from_table(list_of_shares)
    profit_totaled = 0
    for share in shares_to_count:
        profit_totaled += profit_per_share(share)
    profit_totaled = round(profit_totaled, 2)
    return profit_totaled


def values_for_historical_transactions():
    """costs, profits etc. of historical transactions are fixed and
    saved in db, this function adds or sorts them and returns then as a
    dictionary to display"""
    all_shares = manage_db.fetch_all_from_table("gpw_shares_closed")

    dict = {
        'total_profit': 0,
        'total_costs': 0,
        'average_annual_ror': 0,
        'biggest_profit': 0,
        'biggest_profit_profile': '',
        'biggest_lose': 0,
        'biggest_lose_profile': ''
    }

    profit = cost = ror = counter = profit_per_tras = lose = 0
    biggest_profit_prolile = biggest_lose_profile = ''

    for share in all_shares:
        total_buying_price = share[2]*share[3]
        total_selling_price = share[2]*share[6]
        total_div = total_dividend(share[8])
        holder = (total_selling_price - total_buying_price +
                  total_div - share[5])
        # biggest profit per transaction
        if holder > profit_per_tras:
            profit_per_tras = holder
            biggest_profit_prolile = share[1]
        # biggest lose per transaction
        if holder < lose:
            lose = holder
            biggest_lose_profile = share[1]
        # add profit
        profit += holder
        # add costs
        cost += share[5]
        # average annual ror
        ror += annual_ror(share, share[6], share[5], total_dividend(share[8]))
        counter += 1
        holder = profit_per_share(share)

    dict['total_profit'] = round(profit, 2)
    dict['total_costs'] = round(cost, 2)
    dict['average_annual_ror'] = round(ror / counter, 2)
    dict['biggest_profit'] = round(profit_per_tras, 2)
    dict['biggest_profit_profile'] = biggest_profit_prolile
    dict['biggest_lose'] = round(lose, 2)
    dict['biggest_lose_profile'] = biggest_lose_profile
    return dict
