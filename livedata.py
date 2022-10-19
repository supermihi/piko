from typing import Iterable

import requests
from values import PikoValue, all as all_values


def get_live_data(hostname: str = 'piko', values: Iterable[PikoValue] = None) -> dict[PikoValue, float]:
    values = values or all_values
    payload = {'dxsEntries': [v.dxsNr for v in values]}
    data = requests.get(f'http://{hostname}/api/dxs.json', params=payload)
    values_by_id = {v.dxsNr: v for v in values}
    ans = data.json()['dxsEntries']
    return {values_by_id[obj['dxsId']]: obj['value'] for obj in ans}


ld = get_live_data('piko', all_values)
for val in all_values:
    print(val.format(ld[val]))
