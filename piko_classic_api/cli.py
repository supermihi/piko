import time

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


@cli.command
@click.argument('host')
@click.option('-i', '--interval', default=5, help='polling interval (in seconds)')
@click.option('-p', '--port', default=8007, help='HTTP port to listen on')
def export(interval, host, port):
    from piko_classic_api.prometheus import PikoClassicMetrics
    import prometheus_client
    metrics = PikoClassicMetrics(host)

    prometheus_client.REGISTRY.unregister(prometheus_client.GC_COLLECTOR)
    prometheus_client.REGISTRY.unregister(prometheus_client.PLATFORM_COLLECTOR)
    prometheus_client.REGISTRY.unregister(prometheus_client.PROCESS_COLLECTOR)

    prometheus_client.start_http_server(port)
    while True:
        metrics.poll()
        time.sleep(interval)


if __name__ == '__main__':
    cli()
