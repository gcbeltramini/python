import logging
import sys
from tqdm import tqdm
from time import sleep


# Based on:
# https://github.com/tqdm/tqdm/issues/193
# https://github.com/tqdm/tqdm/issues/313
# https://docs.python.org/2/howto/logging-cookbook.html


class TqdmHandler(logging.StreamHandler):
    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)

    def emit(self, record):
        try:
            msg = self.format(record)
            tqdm.write(msg, file=self.stream)
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

# create logger
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)
logger2 = logging.getLogger('my-second-logger')
logger2.setLevel(level=logging.DEBUG)

# create custom handler
handler = TqdmHandler(stream=sys.stdout)
# Only when TqdmHandler(stream=sys.stderr) and tqdm(file=sys.stdout), the
# progress bar is shown multiple times. It works in all other cases.
handler.setLevel(level=logging.DEBUG)
handler2 = logging.StreamHandler(stream=sys.stderr)
handler2.setLevel(level=logging.DEBUG)

# create formatter and add it to the handler
fmt = ('[%(asctime)s] %(levelname)-8s : %(processName)s : %(pathname)s : '
       '%(filename)s : %(name)s : %(funcName)s : %(module)s : '
       '%(message)s (%(relativeCreated)d ms elapsed)')
formatter = logging.Formatter(fmt=fmt,
                              datefmt="%Y-%m-%dT%H:%M:%S%z")
handler.setFormatter(fmt=formatter)
handler2.setFormatter(fmt=logging.Formatter(fmt=logging.BASIC_FORMAT))

# add the handler to the logger
logger.addHandler(handler)
logger2.addHandler(handler2)

# Default handler
# logging.basicConfig(stream=sys.stderr, level=logging.DEBUG,
#                     datefmt="%Y-%m-%dT%H:%M:%S%z")
# default options:
# stream=sys.stderr, level=logging.WARNING, format=logging.BASIC_FORMAT
# logging.BASIC_FORMAT = "%(levelname)s:%(name)s:%(message)s'"
# datefmt: ISO8601

# Test log messages
logger.critical('my critical message')
logger.error('my error message')
logger.warning('my warning message')
logger.info('my info message')
logger.debug('my debug message')

logger2.debug('my debug message in the second logger')

# Test progress bar
total_size = 5
for i in tqdm(iterable=range(total_size),
              file=sys.stdout,
              ncols=80,
              unit='it',
              leave=True,
              total=total_size,
              ):
    sleep(.8)
    logger.info('message inside the loop')
    if i == 3:
        print 1 + 'a'  # test error behavior
