import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import warnings
# Ignore all warnings
warnings.filterwarnings("ignore", category=FutureWarning)

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()

# Get Tesla Stock Data
tesla = yf.Ticker("TSLA")
tesla_data = tesla.history(period="max")
tesla_data.reset_index(inplace=True)
tesla_data.head()

# Get Tesla Revenue Data
tesla_url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
#tesla_html_data = requests.get(tesla_url).text
#tesla_soup = BeautifulSoup(tesla_html_data, 'html5lib')

tesla_pd_html_data = pd.read_html(tesla_url)
tesla_revenue = tesla_pd_html_data[1]
tesla_revenue.rename(columns={'Tesla Quarterly Revenue (Millions of US $)': 'Date', 'Tesla Quarterly Revenue (Millions of US $).1': 'Revenue'}, inplace=True)
tesla_revenue['Revenue'] = tesla_revenue['Revenue'].str.replace('$',"")
tesla_revenue['Revenue'] = tesla_revenue['Revenue'].str.replace(',',"")
tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]
tesla_revenue.tail()

# Get gamestop Stock Data
gamestop = yf.Ticker("GME")
gme_data = gamestop.history(period="max")
gme_data.reset_index(inplace=True)
gme_data.head()

# Get gamestop revenue data
gme_url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
#gme_html_data = requests.get(gme_url).text
#gme_soup = BeautifulSoup(gme_html_data, 'html5lib')

gme_pd_html_data = pd.read_html(gme_url)
gme_revenue = gme_pd_html_data[1]
gme_revenue.rename(columns={'GameStop Quarterly Revenue (Millions of US $)': 'Date', 'GameStop Quarterly Revenue (Millions of US $).1': 'Revenue'}, inplace=True)
gme_revenue['Revenue'] = gme_revenue['Revenue'].str.replace('$',"")
gme_revenue['Revenue'] = gme_revenue['Revenue'].str.replace(',',"")
gme_revenue.dropna(inplace=True)
gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]
gme_revenue.tail()

# Plot tesla
make_graph(tesla_data, tesla_revenue, 'Tesla')
# Plot gamestop
make_graph(gme_data, gme_revenue, 'GameStop')
