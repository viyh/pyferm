import logging
from pyferm import pyferm

logging.basicConfig(
    format="%(asctime)s  %(levelname)-10s %(message)s", level=logging.DEBUG
)

p = pyferm()
p.start()
