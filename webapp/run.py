import tornado.ioloop 
import tornado.web
import signal, os
import pandas as pd
import numpy as np
from nbastats import rendering, utility
from nbastats.salaries_analysis import salaries_stats_analysis_test
from nbastats.salaries_analysis import salaries_preprocessing

# define some constants
YEARS = xrange(2000, 2015)
TEMPLATE_DIR = 'templates'
FILE_DIR = os.path.dirname(os.path.realpath(__file__))

class OverviewHandler(tornado.web.RequestHandler):
    """ Request Handler for /overview/year """
    def get(self, year=2014):
        try:
            filename = FILE_DIR + '/nbastats/static/data/stats_{}.csv'.format(year)
            stats = pd.read_csv(filename)
        except IOError:
            print 'data not found'
            raise tornado.web.HTTPError(500)

        self.write(rendering.render_leaders(stats, 'all', 12, year, TEMPLATE_DIR, 'overview.html'))

class PositionHandler(tornado.web.RequestHandler):
    """ Request handler for /overview/year/position """
    def get(self, year, position):
        try:
            filename = FILE_DIR + '/nbastats/static/data/stats_{}.csv'.format(year)
            stats = pd.read_csv(filename)
        except IOError:
            print filename
            print 'data not found'
            raise tornado.web.HTTPError(500)
        pos = position.upper()
        self.write(rendering.render_leaders(stats[stats.POS==pos], position, 8, year, TEMPLATE_DIR, 'overview.html'))

class PlayersListHandler(tornado.web.RequestHandler):
    """ Request handler for /players/[current, historic] """
    def get(self, option, position):
        try:
            players = pd.read_csv(FILE_DIR + '/nbastats/static/data/players_{}.csv'.format(option))
        except IOError:
            raise tornado.web.HTTPError(500)
        
        self.write(rendering.render_players(players, position, option, TEMPLATE_DIR, 'players_index.html'))
        
class PlayersOverviewHandler(tornado.web.RequestHandler):
    """ Request handler for /players/league_info """
    def get(self):
        position_counts = {}
        for year in YEARS:
            try:
                stats = pd.read_csv(FILE_DIR + '/nbastats/static/data/stats_{}.csv'.format(year))
            except IOError as e:
                continue
            position_counts[year] = utility.count_position(stats)
        self.write(rendering.render_league_info(position_counts, TEMPLATE_DIR, 'league_info.html'))

class PlayerHandler(tornado.web.RequestHandler):
    """ Request handler for player individual pages """
    def get(self, option, name):
        stats = pd.read_csv(FILE_DIR + '/nbastats/static/data/players_{}.csv'.format(option), index_col='PLAYER')
        player = utility.url_to_name(name)
        img_src = stats.ix[player]['IMG']
        if not img_src:
            img_src = None
        years = stats.ix[player]['YEARS'].strip().split()
        last_year = years[-1]
        stats = pd.read_csv(FILE_DIR + '/nbastats/static/data/stats_{}.csv'.format(last_year), index_col='PLAYER')
        self.write(rendering.render_player(player, stats, years, last_year, option, img_src, TEMPLATE_DIR, 'player.html'))

class PlayerByYearHandler(tornado.web.RequestHandler):
    """ """
    def get(self, option, name, year):
        stats = pd.read_csv(FILE_DIR + '/nbastats/static/data/players_{}.csv'.format(option), index_col='PLAYER')
        player = utility.url_to_name(name)
        img_src = stats.ix[player]['IMG']
        years = stats.ix[player]['YEARS'].strip().split()
        stats = pd.read_csv(FILE_DIR + '/nbastats/static/data/stats_{}.csv'.format(year), index_col='PLAYER')
        self.write(rendering.render_player(player, stats, years, year, option, img_src, TEMPLATE_DIR, 'player.html'))

class TrendHandler(tornado.web.RequestHandler):
    def get(self):
        oa = salaries_stats_analysis_test.overall_analysis()
        pos = salaries_stats_analysis_test.position_analysis()
        self.write(rendering.render_trend(oa, pos, TEMPLATE_DIR, 'salaries_trend.html'))

class DistributionHandler(tornado.web.RequestHandler):
    def get(self, year):
        oa = salaries_stats_analysis_test.overall_analysis(int(year))
        pos = salaries_stats_analysis_test.position_analysis(int(year))   
        self.write(rendering.render_distribution(oa, pos, TEMPLATE_DIR, 'salaries_distribution.html'))
        
class Top10Handler(tornado.web.RequestHandler):
    def get(self, year):
        oa = salaries_stats_analysis_test.overall_analysis(int(year))
        positions = ['C','PF','PG','SF','SG']
        pos = []
        for position in positions:
            pos.append(salaries_stats_analysis_test.position_analysis(int(year), position))
        self.write(rendering.render_top10(oa, pos, TEMPLATE_DIR, 'salaries_top10.html'))
        
class RegressionHandler(tornado.web.RequestHandler):
    def get(self,year):
        sr = salaries_regression(year)
        self.write(rendering.render_regression(sr, TEMPLATE_DIR, 'salaries_regression.html'))
        
        
def make_app():
    settings = {"debug": True,
                "static_path": os.path.join(os.path.dirname(__file__), "nbastats/static"),}

    return tornado.web.Application([
        (r'/static/(.*)', tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
        (r'/overview/(20[01][0-9])', OverviewHandler),
        (r'/overview/(20[01][0-9])/(c|pf|sf|sg|pg)', PositionHandler),
        (r'/players/(current|historic)/(c|pf|sf|sg|pg)', PlayersListHandler),
        (r'/overview', tornado.web.RedirectHandler, {'url': '/overview/2014'}),
        (r'/players/current', tornado.web.RedirectHandler, {'url': '/players/current/c'}),
        (r'/players/historic', tornado.web.RedirectHandler, {'url': '/players/historic/c'}),
        (r'/players/info', PlayersOverviewHandler),
        (r'/players/(current|historic)/(.*)/(20[01][0-9])', PlayerByYearHandler),
        (r'/players/(current|historic)/(.*)', PlayerHandler),
        (r'/salaries/trend', TrendHandler),
        (r'/salaries/dist/(20[01][0-9])', DistributionHandler),
        (r'/salaries/top/(20[01][0-9])', Top10Handler),
        (r'/salaries/reg/(20[01][0-9])', RegressionHandler),
    ], **settings)

def on_shutdown():
    print 'Shutting down'
    tornado.ioloop.IOLoop.instance().stop()

def main():
    app = make_app()
    app.listen(8080)
    ioloop = tornado.ioloop.IOLoop.instance()
    signal.signal(signal.SIGINT, lambda sig, frame: ioloop.add_callback_from_signal(on_shutdown))
    ioloop.start()

if __name__ == '__main__':
    main()
