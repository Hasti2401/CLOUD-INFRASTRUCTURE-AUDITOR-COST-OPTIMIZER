import typer

from cloud_auditor.cli.scan import scan
from cloud_auditor.cli.report import report
from cloud_auditor.cli.cleanup import cleanup
from cloud_auditor.cli.config import config
from cloud_auditor.cli.aws.authentication import(
    create_aws_session,
    verify_aws_authentication,
)

app = typer.Typer(
    name="cloud-auditor",
    help="Cloud Infrastructure Auditor & Cost Optimizer",
)


app.command()(scan)
app.command()(report)
app.command()(cleanup)
app.command()(config)

@app.command()
def auth():
    """Verify AWS authentication."""
    try:
        session = create_aws_session()
        identity = verify_aws_authentication(session)

        typer.echo("AWS Authentication")
        typer.echo("------------------")
        typer.echo("Status : SUCCESS")
        typer.echo(f"Account: {identity['Account']}")
        typer.echo(f"Region : {session.region_name}")
        typer.echo(f"ARN    : {identity['Arn']}")

    except Exception as exc:
        typer.echo("AWS Authentication")
        typer.echo("------------------")
        typer.echo("Status : FAILED")
        typer.echo(f"Error  : {exc}")


@app.command()
def version():
    """Show the Cloud Auditor version."""
    typer.echo("Cloud Auditor version 0.1.0")


if __name__ == "__main__":
    app()