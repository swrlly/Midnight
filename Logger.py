import os
import logging, logging.handlers
from datetime import datetime, timezone

#fmt = "%(asctime)s %(levelname)-6s - %(funcName)-8s - %(filename)s - %(name)s - %(message)s"
fmt = "%(asctime)s %(levelname)-6s - %(name)s - %(message)s"
dtfmt = "[%Y-%m-%d] %H:%M:%S - "

directory = "logs"

def CreateLogger(directory):

    if not os.path.exists(directory):
        os.makedirs(directory)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    fileName = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d") + ".txt"
    fileName = os.path.join(directory, fileName)
    h = logging.handlers.RotatingFileHandler(filename = fileName, maxBytes = 4096 ** 2, backupCount = 5)
    h.setLevel(logging.INFO)
    h.setFormatter(logging.Formatter(fmt, dtfmt))
    logger.addHandler(h)

    s = logging.StreamHandler()
    s.setLevel(logging.INFO)
    s.setFormatter(logging.Formatter(fmt, dtfmt))
    logger.addHandler(s)