import enum
import inspect
from collections.abc import Sequence

from prometheus_client import Enum, Gauge

from piko_classic_api import livedata
from piko_classic_api.values import PikoValue, ALL_VALUES, ac_energy_day

name_label = 'name'


def create_metric(value: PikoValue):
    label_names = [name_label]
    if value.wire_data is not None:
        label_names.append(value.wire_data[0])
    if value.parse is not None and inspect.isclass(value.parse) and issubclass(value.parse, enum.Enum):
        return Enum(value.name, value.description, label_names, states=[p.name for p in value.parse])
    else:
        return Gauge(value.name, value.description, label_names)


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
            if piko_value.wire_data is not None:
                labels.append(piko_value.wire_data[1])
            if isinstance(metric, Gauge):
                metric.labels(*labels).set(result)
            else:
                metric.labels(*labels).state(result.name)
