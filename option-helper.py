import nsepy
from datetime import *
import pandas as pd
import matplotlib.pyplot as plt

"""
Input - SYMBOL, STRIKE PRICE, EXPIRY, OPTION_TYPE, FILE_NAME
Function Will Use NSE PY module and Fetch 15 Days Closing Price of Option
And Save into csv File
"""


def option_execute(_symbol, _strike, _expiry, _option_type, file_name):
    try:
        start_date = date.today() - timedelta(days=15)
        end_date = date.today()
        try:
            expiry_date = date(int(_expiry.split("-")[0]), int(_expiry.split("-")[1]), int(_expiry.split("-")[2]))
        except Exception as error:
            print(error)
            expiry_date = max(nsepy.get_expiry_date(year=end_date.year, month=end_date.month))
        if end_date > expiry_date:
            end_date = expiry_date

        print(_symbol, start_date, end_date, _option_type, _strike, expiry_date)
        stock_opt = nsepy.get_history(symbol=_symbol, index=True,
                                      start=start_date, end=end_date,
                                      option_type=_option_type, strike_price=_strike,
                                      expiry_date=expiry_date)
        print(stock_opt)
        stock_opt.to_csv(file_name, encoding='latin-1')
        return True
    except Exception as error:
        print(error)
        return False


"""
Input - SYMBOL, FILE_NAME
Function Will Use NSE PY module and Fetch 15 Days Closing Price of symbol
And Save into csv File
"""


def execute(_symbol, file_name):
    try:
        start_date = date.today() - timedelta(days=15)
        end_date = date.today()
        print(_symbol, start_date, end_date)
        stock_opt = nsepy.get_history(symbol=_symbol, index=True,
                                      start=start_date, end=end_date)
        print(stock_opt)
        stock_opt.to_csv(file_name, encoding='latin-1')
        print('stock opt')
        return True
    except Exception as error:
        print(error)
        return False


"""
Input - STRIKE PRICE, FILE_NAME
Function Will Use Pandas Module and Matplot lib to find option value & symbol value and will plot a graph
"""


def graph(strike_price, file_op, file_eq):
    try:
        data = pd.read_csv(file_op)
        data_uv = pd.read_csv(file_eq)
        data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')
        pd.set_option('display.max_columns', 25)
        pd.set_option('display.width', 100)

        if len(data) == 0:
            print("No Data Found")
            return False

        _dict = {'Date': [], 'STRIKE PRICE': [], 'Option Price': [], 'LTP': [], 'UV': []}
        dict_uv = {}

        for i in range(len(data_uv)):
            dict_uv[data_uv.iloc[i][0]] = data_uv.iloc[i][4]
        _indices = data[data['Strike Price'] == strike_price].index.values.astype(int)
        for i in range(0, len(_indices)):
            date_i = data.iloc[_indices[i], :][0]
            _dict['Date'].append(date_i)
            _dict['STRIKE PRICE'].append(data.iloc[_indices[i], :][4])
            uv = int(dict_uv[str(date_i)[:10]])
            _dict['UV'].append(uv)
            _dict['LTP'].append(data.iloc[_indices[i], :][9] + uv)
            _dict['Option Price'].append(data.iloc[_indices[i], :][9])
            # dict['UNDERLYING VALUE'].append(data.iloc[indicesofinterest[i], :][16])
            # dict['LTP'].append(data.iloc[indicesofinterest[i], :][9] + data.iloc[indicesofinterest[1], :][16])
        frame = pd.DataFrame(_dict)
        print(frame)
        plt.title('LTP  vs  UV. VALUE')
        plt.plot('Date', 'LTP', data=frame, marker='*', markerfacecolor='green', markersize=12, color='skyblue', linewidth=2,
                 label='OPTION PRICE')
        plt.plot('Date', 'UV', data=frame, marker='*', color='blue', linewidth=2, label='UV VALUE')
        plt.xticks(rotation='vertical')
        plt.legend(loc='upper right')
        plt.show()
        return True
    except Exception as error:
        print(error)
        return False


"""
Default Params
Need to change according to requirement
"""

symbol = 'NIFTY'
strike_price = '15900'
expiry = '2021-07-08'
option_type = 'CE'
file_op = 'data_op.csv'
file_eq = 'data_eq.csv'

try:
    d = option_execute(symbol, int(strike_price), expiry, option_type, file_op)
    if d:
        d = execute(symbol, file_eq)
    if d:
        d = graph(int(strike_price), file_op, file_eq)
except Exception as err:
    print(err)
