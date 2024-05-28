import time
from moomoo import *
import yfinance as yf
import threading
from concurrent.futures import ThreadPoolExecutor
import schedule

tickers = ['MSFT',
           'AAPL',
           'NVDA',
           'GOOGL',
           'AMZN',
           'TSLA',
           'NFLX',  # 比较一下... 改weight
           '^GSPC']  #Last = index, ^GSPC from Yahoo

w_list = [ 0.23,
           0.196,
           0.186,
           0.137,
           0.12,
           0.074,
           0.035,
           0.022 ] # 8 个w

# example iv_map = { 'MSFT': { 'US.NVDA240816C1070000': 0.1, 'US.NVDA240816P1070000': 0.2, 'US.SPXW240528C5305000': 0.3, 'US.SPXW240528P5305000': 0.4} }  # 8 个iv
iv_map = {}

# imp_rho_time_series = [{'time': 123456, "value":12.0}]  # 时间序列，每个时间点对应一个字典，字典里是iv
cor3m_time_series = []  # 用来存储历史的imp_rho

stock_to_option = {}  # 用来存储每个股票对应的option
option_to_stock = {}  # 用来存储每个option对应的股票

current_subscribe_options = []  # 用来存储上一次订阅的期权

ticker_price_dict = {} # 用来存储每个股票的当前价格

def convert_to_option_symbol(symbol):
    if symbol.startswith('GOOGL'):
        prefix = 'US.GOOG' + symbol[5:12]
        suffix = symbol[12:]
    else:
        prefix = 'US.' + symbol[:11]
        suffix = symbol[11:]
    return prefix + str(int(suffix))



def get_stock_iv(spot, option1, option2, iv1, iv2, iv3, iv4):
    k1 = float(option1[14:]) / 1000
    k2 = float(option2[14:]) / 1000
    aux = (spot - k2) / (k1 - k2)
    return (iv1 + iv2) * (1 - aux) + (iv3 + iv4) * aux

def imp_rho(iv,w):
    small_var = 0
    avg_vol = 0
    for i in range(len(w)):
        avg_vol += w[i]*iv[i]
        small_var += w[i]*w[i]*iv[i]*iv[i]
    return (iv[len(w)-1]*iv[len(w)-1]-small_var)/(avg_vol*avg_vol-small_var)


def find_nearest_options(ticker):
        
    # Get the stock data
    stock = yf.Ticker(ticker)
    # print('current_price:', current_price)
    # Get the options chain
    if ticker == '^GSPC':
        spx = yf.Ticker("^SPX")
        options = spx.option_chain(spx.options[0])
    else:
        options = stock.option_chain(stock.options[0])

    # Separate the calls and puts
    calls = options.calls
    puts = options.puts

    # Find the call and put options with strike prices closest to the current stock price
    nearest_call = calls.iloc[(calls['strike'] - ticker_price_dict[ticker]).abs().argsort()[:2]]
    nearest_put = puts.iloc[(puts['strike'] - ticker_price_dict[ticker]).abs().argsort()[:2]]
    
    # Format the contract symbols
    nearest_call_symbols = [ convert_to_option_symbol(symbol=symbol) for symbol in nearest_call['contractSymbol'].tolist()]
    nearest_put_symbols = [ convert_to_option_symbol(symbol=symbol) for symbol in nearest_put['contractSymbol'].tolist()]

    return nearest_call_symbols, nearest_put_symbols

class OptionOnsubscribe(StockQuoteHandlerBase):
    def __init__(self):
        super().__init__()
        self.counter = 0
        self.start_time = time.time()
        self.timer = threading.Timer(1, self.print_and_reset_counter)
        self.timer.start()

    

    def handle_data(self, data):
        global iv_map
        for index, row in data.iterrows():
            option = row['code']
            stock = option_to_stock[option]
            iv_new = row['implied_volatility']
            iv_old = iv_map[stock][option]
            if iv_new != iv_old:
                iv_map[stock][option]['iv'] = iv_new
                self.counter += 1

    def print_and_reset_counter(self):
        elapsed_time = time.time() - self.start_time
        # print(f'handle_data was called {self.counter} times in the last {elapsed_time:.2f} seconds.')
        self.counter = 0
        self.start_time = time.time()
        self.timer = threading.Timer(1, self.print_and_reset_counter)
        self.timer.start()
        
    def on_recv_rsp(self, rsp_pb):
        ret_code, data = super(OptionOnsubscribe,self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            print("OptionOnsubscribe: error, msg: %s" % data)
            return RET_ERROR, data
        # 处理data
        self.handle_data(data)
        return RET_OK, data

def unsubscribe(unsubscribe_options):
    # 取消订阅过期的期权
    if len(unsubscribe_options) > 0:
        ret, data = quote_ctx.unsubscribe(unsubscribe_options, [SubType.QUOTE])
        if ret != RET_OK:
            raise Exception('unsubscribe error:', data)
        else:
            # 删除过期的期权数据
            for option in unsubscribe_options:
                ticker = option_to_stock[option]
                del option_to_stock[option]
                stock_to_option[ticker].remove(option)
                del iv_map[ticker][option]
            print('unsubscribe success:', unsubscribe_options)

def refresh_iv_map():
    global iv_map, current_subscribe_options
    subscribe_options = []
    for ticker in tickers:
        call_options, put_options = find_nearest_options(ticker)
        # 初始化iv_map
        if ticker not in iv_map:
            iv_map[ticker] = {} # 用来存储每个option对应的iv
        # 将call_options和put_options加入到iv_map中
        for call_option in call_options:
            if call_option not in iv_map[ticker]:
                iv_map[ticker][call_option] = { 'strike_price': float(call_option[14:]) / 1000, 'type': 'CALL', 'iv': -1, 'on': True}
            else:
                iv_map[ticker][call_option]['on'] = True
        for put_option in put_options:
            if put_option not in iv_map[ticker]:
                iv_map[ticker][put_option] = { 'strike_price': float(put_option[14:]) / 1000, 'type': 'PUT', 'iv': -1, 'on': True}
            else:
                iv_map[ticker][put_option]['on'] = True

        # 更新stock_to_iv和iv_to_stock
        if ticker in stock_to_option:
            stock_to_option[ticker].extend(call_options + put_options)
        else:
            stock_to_option[ticker] = call_options + put_options
        for call_option in call_options:
            option_to_stock[call_option] = ticker
        for put_option in put_options:
            option_to_stock[put_option] = ticker
        
        # 合并到subscribe_options
        subscribe_options.extend(call_options + put_options)
    # 取消订阅过期的期权
    unsubscribe_options = list(set(current_subscribe_options) - set(subscribe_options))
    if len(unsubscribe_options) > 0:
        for option in unsubscribe_options:
            iv_map[option_to_stock[option]][option]['on'] = False # 将对应的option的on设置为False
        # Set a timer to trigger the unsubscribe function after 60 seconds
        timer = threading.Timer(60, unsubscribe, args=[unsubscribe_options])
        timer.start()
    # 订阅新的期权
    new_subscribe_options = list(set(subscribe_options) - set(current_subscribe_options))
    if len(new_subscribe_options) > 0:
        print('new_subscribe_options:', new_subscribe_options)
        ret, data = quote_ctx.subscribe(new_subscribe_options, [SubType.QUOTE])
        if ret != RET_OK:
            print('subscribe error:', data)
            raise Exception('subscribe error:', data)
        else:
            print('subscribe success:', new_subscribe_options)
    # 更新current_subscribe_options
    current_subscribe_options = subscribe_options


            
def get_avg_iv():
    global iv_map
    iv_list = []
    for ticker in tickers:
        # Get all options with 'on' set to True
        on_options = [option for option, data in iv_map[ticker].items() if data['on']]
        # Sort the options by their names
        sorted_options = sorted(on_options)
        iv_list.append(get_stock_iv(ticker_price_dict[ticker], sorted_options[1], sorted_options[0], iv_map[ticker][sorted_options[1]]['iv'], iv_map[ticker][sorted_options[3]]['iv'], iv_map[ticker][sorted_options[0]]['iv'], iv_map[ticker][sorted_options[2]]['iv']))
    return iv_list

def check_all_updated():
        global iv_map
        iv_list = []
        for ticker in tickers:
            for option in stock_to_option[ticker]:
                # Check if the iv_map[ticker] have 4 options    
                if len(iv_map[ticker]) < 4:
                    raise Exception('iv_map is not fully initialized.')
                for option in stock_to_option[ticker]:
                    iv_list.append(iv_map[ticker][option]['iv'])
        for iv in iv_list:
            if iv < 0:
                return False
        return True

def print_cor3m():
    global iv_map, w_list, cor3m_time_series, cor3m_time_series
    if not check_all_updated():
        print('not all updated')
    w = w_list
    stock_iv = get_avg_iv()
    cor3m_time_series.append({'time':time.time(),'value': imp_rho(stock_iv, w)})
    print('cor3m:', cor3m_time_series[-1])

def update_current_price(ticker):
    global ticker_price_dict
    stock = yf.Ticker(ticker)
    # Get the current stock price
    if ticker == '^GSPC':
        current_price = (stock.info['bid'] + stock.info['ask']) / 2
    else:
        current_price = stock.info['currentPrice']
    ticker_price_dict[ticker] = current_price
    
def update_price_continuously(ticker):
    while True:
        try:
            update_current_price(ticker)
        except Exception as e:
            print("update_price_continuously", e)
        time.sleep(1)

def refresh_iv_map_continuously():
    while True:
        try:
            refresh_iv_map()
        except Exception as e:
            print("refresh_iv_map_continuously", e)
        time.sleep(1)

def print_cor3m_continuously():
    while True:
        try:
            print_cor3m()
        except Exception as e:
            print("print_cor3m_continuously", e)
        time.sleep(1)

if __name__ == '__main__':
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    handler = OptionOnsubscribe()
    quote_ctx.set_handler(handler) # Set real-time quote callback
    with ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(update_price_continuously, tickers)
        executor.submit(refresh_iv_map_continuously)
        executor.submit(print_cor3m_continuously)
