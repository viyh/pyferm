import datetime
import logging
import math
import sys
import time

from pyferm import threader

logger = logging.getLogger(__name__ + '.sensors')


class sensor(threader):
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        logger.info("init")
        self.interval = 7
        if not hasattr(self, "metrics"):
            self.metrics = []
        self.start()

    def run(self):
        while self._is_running:
            self.get_metrics()
            for m in self.metrics:
                if datetime.datetime.utcnow() - m.last_updated < datetime.timedelta(
                    seconds=self.interval
                ):
                    logger.debug(f"{m.name:20s} {m.get_formatted_value()}")
            time.sleep(self.interval)

    def get_metric_by_name(self, name):
        return next((m for m in self.metrics if m.name == name), None)


class metric_type:
    def __init__(self):
        pass


class metric_unit:
    def __init__(self):
        pass


class temperature(metric_type):
    def __init__(self):
        self.units = [
            {"name": "Fahrenheit", "format": ".2f", "symbol": "°F"},
            {"name": "Celsius", "format": ".2f", "symbol": "°C"},
        ]

    def f_to_c(self, f):
        return (f - 32) * 5.0 / 9.0

    def c_to_f(self, c):
        return 9.0 / 5.0 * c + 32


class gravity(metric_type):
    def __init__(self):
        self.units = [
            {"name": "Specific Gravity", "format": ".3f", "symbol": "SG"},
            {"name": "Plato", "format": ".2f", "symbol": "°P"},
            {"name": "Brix", "format": ".2f", "symbol": "°Bx"},
        ]

    def brix_to_sg(self, brix):
        return (brix / (258.6 - ((brix / 258.2) * 227.1))) + 1

    def brix_to_plato(self, brix):
        return self.sg_to_plato(self.brix_to_sg(brix))

    def plato_to_sg(self, plato):
        return 1 + (plato / (258.6 - (227.1 * (plato / 258.2))))

    def plato_to_brix(self, plato):
        return self.sg_to_brix(self.plato_to_sg(plato))

    def sg_to_brix(self, sg):
        return ((182.4601 * sg - 775.6821) * sg + 1262.7794) * sg - 669.5622

    def sg_to_plato(self, sg):
        return (
            (135.997 * math.pow(sg, 3))
            - (630.272 * math.pow(sg, 2))
            + (1111.14 * sg)
            - 616.868
        )


class humidity(metric_type):
    def __init__(self):
        self.units = [
            {"name": "Percent", "format": ".2f", "symbol": "%"},
        ]


class ph(metric_type):
    def __init__(self):
        self.units = [
            {"name": "pH", "format": ".2f", "symbol": ""},
        ]


class abv(metric_type):
    def __init__(self):
        self.units = [
            {"name": "Percent", "format": ".2f", "symbol": "%"},
        ]


class count(metric_type):
    def __init__(self):
        self.units = [
            {"name": "Count", "format": "d", "symbol": ""},
        ]


class metric:
    def __init__(self, name, metric_type="count", unit=None):
        self.name = name
        self.metric_type = getattr(sys.modules[__name__], metric_type)()
        self.value = None
        self.last_updated = datetime.datetime.utcnow()
        self.set_unit(unit)

    def set_value(self, value):
        self.value = value
        self.last_updated = datetime.datetime.utcnow()

    def set_unit(self, unit):
        if unit not in self.metric_type.units:
            self.unit = self.metric_type.units[0]
        else:
            self.unit = unit

    def get_value(self):
        return self.value

    def get_formatted_value(self):
        try:
            return f"{self.get_value():{self.unit['format']}} {self.unit['symbol']}"
        except TypeError:
            return f"{self.get_value()} {self.unit['symbol']}"
