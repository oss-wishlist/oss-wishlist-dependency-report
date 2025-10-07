"""Tests for CLI functionality."""

from click.testing import CliRunner
from oss_sustainability_analyzer.cli import main


class TestCLI:
    """Tests for command-line interface."""

    def test_cli_with_valid_url(self):
        """Test CLI with a valid GitHub URL."""
        runner = CliRunner()
        result = runner.invoke(main, ["https://github.com/owner/repo"])

        assert result.exit_code == 0
        assert "Analyzing repository" in result.output

    def test_cli_with_verbose_flag(self):
        """Test CLI with verbose flag."""
        runner = CliRunner()
        result = runner.invoke(main, ["https://github.com/owner/repo", "--verbose"])

        assert result.exit_code == 0

    def test_cli_with_output_file(self):
        """Test CLI with output file option."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(
                main, ["https://github.com/owner/repo", "--output", "report.txt"]
            )

            assert result.exit_code == 0
            assert "Report saved to report.txt" in result.output

    def test_cli_with_invalid_url(self):
        """Test CLI with invalid URL."""
        runner = CliRunner()
        result = runner.invoke(main, ["https://invalid-url.com/repo"])

        assert result.exit_code != 0
