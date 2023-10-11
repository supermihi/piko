import pprint

import click

from livedata import get_live_data


@click.command
@click.argument('host')
def get(host):
    ld = get_live_data(host)
    for k, v in ld.items():
        print(k.format(v))


if __name__ == '__main__':
    get()
