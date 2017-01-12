# heartparser.py
#   Author: Kristy Yancey Spencer
#
#   This script parses the Apple Health export xml file for Heart Rate and
#   Blood Pressure data and produces graphs of the data for given date ranges.

import numpy as np
from datetime import date, datetime, timedelta as td
from matplotlib import pyplot, dates as mdates
from matplotlib.ticker import FormatStrFormatter
from openpyxl import load_workbook
from pandas import DataFrame, ExcelWriter, Index
from seaborn import lmplot, regplot
from xml.dom import minidom


def main():
    dates = ["2016-12-11", "2017-01-05"]
    datelist = makedatelist(dates)
    xmldoc = minidom.parse('apple_health_export/export.xml')
    recordlist = xmldoc.getElementsByTagName('Record')
    plotheartrate(dates, datelist, recordlist)
    plotbp(dates, datelist, recordlist)


def plotheartrate(dates, datelist, recordlist):
    # This module parses the heart rate data from the xml file and calls
    # the plotting function.
    category = "HKQuantityTypeIdentifierHeartRate"
    df_hr = parse(category, recordlist)
    df_hr.columns = ['Time', 'Heart Rate (bpm)']
    df_weekhr = weeklyhr(datelist, df_hr)
    for i in range(52):
        maxnum = df_weekhr[df_weekhr['Week'] == i].max()
        print(maxnum)
    makehrplot(dates, df_weekhr)
    
    
def weeklyhr(datelist, df_hr):
    # This module filters through df_hr and returns a dataframe containing
    # weekly heart rate values.
    list_weekhr = []
    dict_weekday = {}
    for di in range(len(datelist)):
        year = int(datelist[di][:4])
        month = int(datelist[di][5:7])
        day = int(datelist[di][8:10])
        weekj = date(year, month, day).isocalendar()[1]
        if weekj not in dict_weekday:
            dict_weekday[weekj] = mdates.date2num(datetime(year, month, day))
        try:
            i = df_hr.index.get_loc(datelist[di])
            di_hr = df_hr.get_value(i, 1, takeable=True)
            list_weekhr.append({
                'Date': mdates.date2num(datetime(year, month, day)),
                'PlotDate': dict_weekday[weekj], 
                'Week': weekj,
                'Heart Rate (bpm)': float(di_hr)
            })
        except:
            pass
    df_weekhr = DataFrame(list_weekhr)
    print(df_weekhr)
    return df_weekhr


def makehrplot(dates, df_week):
    # This module plots the heart rate data between the dates given.
    plotname = 'heartrate_{0}to{1}'.format(dates[0], dates[1])
    fig, ax = pyplot.subplots()
    fig.dpi = 2000
    regplot(x='PlotDate', y='Heart Rate (bpm)', data=df_week,
            x_estimator=np.mean, color='#D42426', ax=ax)
    # assign formatter for the xaxis ticks.
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y.%m.%d'))
    pyplot.savefig(plotname + '.pdf', format='pdf')
    # pyplot.savefig(plotname + '.jpg', format='jpg')
    pyplot.close()


def plotbp(dates, datelist, recordlist):
    # This module parses the blood pressure data from the xml file and
    # calls the plotting function.
    cat1 = "HKQuantityTypeIdentifierBloodPressureSystolic"
    df_bps = parse(cat1, recordlist)
    df_bps.columns = ['Time', 'BP Systolic']
    cat2 = "HKQuantityTypeIdentifierBloodPressureDiastolic"
    df_bpd = parse(cat2, recordlist)
    df_bpd.columns = ['Time', 'BP Diastolic']
    df_bp = df_bps.merge(df_bpd, left_index=True, right_index=True, 
                         how='outer')
    df_bp.drop_duplicates()
    df_bloodpressure = select_bprange(datelist, df_bp)
    makebpplot(dates, df_bloodpressure)


def select_bprange(datelist, df_bp):
    # This module filters df_bp with the given datelist and returns a usable
    # dataframe.
    list_bp = []
    for di in range(len(datelist)):
        year = int(datelist[di][:4])
        month = int(datelist[di][5:7])
        day = int(datelist[di][8:10])
        try:
            i = df_bp.index.get_loc(datelist[di])
            di_bp_sys = df_bp.get_value(i, 1, takeable=True)
            di_bp_dia = df_bp.get_value(i, 3, takeable=True)
            list_bp.append({
                    'Date': mdates.date2num(datetime(year, month, day)),
                    'Blood Pressure': di_bp_sys[0],
                    'Type': 'Systolic'
                })
            list_bp.append({
                    'Date': mdates.date2num(datetime(year, month, day)),
                    'Blood Pressure': di_bp_dia[0],
                    'Type': 'Diastolic'
                })
        except:
            pass
    df_bloodpressure = DataFrame(list_bp)
    print(df_bloodpressure)
    return df_bloodpressure
    
    
def makebpplot(dates, df_bp):
    # This module plots the blood pressure data between the dates given.
    plotname = 'bloodpressure_{0}to{1}'.format(dates[0], dates[1])
    fig, ax = pyplot.subplots()
    fig.dpi = 2000
    kws = dict(linewidth=1, edgecolor="w")
    bpplot = lmplot(x='Date', y='Blood Pressure', data=df_bp, hue='Type',
                    palette='Set1', aspect=1.5, markers=['^', 'v'],
                    legend_out=False, fit_reg=False, scatter_kws=kws)
    ax.legend(loc='upper right', frameon=True)
    # assign formatter for the xaxis ticks.
    axes = bpplot.axes
    axes[0, 0].xaxis.set_major_locator(mdates.AutoDateLocator())
    axes[0, 0].xaxis.set_major_formatter(mdates.DateFormatter('%Y.%m.%d'))
    # put the labels at 45deg since they tend to be too long
    fig.autofmt_xdate()
    pyplot.savefig(plotname + '.pdf', format='pdf')
    # pyplot.savefig(plotname + '.jpg', format='jpg')
    pyplot.close()
    
    
def makedatelist(dates):
    # This module creates a list of days from dates[0] to dates[1].
    startyr, startmn, startdy = int(dates[0][0:4]), int(dates[0][5:7]), int(dates[0][8:10])
    endyr, endmn, enddy = int(dates[1][0:4]), int(dates[1][5:7]), int(dates[1][8:10])
    # Make date list
    d1 = date(startyr, startmn, startdy)
    d2 = date(endyr, endmn, enddy)
    delta = d2 - d1
    datelist = []
    for i in range(delta.days + 1):
        di = d1 + td(days=i)
        datelist.append(di.strftime("%Y-%m-%d"))
    return datelist


def parse(category, recordlist):
    # This module parses the xml file for category's data and
    # returns a Pandas Dataframe
    dates = []
    datalist = []
    for s in recordlist:
        if s.attributes['type'].value == category:
            date = s.attributes['startDate'].value[:10]
            time = s.attributes['startDate'].value[11:16]
            datum = s.attributes['value'].value
            dates.append(date)
            datalist.append([time, int(datum)])
    dfindex = Index(dates, name='Date')
    df = DataFrame(datalist, index=dfindex)
    return df


if __name__ == '__main__':
    main()
