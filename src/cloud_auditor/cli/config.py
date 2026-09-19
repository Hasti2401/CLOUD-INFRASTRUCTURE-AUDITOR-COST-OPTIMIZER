import typer

app = typer.Typer()


@app.command()
def config():
    """Manage Cloud Auditor configuration."""
    typer.echo("Config command selected")