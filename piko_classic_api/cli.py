import time

import click

from piko_classic_api.livedata import get_live_data
import logging


@click.group
@click.option('-v', '--verbose', count=True)
def cli(verbose):
    match verbose:
        case 0:
            level = logging.WARNING
        case 1:
            level = logging.INFO
        case _:
            level = logging.DEBUG
    logging.basicConfig(format='m(asctime)s %(levelname)s: %(message)s', level=level)


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
    logging.info(f'starting Prometheus exporter on port {port}')
    prometheus_client.start_http_server(port)
    logging.info(f'polling http://{host} every {interval}s ...')
    while True:
        logging.debug('polling ...')
        try:
            metrics.poll()
        except Exception as e:
            logging.error('Exception polling PIKO:')
            logging.error(e)
        time.sleep(interval)


if __name__ == '__main__':
    cli()
