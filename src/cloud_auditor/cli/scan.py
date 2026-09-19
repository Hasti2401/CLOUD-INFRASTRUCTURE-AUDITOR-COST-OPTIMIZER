import typer

app = typer.Typer()


@app.command()
def scan():
    """Scan AWS resources for security and cost issues."""
    typer.echo("Scan command selected")