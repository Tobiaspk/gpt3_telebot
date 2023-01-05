import click
from inspect_data import *

COMMANDS = [
    show_db_size,
    show_last_n,
    show_last_n_human,
    reset_db
]

@click.group()
def cli():
    pass

for c in COMMANDS:
    cli.add_command(c)

if __name__ == '__main__':
    cli()
