import click
from flinkop.flinkop import flinkop
from redpanda_helm.redpanda import redpanda
from scylladb.scylladb import scylladb
from sparkop.sparkop import sparkop
from miniop.miniop import miniop
from os import path

@click.group()
def dp():
    pass

if __name__ == '__main__':
    dp.add_command(flinkop)
    dp.add_command(redpanda)
    dp.add_command(scylladb)
    dp.add_command(sparkop)
    dp.add_command(miniop)
    dp()