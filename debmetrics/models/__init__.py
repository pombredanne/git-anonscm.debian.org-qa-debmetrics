import logging
from glob import glob1
from os.path import dirname

log = logging.getLogger('debmetrics')

models = {}
for i in (i[:-3] for i in glob1(dirname(__file__), '*.py')):
    if i != '__init__':
        try:
            module = __import__('models.%s' % i,
                                fromlist=[i])
            models[i] = getattr(module, i.title().replace('_', ''))
        except Exception as err:
            if log.level < logging.INFO:
                log.debug("cannot initialize '%s' model", i, exc_info=True)
            else:
                log.debug("cannot initialize '%s' model: %s", i, err)
