import typer

app = typer.Typer()


@app.command()
def cleanup():
    """Clean up approved unused resources."""
    typer.echo("Cleanup command selected")