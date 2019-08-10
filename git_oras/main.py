import click


@click.group()
def cli():
    pass

@cli.command()
def status():
    pass


@cli.command()
def push():
    pass

@cli.command()
def pull():
    pass