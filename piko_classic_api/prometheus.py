import enum
import inspect
import itertools
from collections.abc import Sequence

from prometheus_client import Enum, Gauge

from piko_classic_api import livedata
from piko_classic_api.values import PikoValue, ALL_VALUES, ac_energy_day

name_label = 'name'
phase_label = 'phase'


def create_metric(value: PikoValue):
    label_names = [name_label]
    if value.phase is not None:
        label_names.append(phase_label)
    if value.parse is not None and inspect.isclass(value.parse) and issubclass(value.parse, enum.Enum):
        return Enum(value.name, value.name, label_names, states=[p.name for p in value.parse])
    else:
        return Gauge(value.name, value.name, label_names)


class PikoClassicMetrics:

    def __init__(self, hostname: str, values: Sequence[PikoValue] = None):
        self.values = values or [v for v in ALL_VALUES if v != ac_energy_day]
        self.hostname = hostname
        self.metrics = {}
        for value in self.values:
            if value.name in self.metrics:
                continue
            self.metrics[value.name] = create_metric(value)

    def poll(self):
        results = livedata.get_live_data(self.hostname, self.values)
        for piko_value, result in results.items():
            metric = self.metrics[piko_value.name]
            labels = [self.hostname]
            if piko_value.phase is not None:
                labels.append(piko_value.phase)
            if isinstance(metric, Gauge):
                metric.labels(*labels).set(result)
            else:
                metric.labels(*labels).state(result.name)
