import typer

app = typer.Typer()


@app.command()
def report():
    """Generate an audit report."""
    typer.echo("Report command selected")