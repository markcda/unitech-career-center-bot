import sys

# Отредактируйте путь до папки с ботом.
path = '/home/<username>/unitech-career-center-bot/'
if path not in sys.path:
  sys.path.append(path)

import bot
bot.main()


def application(environ, start_response):
  status = '404 NOT FOUND'
  content = 'Page not found.'
  response_headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(content)))]
  start_response(status, response_headers)
  yield content.encode('utf8')
