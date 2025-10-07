"""Tests for the analyzer module."""

import pytest
from oss_sustainability_analyzer.analyzer import parse_github_url, analyze_repository


class TestParseGithubUrl:
    """Tests for GitHub URL parsing."""

    def test_parse_https_url(self):
        """Test parsing HTTPS GitHub URL."""
        owner, repo = parse_github_url("https://github.com/owner/repo")
        assert owner == "owner"
        assert repo == "repo"

    def test_parse_git_url(self):
        """Test parsing git protocol URL."""
        owner, repo = parse_github_url("git@github.com:owner/repo.git")
        assert owner == "owner"
        assert repo == "repo"

    def test_parse_invalid_url(self):
        """Test that invalid URL raises ValueError."""
        with pytest.raises(ValueError):
            parse_github_url("https://gitlab.com/owner/repo")


class TestAnalyzeRepository:
    """Tests for repository analysis."""

    def test_analyze_valid_repository(self):
        """Test analyzing a valid repository."""
        result = analyze_repository("https://github.com/owner/repo")

        assert result["repository"] == "owner/repo"
        assert result["status"] == "analyzed"
        assert "metrics" in result

    def test_analyze_invalid_url(self):
        """Test that analyzing invalid URL raises ValueError."""
        with pytest.raises(ValueError):
            analyze_repository("https://invalid-url.com/repo")
