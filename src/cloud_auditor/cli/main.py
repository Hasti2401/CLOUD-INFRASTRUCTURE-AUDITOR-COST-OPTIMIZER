import typer

from cloud_auditor.cli.scan import scan
from cloud_auditor.cli.report import report
from cloud_auditor.cli.cleanup import cleanup
from cloud_auditor.cli.config import config


app = typer.Typer(
    name="cloud-auditor",
    help="Cloud Infrastructure Auditor & Cost Optimizer",
)


app.command()(scan)
app.command()(report)
app.command()(cleanup)
app.command()(config)


@app.command()
def version():
    """Show the Cloud Auditor version."""
    typer.echo("Cloud Auditor version 0.1.0")


if __name__ == "__main__":
    app()