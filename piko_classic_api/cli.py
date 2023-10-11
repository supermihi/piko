import click

from piko_classic_api.livedata import get_live_data


@click.group
def cli():
    pass


@cli.command
@click.argument('host')
def get(host):
    ld = get_live_data(host)
    for k, v in ld.items():
        print(k.format(v))


if __name__ == '__main__':
    cli()
