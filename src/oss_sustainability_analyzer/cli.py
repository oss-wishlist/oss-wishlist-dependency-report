"""Command-line interface for OSS Sustainability Analyzer."""

import click
from .analyzer import analyze_repository


@click.command()
@click.argument("repository_url")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.option("--output", "-o", default=None, help="Output file for the report")
def main(repository_url, verbose, output):
    """Analyze the sustainability of an open source repository.

    REPOSITORY_URL: The URL of the repository to analyze (e.g., https://github.com/owner/repo)
    """
    click.echo(f"Analyzing repository: {repository_url}")

    try:
        result = analyze_repository(repository_url, verbose=verbose)

        if output:
            with open(output, "w") as f:
                f.write(str(result))
            click.echo(f"Report saved to {output}")
        else:
            click.echo("\n=== Sustainability Analysis Report ===")
            click.echo(result)

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()


if __name__ == "__main__":
    main()
