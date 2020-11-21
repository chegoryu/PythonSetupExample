import click

from .helpers import helpers


@click.group(context_settings={'help_option_names': ['-h', '--help']})
def cli():
    pass


@cli.command(name='sum', help='Sum numbers.')
@click.argument('numbers', type=click.INT, nargs=-1)
def sum(numbers):
    click.echo(helpers.sum_numbers(numbers))


@cli.command(name='sort', help='Sort numbers.')
@click.argument('numbers', type=click.INT, nargs=-1)
@click.option('--reverse', type=click.BOOL, default=False)
def sort(numbers, reverse):
    click.echo(" ".join(map(str, helpers.sort_numbers(numbers, reverse=reverse))))
