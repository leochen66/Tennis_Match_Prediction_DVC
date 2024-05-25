import logging
import watchtower

FORMAT = '%(asctime)s %(filename)s %(levelname)s:%(message)s'

logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)
logger.addHandler(watchtower.CloudWatchLogHandler())