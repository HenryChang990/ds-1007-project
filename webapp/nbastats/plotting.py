'''
Authored by Yijun Xiao, Henry Chang

'''

import numpy as np
import matplotlib.pyplot as plt
import mpld3
import os

def hist_plot(data):
    """ plot histogram from data and return html raw code """
    fig = plt.figure(figsize=(10,6))
    ax = fig.add_subplot(111, axisbg='#EEEEEE')
    ax.grid(color='white', linestyle='solid')
    ax.hist(data, 30, histtype='stepfilled', fc='#0077FF', alpha=0.5)
    html = mpld3.fig_to_html(fig)
    plt.close()
    return html

def pie_plot(data):
    """ plot pie chart and return html code """
    fig = plt.figure(figsize=(4.5, 4.5))
    ax = fig.add_subplot(111, axisbg='#FFFFFF')
    labels = 'C', 'PF', 'SF', 'SG', 'PG'
    colors = ['skyblue', 'yellowgreen', 'lightcoral', 'mediumpurple', 'gold']
    explode = (data==max(data)) * 0.1
    ax.pie(data, labels=labels, colors = colors, startangle=90, autopct='%1.1f%%', explode=explode)
    plt.tight_layout()
    html = mpld3.fig_to_html(fig)
    plt.close()
    return html

def trend_plot(data):
    """ plot number of players in each position by season """
    years = sorted(data.keys())
    counts = np.array([x[1] for x in sorted(data.items(), key=lambda x:x[0])])
    labels = 'C', 'PF', 'SF', 'SG', 'PG'
    colors = ['skyblue', 'yellowgreen', 'lightcoral', 'mediumpurple', 'gold']
    fig = plt.figure(figsize=(6.5, 4.5))
    ax = fig.add_subplot(111, axisbg='#EEEEEE')
    ax.grid(color='white', linestyle='solid')
    for i in xrange(5):
        ax.plot(years, counts[:, i], label=labels[i], color=colors[i], linewidth=2.0)
    ax.legend(loc=4)
    plt.tight_layout()
    html = mpld3.fig_to_html(fig)
    plt.close()
    return html
    
def radar_plot(data, fig_name, pos):
    """ plot radar chart for specified player based on 6 predefined stats """

    fig = plt.figure(figsize=(3, 3))
    titles = ['AST', 'PTS', 'FG%', 'BLK', 'REB', 'STL']
    n = 6

    # Set angles
    angles = np.arange(30, 30+360, 360.0/n)
    rect = [0.1, 0.1, 0.9, 0.9]

    axes = [fig.add_axes(rect, projection="polar")]
    ax = axes[0]
    ax.set_thetagrids(angles, labels=titles, fontsize=10)
    for ax in axes[0:]:
        ax.patch.set_visible(False)
        ax.grid("on")
        ax.xaxis.set_visible(True)
    for ax, angle in zip(axes, angles):
        ax.set_rgrids(range(1, 6), angle=angle)
        ax.spines["polar"].set_visible(True)
        ax.set_ylim(0, 1)
        
    stats = np.append(data, data[0])
    angles = np.append(angles, angles[0])
    angles = np.deg2rad(angles)
    colorbook = dict(C='skyblue', PF='yellowgreen', SF='lightcoral', SG='mediumpurple', PG='gold')
    color = colorbook[pos]
    ax.plot(angles, stats, "-", lw=4, color=color, alpha=0.55, label="name")
    ax.fill(angles, stats, facecolor=color, alpha=0.25)
    fig_path = os.path.join(os.path.dirname(__file__), "static/img/{}".format(fig_name))
    plt.savefig(fig_path, bbox_inches='tight')
    plt.close()
