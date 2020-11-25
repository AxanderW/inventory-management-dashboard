

import pandas as pd
import numpy as np
import os
import pathlib


# Load data

APP_PATH = pathlib.Path(__file__).parent
DATA_PATH = APP_PATH.joinpath("../data").resolve()

df_full_data = pd.read_csv(DATA_PATH.joinpath("full_data.csv"),parse_dates=True)
df_lat_lon = pd.read_csv(DATA_PATH.joinpath("statelatlong.csv"),parse_dates=True)

# Create variables 

YEARS_INVENTORY = df_full_data['Order Year'].unique().tolist()

ALL_BRANDS = df_full_data['Brand'].unique().tolist()
ALL_BRANDS = sorted(ALL_BRANDS)

INVENTORY_TABLE_COLUMNS = ['Order Year','Buyer Region','Brand','Sneaker Name','Shoe Size','Current Inventory']

ALL_OPTIONS = [
                {
                    "label": "Total Sales",
                    "value":"total_sales"
                },
                {
                    "label": "Count of Sales",
                    "value":"count_sales",
                },
                {
                    "label": "Average Sales",
                    "value":"avg_sales",
                },
                {
                    "label": "Current Inventory",
                    "value":"curr_inventory",
                },
                {
                    "label": "Top Performers",
                    "value":"top_performers",
                },
                {
                    "label": "Bottom Performers",
                    "value":"bottom_performers",
                },
                {
                    "label": "Average Net Profit",
                    "value":"avg_net_profit",
                },
                {
                    "label": "Top Net Profit",
                    "value":"top_avg_net_profit",
                },
                {
                    "label": "Bottom Net Profit",
                    "value":"bottom_avg_net_profit",
                },
                {
                    "label": "Average Inventory Turnover",
                    "value":"avg_inventory_turnover"
                },
                {
                    "label": "Top Inventory Turnover",
                    "value":"top_avg_inventory_turnover"
                },
                {
                    "label": "Bottom Inventory Turnover",
                    "value":"bottom_avg_inventory_turnover"
                }
            ]


# Create functions
def create_plot_metric(filters,metric_type="total_sales"):
    
    if metric_type == "total_sales":
        return get_total_sales(filters)
    
    if metric_type == "count_sales" :
        return get_count_sales(filters)
    
    if metric_type == "avg_sales":
        return get_avg_sales(filters)
    
    if metric_type == "curr_inventory":
        return get_curr_inventory(filters)
                                  
    if metric_type == "top_performers":
        return get_top_performers(filters)
    
    if metric_type == "bottom_performers":
        return get_bottom_performers(filters)
    
    if metric_type == "avg_net_profit":
        return get_avg_net_profit(filters)
    
    if metric_type == "top_avg_net_profit":
        return get_top_avg_net_profit(filters)
    
    if metric_type == "bottom_avg_net_profit":
        return get_bottom_avg_net_profit(filters)
    
    if metric_type == "avg_inventory_turnover":
        return get_avg_inventory_turnover(filters)
    
    if metric_type == "top_avg_inventory_turnover":
        return get_top_avg_inventory_turnover(filters)
    
    if metric_type == "bottom_avg_inventory_turnover":
        return get_bottom_avg_inventory_turnover(filters)

    if metric_type == "sales_over_time":
        return get_sales_over_time(filters)


def get_total_sales(filters):    
    data =  df_full_data.groupby(filters,as_index=False).agg({'Sale Price':['sum']})
    filters.append('Total Sales')
    data.columns = filters
    data.sort_values(by=['Total Sales'],ascending=[False],inplace=True)
    return data

def get_count_sales(filters):    
    data =  df_full_data.groupby(filters,as_index=False).agg({'Sale Price':['count']})
    filters.append('Sales Count')
    data.columns = filters
    data.sort_values(by=['Sales Count'],ascending=[False],inplace=True)
    return data

def get_avg_sales(filters):    
    data =  df_full_data.groupby(filters,as_index=False).agg({'Sale Price':['mean']})
    filters.append('Avg Sales')
    data.columns = filters
    data.sort_values(by=['Avg Sales'],ascending=[False],inplace=True)
    return data


def get_curr_inventory(filters):    
    data =  df_full_data.groupby(filters,as_index=False).agg({'Product_ID':['count']})
    filters.append('Current Inventory')
    data.columns = filters
    data.sort_values(by=['Current Inventory'],ascending=[True],inplace=True)
    return data

def get_top_performers(filters):    
    data =  df_full_data.groupby(filters,as_index=False).agg({'Sale Price':['sum']})
    filters.append('Total Sales')
    data.columns = filters
    data.sort_values(by=['Total Sales'],ascending=[False],inplace=True)
    return data.head(10)


def get_bottom_performers(filters):    
    data =  df_full_data.groupby(filters,as_index=False).agg({'Sale Price':['sum']})
    filters.append('Total Sales')
    data.columns = filters
    data.sort_values(by=['Total Sales'],ascending=[True],inplace=True)
    return data.head(10)


def get_avg_net_profit(filters):    
    data =  df_full_data.copy()
    data['net_profit'] = data['Sale Price'] - data['Retail Price']
    data = data.groupby(filters,as_index=False).agg({'net_profit':['mean']})
    filters.append('Avg Net Profit')
    data.columns = filters
    data.sort_values(by=['Avg Net Profit'],ascending=[False],inplace=True)
    return data

def get_top_avg_net_profit(filters):    
    data =  df_full_data.copy()
    data['net_profit'] = data['Sale Price'] - data['Retail Price']
    data = data.groupby(filters,as_index=False).agg({'net_profit':['mean']})
    filters.append('Avg Net Profit')
    data.columns = filters
    data.sort_values(by=['Avg Net Profit'],ascending=[False],inplace=True)
    return data.head(10)


def get_bottom_avg_net_profit(filters):    
    data =  df_full_data.copy()
    data['net_profit'] = data['Sale Price'] - data['Retail Price']
    data = data.groupby(filters,as_index=False).agg({'net_profit':['mean']})
    filters.append('Avg Net Profit')
    data.columns = filters
    data.sort_values(by=['Avg Net Profit'],ascending=[True],inplace=True)
    return data.head(10)



def get_avg_inventory_turnover(filters):    
    data =  df_full_data.copy()
    data['Order Date'] = pd.to_datetime(data['Order Date'])
    data['Release Date'] = pd.to_datetime(data['Release Date'])

    data['days_in_inventory'] = (data['Order Date'] - data['Release Date'])/np.timedelta64(1,'D')
    data = data.groupby(filters,as_index=False).agg({'days_in_inventory':['mean']})
    filters.append('Inventory Turnover')
    data.columns = filters
    data.sort_values(by=['Inventory Turnover'],ascending=[True],inplace=True)
    #plot_data = data
    return data

def get_top_avg_inventory_turnover(filters):    
    data =  df_full_data.copy()
    data['Order Date'] = pd.to_datetime(data['Order Date'])
    data['Release Date'] = pd.to_datetime(data['Release Date'])

    data['days_in_inventory'] = (data['Order Date'] - data['Release Date'])/np.timedelta64(1,'D')
    data = data.groupby(filters,as_index=False).agg({'days_in_inventory':['mean']})
    filters.append('Inventory Turnover')
    data.columns = filters
    data.sort_values(by=['Inventory Turnover'],ascending=[True],inplace=True)
    return data.head(10)


def get_bottom_avg_inventory_turnover(filters):    
    data =  df_full_data.copy()
    data['Order Date'] = pd.to_datetime(data['Order Date'])
    data['Release Date'] = pd.to_datetime(data['Release Date'])
    
    data['days_in_inventory'] = (data['Order Date'] - data['Release Date'])/np.timedelta64(1,'D')
    data = data.groupby(filters,as_index=False).agg({'days_in_inventory':['mean']})
    filters.append('Inventory Turnover')
    data.columns = filters
    data.sort_values(by=['Inventory Turnover'],ascending=[False],inplace=True)
    return data.head(10)

def get_sales_over_time(filters):
    data = df_full_data[filters].copy()   
    return data