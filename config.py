from flask import g
import configparser


# To generate a new secret key:
# >>> import random, string
# >>> "".join([random.choice(string.printable) for _ in range(24)])
# SECRET_KEY = "#d#JCqTTW\nilK\\7m\x0bp#\tj~#H"
# SECRET_KEY = '7540d096a1af7602423becbadf2f2df8'
FB_APP_ID = 1200420960103822
app.config['SECRET_KEY'] = '7540d096a1af7602423becbadf2f2df8'

def get_config():
    if 'config' not in g:
        g.config = configparser.ConfigParser()
        g.config.read('app.config')

        return g.config