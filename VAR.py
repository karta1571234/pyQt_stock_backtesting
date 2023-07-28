# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 01:02:57 2022

@author: karta
"""

import pandas as pd

from KPI import get_KPI
from func import get_MA

def trade(df):
    df["Buy"] = None
    df["Sell"] = None
  
    last_index = df.index[-1]
    hold = 0 # 是否持有
    #foreach每個row
    for index, row in df.copy().iterrows():
        # 最後一天不交易，並將部位平倉
        if index == last_index: 
            if hold == 1: # 若持有部位，平倉
                  df.at[index, "Sell"] = row["收盤價"] # 紀錄賣價
                  hold = 0
            break # 跳出迴圈
        #買進條件
        #買進條件1 今日VAR5<15 且 今日VAR5>前一日VAR5
        #買進條件2 今日VAR10<50 且 今日VAR10>前一日VAR10
        #買進條件3 今日收盤價>20均
        buy_condition_1=(row["VAR_5"]<15) and (row["VAR_5"]>row["VAR_5_T1"])
        buy_condition_2=(row["VAR_10"]<50) and (row["VAR_10"]>row["VAR_10_T1"])
        buy_condition_2=row["收盤價"]>row["SMA_20"]
        
        #賣出條件
        #賣出條件1 今日VAR5<前一日VAR5 且 今日VAR10<前一日VAR10 且 今日收盤價<今日SAR
        #或
        #賣出條件2 今日VAR5>前一日VAR5 且 今日VAR10>前一日VAR10 且 今日收盤價<20均
        sell_condition_1=((row["VAR_5"]<row["VAR_5_T1"]) and (row["VAR_10"]<row["VAR_10_T1"]) and row["收盤價"]<row["SAR"])
        sell_condition_2=((row["VAR_5"]>row["VAR_5_T1"]) and (row["VAR_10"]>row["VAR_10_T1"]) and row["收盤價"]<row["SMA_20"])
        
        #符合兩個買進條件，沒有持股就買入
        if(buy_condition_1 and buy_condition_2) and hold==0:
            df.at[index, "Buy"]=row["收盤價"]  #記錄買價
            hold=1 #持股
        #符合兩個賣出條件，有持股就賣出
        elif(sell_condition_1 or sell_condition_2) and hold==1:
            df.at[index, "Sell"]=row["收盤價"]  #記錄賣價
            hold=0 #持股
    return df


def main(stock_id=3711, period="12mo"):
    df=get_MA(stock_id, period) #取得資料
    df=trade(df)    #交易
    KPI_df=get_KPI(df)
    
    return df, KPI_df
    print(df)

if __name__ == "__main__":
    main()