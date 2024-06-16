###First Do in jupyter notebook

import yfinance as yf
import joblib
import numpy as np
import pandas as pd
from sklearn.pipeline import make_pipeline
import pandas_ta as ta


def appTechnicalIndicatorBased(ticker_name):
    df = yf.download(ticker_name, interval='5m', period='1mo')
    df=df[df.High!=df.Low]
    df.reset_index(inplace=True)
    
    df.ta.bbands(append=True, length=30, std=2)
    df.ta.rsi(append=True, length=14)
    df["atr"] = ta.atr(low = df.Low, close = df.Close, high = df.High, length=14)

    # Rename columns for clarity if necessary
    df.rename(columns={
        'BBL_30_2.0': 'bbl', 'BBM_30_2.0': 'bbm', 'BBU_30_2.0': 'bbh', 'RSI_14': 'rsi'
    }, inplace=True)

    # Calculate Bollinger Bands Width
    df['bb_width'] = (df['bbh'] - df['bbl']) / df['bbm']
    df = apply_total_signal(df=df, rsi_threshold_low=30, rsi_threshold_high=70, bb_width_threshold=0.001)
    temp = df.tail(1)
    return np.array(temp['TotalSignal'])[0]


def apply_total_signal(df, rsi_threshold_low=30, rsi_threshold_high=70, bb_width_threshold = 0.0015):
    # Initialize the 'TotalSignal' column
    df['TotalSignal'] = 0
    for i in range(1, len(df)):
        # Previous candle conditions
        prev_candle_closes_below_bb = df['Close'].iloc[i-1] < df['bbl'].iloc[i-1]
        prev_rsi_below_thr = df['rsi'].iloc[i-1] < rsi_threshold_low
        # Current candle conditions
        closes_above_prev_high = df['Close'].iloc[i] > df['High'].iloc[i-1]
        bb_width_greater_threshold = df['bb_width'].iloc[i] > bb_width_threshold

        # Combine conditions
        if (prev_candle_closes_below_bb and
            prev_rsi_below_thr and
            closes_above_prev_high and
            bb_width_greater_threshold):
            df.at[i, 'TotalSignal'] = 2  # Set the buy signal for the current candle

        # Previous candle conditions
        prev_candle_closes_above_bb = df['Close'].iloc[i-1] > df['bbh'].iloc[i-1]
        prev_rsi_above_thr = df['rsi'].iloc[i-1] > rsi_threshold_high
        # Current candle conditions
        closes_below_prev_low = df['Close'].iloc[i] < df['Low'].iloc[i-1]
        bb_width_greater_threshold = df['bb_width'].iloc[i] > bb_width_threshold

        # Combine conditions
        if (prev_candle_closes_above_bb and
            prev_rsi_above_thr and
            closes_below_prev_low and
            bb_width_greater_threshold):
            df.at[i, 'TotalSignal'] = 1  # Set the sell signal for the current candle
    return df


def appMLbased(ticker_name):
    df = yf.download(ticker_name, interval='5m', period='1mo')
    df=df[df.High!=df.Low]
    df.reset_index(inplace=True)
    data = calculateIndicator(df)
    data.dropna(inplace = True)
    
    scaler = joblib.load(f'Technical Analysis/{ticker_name}/{ticker_name}MinMaxScaler.pkl')
    model = joblib.load(f'Technical Analysis/{ticker_name}/{ticker_name}MLmodel.pkl')
    pipeline = make_pipeline(scaler, model)
    predict = pipeline.predict(data.tail(1))
    
    return predict[0]

def calculateIndicator(stock):
    stock['EMA_50']=ta.ema(stock.Close, length=50)#sma ema
    stock['EMA_20']=ta.ema(stock.Close, length=20)#sma ema
    stock['RSI']=ta.rsi(stock.Close, length=14)
    my_bbands = ta.bbands(stock.Close, length=20, std=2)
    stock=stock.join(my_bbands)
    temp = ta.macd(stock.Close)
    stock=stock.join(temp)
    stock.drop(columns = ['MACD_12_26_9','MACDs_12_26_9','BBP_20_2.0','BBB_20_2.0','BBM_20_2.0'],inplace = True)
    temp = ta.cci(stock.High,stock.Low,stock.Close)
    stock=stock.join(temp)
    temp = ta.stoch(stock.High,stock.Low,stock.Close,k=10)
    stock=stock.join(temp)
    stock.drop(columns = ['STOCHd_10_3_3'],inplace = True)
    temp = ta.supertrend(stock.High,stock.Low,stock.Close)
    stock=stock.join(temp)
    stock.drop(columns = ['SUPERTl_7_3.0','SUPERTs_7_3.0'],inplace = True)
    temp = ta.donchian(stock.High,stock.Low)
    stock=stock.join(temp)
    stock.drop(columns = ['DCM_20_20'],inplace = True)
    temp = ta.adx(stock.High,stock.Low,stock.Close)
    stock=stock.join(temp)
    stock.drop(columns = ['DMP_14','DMN_14'],inplace = True)
    temp = ta.slope(stock.EMA_50)
    stock=stock.join(temp)
    stock.rename(columns = {'SLOPE_1' : 'EMA_50_slope'},inplace = True)
    temp = ta.slope(stock.EMA_20)
    stock=stock.join(temp)
    stock.rename(columns = {'SLOPE_1' : 'EMA_20_slope'}, inplace = True)
    temp = ta.slope(stock['BBL_20_2.0'])
    stock = stock.join(temp)
    stock.rename(columns = {'SLOPE_1' : 'BBL_20_2.0_slope'}, inplace = True)
    temp = ta.slope(stock['BBU_20_2.0'])
    stock = stock.join(temp)
    stock.rename(columns = {'SLOPE_1' : 'BBU_20_2.0_slope'}, inplace = True)
    temp = ta.slope(stock.DCL_20_20)
    stock=stock.join(temp)
    stock.rename(columns = {'SLOPE_1' : 'DCL_20_20_slope'},inplace = True)
    temp = ta.slope(stock.DCU_20_20)
    stock=stock.join(temp)
    stock.rename(columns = {'SLOPE_1' : 'DCU_20_20_slope'},inplace = True)    
    stock.drop(columns = ['EMA_50','EMA_20','DCL_20_20','DCU_20_20','BBL_20_2.0','BBU_20_2.0'], inplace = True)
    stock.drop(columns = ['Open','High','Low','Volume','Close','SUPERT_7_3.0','Adj Close','Datetime'],inplace = True)
    return stock