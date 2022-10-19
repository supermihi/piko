from pathlib import Path

import pandas as pd
import requests
from datetime import datetime

default_hostname = 'piko'
default_user = 'pvserver'
default_password = 'pvwr'


def read_total_log():
    logfile_names = sorted(Path('.').resolve().glob('logdata-*.dat'))
    logfiles = [read_logdata(fn) for fn in logfile_names]
    log = pd.concat(logfiles)
    log = log.loc[~log.index.duplicated(keep='first')]
    return log


def read_logdata(filename: Path):
    print(f'reading {filename}...')
    table = pd.read_csv(str(filename), parse_dates=[0], date_parser=lambda t: pd.to_datetime(t, unit='s'), index_col=0,
                        skiprows=6, sep=r'\t', skipinitialspace=True,
                        error_bad_lines=True)
    table['P'] = total_power(table)
    table['W'] = table['P'] / 4000
    return table


def total_power(table):
    return table['AC1 P'] + table['AC2 P'] + table['AC3 P']


# per_day.plot(kind='bar', xticks=[str(dt.date()) for dt in per_day.index])
def fetch(hostname=default_hostname, user=default_user, password=default_password) -> bytes:
    data = requests.get(f'http://{hostname}/LogDaten.dat', auth=(user, password))
    return data.content


def fetch_and_store(hostname=default_hostname, user=default_user, password=default_password):
    data = fetch(hostname, user, password)
    now = datetime.now()
    filename = f"logdata-{now:%Y-%m-%d}.dat"
    Path(filename).write_bytes(data)
    print(f'wrote {filename}')


if __name__ == '__main__':
    fetch_and_store()
