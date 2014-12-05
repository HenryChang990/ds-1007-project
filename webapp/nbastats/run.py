import tornado.ioloop 
import tornado.web
import signal, os
from jinja2 import Environment, FileSystemLoader
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mpld3

YEARS = xrange(2000, 2015)
TEMPLATE_DIR = 'templates'
POSITIONS = {'c':'Center', 'pf':'Power Forward', 'sf':'Small Forward', 'sg':'Shooting Guard', 'pg':'Point Guard', 'all':'All Players'}
STATS = ['PPG', 'RPG', 'APG', 'SPG', 'BPG']

def hist_plot(data, title):
    """ plot histogram from data with title """
    fig = plt.figure()
    ax = fig.add_subplot(111, axisbg='#EEEEEE')
    ax.grid(color='white', linestyle='solid')
    ax.hist(data, 30, histtype='stepfilled', fc='lightblue', alpha=0.5)
    plt.title(title)
    return mpld3.fig_to_html(fig)

def render_leaders(stats, n_top, year, temp_dir, temp_file, position):
    """ take in a dataframe, return rendered templates with data of top player stats in PTS, REB, AST, STL, and BLK """
    leader_stats = []
    plots = []
    for stat in STATS:
        leader_stats.append(stats.sort(stat, ascending=False)[:n_top].to_dict(orient='record'))
        plots.append(hist_plot(np.array(stats[stat]), '{} Distribution in the League'.format(stat)))
    env = Environment(loader=FileSystemLoader(temp_dir))
    template = env.get_template(temp_file)
    
    return template.render(data=leader_stats, years=YEARS, year=year, season='{}-{}'.format(int(year)-1, year), position=POSITIONS[position], plots=plots)
    
class OverviewHandler(tornado.web.RequestHandler):
    """ Request Handler for /overview/year """
    def get(self, year=2014):
        try:
            stats = pd.read_csv('data/stats_{}.csv'.format(year))
        except IOError:
            raise tornado.web.HTTPError(404)
        self.write(render_leaders(stats, 12, year, TEMPLATE_DIR, 'overview.html', 'all'))

class PositionHandler(tornado.web.RequestHandler):
    """ Request handler for /overview/year/position """
    def get(self, year, position):
        try:
            stats = pd.read_csv('data/stats_{}.csv'.format(year))
        except IOError:
            raise tornado.web.HTTPError(404)
        pos = position.upper()
        self.write(render_leaders(stats[stats.POS==pos], 8, year, TEMPLATE_DIR, 'overview.html', position))
        
def make_app():
    settings = {"debug": True,
                "static_path": os.path.join(os.path.dirname(__file__), "static"),}
    return tornado.web.Application([
        (r'/static/(.*)', tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
        (r'/overview/(20[01][0-9])', OverviewHandler),
        (r'/overview/(20[01][0-9])/(c|pf|sf|sg|pg)', PositionHandler),
        (r'/.*', tornado.web.RedirectHandler, {'url': '/overview/2014'}),
    ], **settings)

def on_shutdown():
    print 'Shutting down'
    tornado.ioloop.IOLoop.instance().stop()

def main():
    app = make_app()
    app.listen(8888)
    ioloop = tornado.ioloop.IOLoop.instance()
    signal.signal(signal.SIGINT, lambda sig, frame: ioloop.add_callback_from_signal(on_shutdown))
    ioloop.start()

if __name__ == '__main__':
    main()
