from collections.abc import Iterable, Mapping
from typing import Any

import requests
from values import PikoValue, ALL_VALUES


def get_live_data(hostname: str = 'piko', values: Iterable[PikoValue] = None) -> Mapping[PikoValue, Any]:
    values = list(values or ALL_VALUES)
    payload = {'dxsEntries': [v.dxsNr for v in values]}
    data = requests.get(f'http://{hostname}/api/dxs.json', params=payload)
    values_by_id: dict[int, PikoValue] = {v.dxsNr: v for v in values}
    response = data.json()['dxsEntries']
    result = {}
    for obj in response:
        piko_value = values_by_id[obj['dxsId']]
        raw_value = obj['value']
        value = piko_value.parse(raw_value)
        result[piko_value] = value
    return result
    return {values_by_id[obj['dxsId']]: obj['value'] for obj in response}
