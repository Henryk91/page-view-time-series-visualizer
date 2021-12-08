import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
from matplotlib.axis import Axis  
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=['date'])

df.set_index('date', inplace = True)

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():
    # Draw line plot

    fig, ax = plt.subplots()
    df.plot(kind = 'line', color='red', ax=ax)
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019', fontsize=14)
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Page Views', fontsize=14)

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    
    df_bar = df.copy()
    df_bar.reset_index(inplace=True)

    df_bar['year'] = pd.DatetimeIndex(df_bar['date']).year
    df_bar['Month'] = pd.DatetimeIndex(df_bar['date']).month_name()
    df_bar['month_count'] = pd.DatetimeIndex(df_bar['date']).month

    df_bar = df_bar.groupby(['year', 'month_count', 'value']).agg({'value': [("total","count")]})['value'].reset_index()

    # Draw bar plot
    fig, ax = plt.subplots()
    df_bar = pd.pivot_table(df_bar, index = 'year', columns = 'month_count', values = 'value')
    
    df_bar.plot(kind = "bar", ax=ax)
    plt.legend(['January', 'February', 'March', 'April', 'May', 'June', 'July','August', 'September', 'October', 'November', 'December'])
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)

    fig, axes = plt.subplots(1, 2)
    p1 = sns.boxplot(x="year", y="value", data=df_box.copy(), ax=axes[0])

    p1.set_title('Year-wise Box Plot (Trend)', fontsize=14)
    p1.set_xlabel("Year")
    p1.set_ylabel("Page Views")
    col_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul','Aug', 'Sep', 'Oct', 'Nov', 'Dec']
 
    p2 = sns.boxplot(x="month", y="value", data=df_box.copy(), ax=axes[1], order=col_order)
    p2.set_title('Month-wise Box Plot (Seasonality)', fontsize=14)
    p2.set_xlabel("Month")
    p2.set_ylabel("Page Views")

    # plt.show()

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
