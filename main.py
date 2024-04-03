import typer
from pgcheck.connection import perform_connection
from pgcheck.translator import perform_translation
from pgcheck.evaluation import perform_performance_test

app = typer.Typer()


@app.command()
def connect(database: str, username: str, password: str, host: str = 'localhost', port: int = 5432):
    """Connect to a PostgreSQL database using provided credentials."""
    perform_connection(database, username, password, host, port)
    typer.echo("Connection established.")


@app.command()
def translate(sql: str):
    """Translate existing CHECK constraints into triggers and stored functions."""
    perform_translation(sql)
    typer.echo("Translation completed.")


@app.command()
def performance(report: str = "performance_report.txt"):
    """Run performance tests on the translated constraints."""
    perform_performance_test(report)
    typer.echo(f"Performance report generated: {report}")


@app.command()
def help(command: str = None):
    """Display help information for the CLI or a specific command."""
    if command:
        typer.echo(typer.Typer.get_command(app, command).help)
    else:
        typer.echo(app.get_help())


if __name__ == "__main__":
    app()
