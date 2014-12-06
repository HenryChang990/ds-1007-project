import matplotlib.pyplot as plt
import mpld3

def hist_plot(data, title):
    """ plot histogram from data with title """
    fig = plt.figure()
    ax = fig.add_subplot(111, axisbg='#EEEEEE')
    ax.grid(color='white', linestyle='solid')
    ax.hist(data, 30, histtype='stepfilled', fc='lightblue', alpha=0.5)
    plt.title(title)
    html = mpld3.fig_to_html(fig)
    plt.close()
    return html
