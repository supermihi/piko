from collections.abc import Iterable, Mapping, Sequence
from typing import Any

import requests

from piko_classic_api.values import PikoValue, ALL_VALUES


def get_live_data(hostname: str = 'piko', values: Iterable[PikoValue] = None) -> Mapping[PikoValue, Any]:
    """Queries the 'live data' PIKO API that returns current values and is available without login.

    Args:
        hostname (str): hostname or IP address to connect to
        values (Iterable[PikoValue]): subset of values. By default, all known values are queried.
    """
    values = list(values or ALL_VALUES)
    values_by_id: dict[int, PikoValue] = {v.dxsNr: v for v in values}
    response = _fetch(hostname, values)
    result = {}
    for obj in response:
        dxs_id, raw_value = obj['dxsId'], obj['value']
        piko_value = values_by_id[dxs_id]
        value = piko_value.parse(raw_value)
        result[piko_value] = value
    return result


MAX_VALUES_PER_QUERY = 25  # piko only returns first 25 values


def _fetch(hostname: str, values: Sequence[PikoValue]):
    results = []
    while len(values) > 0:
        current_values = values[:MAX_VALUES_PER_QUERY]
        values = values[MAX_VALUES_PER_QUERY:]

        payload = {'dxsEntries': [v.dxsNr for v in current_values]}
        data = requests.get(f'http://{hostname}/api/dxs.json', params=payload).json()['dxsEntries']
        results.extend(data)

    return results
