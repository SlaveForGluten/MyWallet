"""pull content from the bankier.pl website """

from bs4 import BeautifulSoup
import urllib3
from urllib3.exceptions import MaxRetryError
from urllib3.exceptions import ConnectionError

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def pull_current_price(name):
    """
    downloads and returns current price, price change by percent and value and
    the time of last price check
    """
    url = 'https://www.bankier.pl/inwestowanie/profile/quote.html?symbol='+name
    try:
        http = urllib3.PoolManager()
        raw = http.request("GET", url)
    except ConnectionError:
        return "failed to connect"
    except MaxRetryError:
        return "failed to connect"
    soup = BeautifulSoup(raw.data, 'lxml')
    price = soup.find("div", {"class": "profilLast"})
    price = price.getText().rstrip(" zł").replace(",", ".")

    pkt_and_prc_change = soup.findAll("span", {"class": "value"})
    val_change = pkt_and_prc_change[0].getText()
    val_change += " "+pkt_and_prc_change[1].getText()
    val_change = val_change.strip("zł").replace(",", ".")

    time = soup.find("time", {"class": "time"})
    time = time.getText()
    return price+" "+val_change.replace("\n", " ")+time


def historical_data(name):
    """pull quarterly reports of a given company"""
    url = ('https://www.bankier.pl/gielda/notowania/akcje/'+name +
           '/wyniki-finansowe/skonsolidowany/kwartalny/standardowy/2')
    url2 = ('https://www.bankier.pl/gielda/notowania/akcje/'+name +
            '/wyniki-finansowe/skonsolidowany/kwartalny/standardowy/1')

    quarters = list()
    net_income = list()
    net_profit = list()
    book_value = list()
    num_of_shares = list()
    for link in (url, url2):
        try:
            http = urllib3.PoolManager()
            raw = http.request("GET", link)
        except ConnectionError:
            return("failed to connect")
        except MaxRetryError:
            return("failed to connect")
        soup = BeautifulSoup(raw.data, 'lxml')
        raw_quarter = soup.findAll("th", {"class": "textAlignCenter"})
        for quar in range(0, 4):
            quarters.append(raw_quarter[quar].getText())

        soup = BeautifulSoup(raw.data, 'lxml')
        raw_values = soup.findAll("td", {"class": "textAlignRight"})
        for q in range(0, 36):
            if 0 <= q < 4:
                net_income.append(raw_values[q].getText().replace("\xa0", ""))
            if 11 < q < 16:
                net_profit.append(raw_values[q].getText().replace("\xa0", ""))
            if 27 < q < 32:
                book_value.append(raw_values[q].getText().replace("\xa0", ""))
            if 31 < q < 36:
                num_of_shares.append(
                    raw_values[q].getText().replace(
                        "\xa0", "").replace(",", ""))

    av_price = convert_date_to_code(quarters, name)

    list_of_tuples = list()
    list_of_values = (quarters, av_price, net_income, net_profit, book_value,
                      num_of_shares)
    for i, val in enumerate(list_of_values):
        tup = ("quarters", "av_price", "net_income", "net_profit",
               "book_value", "num_of_shares")
        report_tuple = (name, tup[i], val[0], val[1], val[2], val[3], val[4],
                        val[5], val[6], val[7])
        list_of_tuples.append(report_tuple)

    return list_of_tuples


def pull_average_price(start, end, name):
    """pull average price """
    url = ('https://www.bankier.pl/new-charts/get-data?date_from='+start +
           '&date_to='+end+'&symbol='+name+'&intraday=false&type=area')
    try:
        http = urllib3.PoolManager()
        raw = http.request("GET", url)
    except ConnectionError:
        return "failed to connect"
    except MaxRetryError:
        return "failed to connect"
    soup = BeautifulSoup(raw.data, 'lxml')
    string = soup.getText().split('":{')
    string = string[1].split('},"')
    list_of_values = string[0].split('"volume":')

    for val in list_of_values[0].split(',"'):
        if 'prevCloseDate' in val:
            prev_close = val.strip('"prevCloseDate":"')
        if 'startDate' in val:
            start = val.strip('startDate":"').strip('"')
        if 'endDate' in val:
            end = val.strip('endDate":"')
        if 'valueAverage' in val:
            av_val = val.strip('valueAverage":"').replace(',', '.')

    av_price_dict = {"Start": start[2:10],
                     "End": end[2:10],
                     "PrevClose": prev_close,
                     "AvPrice": av_val}
    return av_price_dict


def convert_date_to_code(quarters, name):
    """bankier.pl website translates dates to numerical code. In order to pull
    average price of share from given period I need to translate border dates
    of this period to their code. This function does that.
    """
    start = 1451606400000  # 1st January 2016
    quarter = 7776000000  # 3 months period
    day = 86400000
    starting_year = 16
    year_of_the_first_quarter = quarters[0][len(quarters[0])-2:len(quarters[0])+1]

    # set starting year
    while int(year_of_the_first_quarter) != starting_year:
        starting_year += 1
        start += (4*quarter)

    # set starting quarter
    if quarters[0].split(" Q ")[0] == "I":
        pass
    elif quarters[0].split(" Q ")[0] == "II":
        start += quarter
    elif quarters[0].split(" Q ")[0] == "III":
        start += quarter*2
    elif quarters[0].split(" Q ")[0] == "IV":
        start += quarter*3

    end = start + quarter
    # adjust year
    date = pull_average_price(str(start), str(end), name)
    while date['Start'][0:2] != year_of_the_first_quarter:
        start += day
        end += day
        date = pull_average_price(str(start), str(end), name)
    list_of_results = list()
    for _ in range(0, 8):
        date = pull_average_price(str(start), str(end), name)
        # adjust month
        while date["PrevClose"][3:5] == date["Start"][3:5]:
            start += day
            end += day
            date = pull_average_price(str(start), str(end), name)
        list_of_results.append(date['AvPrice'])
        start += quarter + day
        end = start + quarter
    return list_of_results


def pull_currency_rates():
    """current rates of most popular currencies to PLN"""
    currencies = ["USDPLN", "EURPLN", "GBPPLN", "CHFPLN"]
    currencies_dict = dict()
    for curr in currencies:
        url = 'https://www.bankier.pl/waluty/kursy-walut/forex/'+curr
        try:
            http = urllib3.PoolManager()
            raw = http.request("GET", url)
        except ConnectionError:
            return False
        except MaxRetryError:
            return False
        soup = BeautifulSoup(raw.data, 'lxml')
        rate = soup.find("div", {"class": "profilLast"})
        rate = rate.getText().strip().replace(",", ".")
        currencies_dict[curr] = rate
    return currencies_dict
