import click
from flinkop.flinkop import flinkop

@click.group()
def dp():
    pass

if __name__ == '__main__':
    dp.add_command(flinkop)
    dp()