import click
from flinkop.flinkop import flinkop
from redpanda_helm.redpanda import redpanda
from os import path

@click.group()
def dp():
    pass

if __name__ == '__main__':
    dp.add_command(flinkop)
    dp.add_command(redpanda)
    dp()