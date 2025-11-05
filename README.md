# README.md

## OSS Sustainability Analyzer

A GitHub Action that helps identify **which of your dependencies need sustainability support** by analyzing an SBOM, enriching with ecosyste.ms metadata, detecting wishlist/funding signals, and optionally filtering by OpenSSF Scorecard and Criticality scores.

**Part of the OSS Wishlist Initiative** — a community effort connecting maintainer needs with expert practitioners and company funding.

## The Problem We're Solving

The open source sustainability landscape is fragmented:
- **Companies struggle to identify** which dependencies actually need their support
- **Maintainers can't articulate** their sustainability needs in ways funders understand
- **Expert practitioners** are available but disconnected from projects that need them
- **Money exists** but demonstrating impact on sustainability is unclear

This action provides the **data foundation** to solve these problems by identifying **which dependencies in your supply chain are at risk** AND have declared a funding “wishlist” (currently proxied by GitHub Sponsors and other funding links in ecosyste.ms).

## How This Fits Into OSS Wishlist
Discoverablity.
This action will surface wishes of a repository, through a reporting function. 

**This action is Step 1**: Help companies and developers understand **which dependencies in their supply chain need sustainability support** before those dependencies become supply chain incidents.

This provides **sustainability-focused risk assessment** that identifies projects where **expert intervention could make the biggest impact**.

## Features

- 📊 **OpenSSF Scorecard & Criticality (optional filters)** — Filter the report by Scorecard (0–10) and/or Criticality (0–1) when enabled
- 🔍 **Supply Chain Visibility** - See which dependencies are at risk using SBOM + ecosyste.ms
- 🌐 **Polyglot Support** - Works with npm, PyPI, Cargo, Maven, RubyGems, Go, NuGet, Hex, Pub, Composer, and more
- 📈 **Risk Categorization** - High/medium/low risk based on sustainability indicators
- 💬 **Automated Reporting** - PR comments and issues flag at-risk dependencies
- 📦 **SBOM Analysis** - Works with SPDX and CycloneDX formats
- 🏢 **Maintainer Big Tech email alias** — Flags dependencies whose maintainers use Big Tech email domains (optional inclusion)

## How it works

1) SBOM input
- The action consumes a Software Bill of Materials (SBOM) in SPDX JSON or CycloneDX JSON.
- The provided workflow can also generate an SBOM for you using anchore/sbom-action.
- We extract Package URLs (PURLs) from the SBOM and analyze dependencies across many ecosystems (npm, PyPI, Cargo, Maven, RubyGems, Go, NuGet, Hex, Pub, Composer, and more).

2) Enrichment via ecosyste.ms
- For each dependency PURL, the action queries ecosyste.ms to retrieve repository metadata (stars, age, last update), dependents count, repository URL, maintainers, and funding signals.
- Wishlist detection today is based on funding/sponsor signals (e.g., funding_links on the package/owner/repo, owner sponsors listing, or repo FUNDING file). When ecosyste.ms exposes an official `oss-wishlist` field, the action will pivot to that.

3) Optional filtering
- Maintainer Big Tech email alias: By default, packages with maintainers using Big Tech email domains are excluded; you can opt-in to include them.
- OpenSSF Scorecard filter: If enabled, calls the public Scorecard API for GitHub repos and only includes packages within your score range.
- OpenSSF Criticality filter: If enabled, filters by Criticality score when available in ecosyste.ms metadata.

4) Report generation
- The report contains a summary and two sections grouped by “maintainer Big Tech email alias” presence, listing key metrics per package: dependents, stars, age, last update, repository link, funding links, and (when available) Scorecard and Criticality values.

## Inputs (Action)

- sbom-path: Path to SPDX/CycloneDX JSON SBOM (default: sbom.json)
- token: GitHub token for API access
- create-issue: Create an issue summarizing results (default: false)
- comment-pr: Comment a PR with results (default: true)
- include-bigtech-backed: Include dependencies with Big Tech backing (default: false)
- filter-scorecard: Filter by OpenSSF Scorecard score range (default: false)
	- scorecard-min: Minimum Scorecard score (0.0 – 10.0)
	- scorecard-max: Maximum Scorecard score (0.0 – 10.0)
- filter-criticality: Filter by OpenSSF Criticality score (if available in metadata; default: false)
	- criticality-min: Minimum Criticality score (0.0 – 1.0)
	- criticality-max: Maximum Criticality score (0.0 – 1.0)
- use-wishlists-json: Enable a local wishlists JSON file as the primary wishlist source (default: false)
- wishlists-path: Path to local wishlists JSON file (default: wishlists.json)

Notes:
- Scorecard scores are retrieved via the public OpenSSF Scorecard API for GitHub-hosted repositories when filtering is enabled.
- Criticality score filtering is best-effort and only applied when the metric is available in ecosyste.ms metadata.

### Using a local wishlists JSON file (temporary stand-in for ecosyste.ms field)

Until ecosyste.ms exposes an official `oss-wishlist` field, you can provide a JSON file that explicitly marks packages as having wishlists. This allows testing with **actual projects** and **actual wishes** before the field is available.

**Recommended location:** `wishlists.json` in your repository root.

**To enable:** Set `use-wishlists-json: true` in your workflow (or use the manual workflow checkbox). If enabled, the action will load the file and treat matching packages as having wishlists, regardless of funding signals.

**Supported JSON formats** (choose one):

1) Array of entries

```json
[
	{ "purl": "pkg:npm/%40types/node@20.10.0", "has_wishlist": true, "links": ["https://github.com/sponsors/foo"] },
	{ "type": "pypi", "name": "requests", "has_wishlist": true }
]
```

2) Object map (keys are purl or `type:name`), values may be `true` or an object

```json
{
	"pkg:npm/lodash@4.17.21": true,
	"pypi:requests": { "has_wishlist": true, "links": ["https://opencollective.com/requests"] }
}
```

**Behavior:**
- If a local entry is found for a component by exact PURL match, it takes precedence.
- Otherwise, a `type:name` (e.g., `npm:lodash`) match is attempted (version-agnostic).
- `has_wishlist` defaults to `true` when an entry exists.
- Any `links` provided are merged into the Funding section of the report.
- The report will note "Wishlist source: mock JSON file" for transparency.
- When enabled, this overrides the default funding-based proxy for matched packages.

**Legacy input names:** If you previously used `mock-wishlists-path` or `wishlist-map-path`, those are still supported as fallbacks when `use-wishlists-json` is not enabled.

## SBOM generation details

The example manual workflow includes a step that can generate an SBOM automatically:

- Tool: `anchore/sbom-action`
- Formats: `spdx-json` or `cyclonedx-json`
- Output path configurable (default `sbom.json`)

Coverage tips:
- Transitive dependencies are best captured when lockfiles or installed artifacts exist.
	- Node: include `package-lock.json` or `yarn.lock`
	- Python: include `Poetry.lock` or `pip-compile` outputs, or scan a built image/virtualenv
- You can also point the action at a pre-existing SBOM if you already generate one elsewhere.

## OpenSSF Scorecard

- What it is: A set of repository-level checks producing a score from 0 to 10.
- How we get it: When “Filter by OpenSSF Scorecard score range” is enabled, the action:
	- Parses `repository_url` for each dependency to extract `owner/repo` if it’s a GitHub URL.
	- Calls `https://api.securityscorecards.dev/projects/github.com/{owner}/{repo}`.
	- Caches responses per run and adds a small delay between calls.
	- Skips packages without a GitHub repo or with unavailable scores (and logs the skip reason).
- How it’s used: Only packages with scores within the selected min–max range are included.

## OpenSSF Criticality

- What it is: A 0–1 score estimating the importance of a project.
- How we get it: Best-effort — we read any `criticality_score` surfaced via ecosyste.ms metadata when available for the repository.
- How it’s used: If the filter is enabled, only packages whose score is within the selected min–max range are included. If a package has no criticality score, it is skipped (logged).

## Maintainer Big Tech email alias

- Purpose: Flag whether any maintainers use email addresses from a curated list of Big Tech domains defined in configuration.
- Behavior: By default, packages with such maintainers are excluded from the “needs support” section to highlight projects without that affiliation; you can opt-in to include them via the workflow checkbox.
- Scope: This detection uses maintainer email domains only. It does not infer affiliation from repository owner names.

## Running it manually

- Go to Actions → “Run OSS Wishlist Analyzer (manual)” → select options:
	- Optionally generate an SBOM, choose format, or provide a path to an existing SBOM.
	- Toggle “Include dependencies whose maintainers use Big Tech email domains”.
	- Toggle Scorecard and/or Criticality filters and set ranges.
- Outputs:
	- Report file `oss-wishlist-report.md` is uploaded as artifact and referenced in the job summary with a preview.
	- SBOM summary and SBOM artifact are uploaded when SBOM generation is enabled.

## Workflow
The workflow generates an SBOM if there is one one available 

1. anchore/sbom-action reads your package.json and package-lock.json
2. Generates sbom.json (temporary file in the workflow)
3. Your oss-analyzer action reads that sbom.json
3. Analyzes it and generates the risk report


