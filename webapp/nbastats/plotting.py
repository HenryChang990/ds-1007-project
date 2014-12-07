import numpy as np
import matplotlib.pyplot as plt
import mpld3

def hist_plot(data):
    """ plot histogram from data and return html raw code """
    fig = plt.figure()
    ax = fig.add_subplot(111, axisbg='#EEEEEE')
    ax.grid(color='white', linestyle='solid')
    ax.hist(data, 30, histtype='stepfilled', fc='#0077FF', alpha=0.5)
    html = mpld3.fig_to_html(fig)
    plt.close()
    return html

def pie_plot(data):
    """ plot pie chart and return html code """
    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(111, axisbg='#FFFFFF')
    labels = 'C', 'PF', 'SF', 'SG', 'PG'
    colors = ['skyblue', 'yellowgreen', 'lightcoral', 'mediumpurple', 'gold']
    explode = (data==max(data)) * 0.1
    ax.pie(data, labels=labels, colors = colors, startangle=90, autopct='%1.1f%%', explode=explode)
    html = mpld3.fig_to_html(fig)
    plt.close()
    return html

def trend_plot(data):
    """ plot number of players in each position by season """
    years = sorted(data.keys())
    counts = np.array([x[1] for x in sorted(data.items(), key=lambda x:x[0])])
    labels = 'C', 'PF', 'SF', 'SG', 'PG'
    colors = ['skyblue', 'yellowgreen', 'lightcoral', 'mediumpurple', 'gold']
    fig = plt.figure(figsize=(7, 5))
    ax = fig.add_subplot(111, axisbg='#EEEEEE')
    ax.grid(color='white', linestyle='solid')
    for i in xrange(5):
        ax.plot(years, counts[:, i], label=labels[i], color=colors[i], linewidth=2.0)
    ax.legend(loc=4)
    html = mpld3.fig_to_html(fig)
    plt.close()
    return html
    
