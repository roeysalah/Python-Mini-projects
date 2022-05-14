# None of these imports are strictly required, but use of at least some is strongly encouraged
# Other imports which don't require installation can be used without consulting with course staff.
# If you feel these aren't sufficient, and you need other modules which require installation,
# you're welcome to consult with the course staff.
import math
import numpy as np
import pandas as pd
from datetime import date
import itertools
import yfinance as yf
import pandas_datareader as pdr
from typing import List


class PortfolioBuilder:

    def get_daily_data(self, tickers_list: List[str],start_date: date,end_date: date = date.today()) -> pd.DataFrame:
        """
        get stock tickers adj_close price for specified dates.

        :param List[str] tickers_list: stock tickers names as a list of strings.
        :param date start_date: first date for query
        :param date end_date: optional, last date for query, if not used assumes today
        :return: daily adjusted close price data as a pandas DataFrame
        :rtype: pd.DataFrame

        example call: get_daily_data(['GOOG', 'INTC', 'MSFT', ''AAPL'], date(2018, 12, 31), date(2019, 12, 31))
        """
        try:
            data = pdr.DataReader(tickers_list,'yahoo',start_date,end_date)
            df_close=data['Adj Close']
            self.stock_data = data
            self.tickers_list = tickers_list
            if df_close.isnull().values.any():
                raise ValueError
            return data['Adj Close']
        except Exception:
            raise  ValueError

    def find_universal_portfolio(self, portfolio_quantization: int = 20) -> List[float]:
        """
        calculates the universal portfolio for the previously requested stocks

        :param int portfolio_quantization: size of discrete steps of between computed portfolios. each step has size 1/portfolio_quantization
        :return: returns a list of floats, representing the growth trading  per day
        """
        stock_data = self.stock_data['Adj Close']
        number_of_stocks = len(self.tickers_list)
        p_f_q=portfolio_quantization

        # x_vec init
        x_vec = []
        for i in range(len(stock_data)-1):
            x_vec.append(list(stock_data.iloc[i+1] / stock_data.iloc[i]))
        x_vec=np.array(x_vec)

        a=(1 / p_f_q)
        b = np.arange(0.0, 1.0,a)
        b = np.append(1.0, b)
        product = list(itertools.product(b, repeat=number_of_stocks))
        all_perm = [np.round(i, 10) for i in product]
        # b_vec init
        b_vec_inittial=np.zeros(number_of_stocks)
        b_vec_inittial+=(1 / number_of_stocks)
        # all permuation sum to 1
        b_w = [i for i in all_perm if 0.999 <= np.sum(i) <= 1.001]
        b_vec=np.zeros((len(stock_data), number_of_stocks))
        b_vec[0]=b_vec_inittial

        s_vec=np.zeros(len(stock_data))
        # s_vec init with s_0=1
        s_vec[0]=1
        s_vec[1]=np.dot(b_vec_inittial, x_vec[0])
        result=[np.dot(a, x_vec[0]) for a in b_w]
        sum_denominator=np.sum(result)
        sum2=[a * j for a,j in zip(b_w, result)]
        sum_numerator=np.sum(sum2,axis=0)
        b_vec[1]= sum_numerator / sum_denominator

        # This for loop calculate the wealth S_vector, x vector * b vector calculation from day 2
        for day in range(2, len(stock_data)):
                s_vec[day]=np.dot(s_vec[day - 1], np.dot(b_vec[day - 1], x_vec[day - 1]))
                s_lis=[]
                result=[]
                for i in b_w:
                    s_list=[]
                    for j in range(0,day):
                        s_list.append(np.dot(x_vec[j], i))
                    s_lis.append(np.prod(s_list))
                    u_sum= i * np.prod(s_list)
                    result.append(u_sum)

                sum_denominator=np.sum(s_lis)
                sum_numerator=np.sum(result, axis=0)
                b_vec[day]= sum_numerator / sum_denominator
        return s_vec




    def find_exponential_gradient_portfolio(self, learn_rate: float = 0.5) -> List[float]:
        """
        calculates the exponential gradient portfolio for the previously requested stocks

        :param float learn_rate: the learning rate of the algorithm, defaults to 0.5
        :return: returns a list of floats, representing the growth trading  per day
        """

        stock_data = self.stock_data['Adj Close']
        number_of_stocks = len(self.tickers_list)

        # s_vec init
        s_vec = []
        s_0=1.0
        s_vec.append(s_0)

        # x_vec init
        x_vec = []
        for i in range(len(stock_data)-1):
            x_vec.append(list(stock_data.iloc[i+1] / stock_data.iloc[i]))

        # b_vec init
        b_vec = []
        b_vec.append([ 1 / number_of_stocks for i in range(number_of_stocks)])

        for i in range(len(stock_data)-1):

            result = []

            for j in range(number_of_stocks):
                numerator = learn_rate * x_vec[i][j]
                denominator = sum([a*b for a,b in zip(x_vec[i],b_vec[i])])
                a_b_exp =  b_vec[i][j] * math.exp(numerator/denominator)
                result.append(a_b_exp)

            item = []
            for k in range(len(result)):
                item.append(result[k] / sum(result))

            b_vec.append(item)

        # s_vec
        for i in range(len(stock_data)-1):
            # x vector * b vector calculation
            b_multi_x = list(map(lambda x,z: x*z ,x_vec[i],b_vec[i]))
            s_vec.append(sum(list(map( lambda x: s_vec[i]*x ,b_multi_x))))


        return s_vec





if __name__ == '__main__':  # You should keep this line for our auto-grading code.
    pb=PortfolioBuilder()
    tickers = ['GOOG','AAPL','MSFT']
    start_date = date(2020, 1, 1)
    end_date = date(2020, 2, 1)
    stock_data = pb.get_daily_data(tickers,start_date,end_date)
    print('********************************************')
    print('stock_data length: ' + str(len(stock_data)))
    print(stock_data)
    print('\n')
    universal_portfolio=pb.find_universal_portfolio()
    print(universal_portfolio)
    #print('universal_portfolio length: '+str(len(universal_portfolio)))
    #exponential_gradient = pb.find_exponential_gradient_portfolio()
    #print(exponential_gradient)
    #print('exponential_gradient length: '+str(len(exponential_gradient)))


