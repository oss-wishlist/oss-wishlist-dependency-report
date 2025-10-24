# README.md

## OSS Sustainability Analyzer

A GitHub Action that helps identify **which of your dependencies need sustainability support** by analyzing SBOM data and calculating risk scores based on the OpenSSF Criticality Score algorithm additionally weighted by the organizational affiliation of the user's login credentials.  Note: we know that many people use their personal email for work-related open source work, and  this is one way we can look at existing influence and support from an analytics perspective.

**Part of the [OSS Wishlist Initiative](https://github.com/your-org/oss-wishlist)** -  community-driven platform connecting maintainer needs with expert practitioners and company funding.

## The Problem We're Solving

The open source sustainability landscape is fragmented:
- **Companies struggle to identify** which dependencies actually need their support
- **Maintainers can't articulate** their sustainability needs in ways funders understand
- **Expert practitioners** are available but disconnected from projects that need them
- **Money exists** but demonstrating impact on sustainability is unclear

This action provides the **data foundation** to solve these problems by identifying **which dependencies in your supply chain are at risk** AND have declared a 'wish' for fullfillment via Open Source Wishlist.  You can also search for wishlists via our  main website.

## How This Fits Into OSS Wishlist
Discoverablity.
This action will surface wishes of a repository, through a reporting function. 

**This action is Step 1**: Help companies and developers understand **which dependencies in their supply chain need sustainability support** before those dependencies become supply chain incidents.

This provides **sustainability-focused risk assessment** that identifies projects where **expert intervention could make the biggest impact**.

## Features

- 📊 **Enhanced Criticality Score** - OpenSSF algorithm + organizational backing analysis
- 🔍 **Supply Chain Visibility** - See which dependencies are at risk using SBOM + ecosyste.ms
- 🌐 **Polyglot Support** - Works with npm, PyPI, Cargo, Maven, RubyGems, Go, NuGet, Hex, Pub, Composer, and more
- 📈 **Risk Categorization** - High/medium/low risk based on sustainability indicators
- 💬 **Automated Reporting** - PR comments and issues flag at-risk dependencies
- 📦 **SBOM Analysis** - Works with SPDX and CycloneDX formats
- 🏢 **Organizational Backing Assessment** - Evaluates maintainer employment/support structure

## Workflow
The workflow generates an SBOM if there is one one available 

1. anchore/sbom-action reads your package.json and package-lock.json
2. Generates sbom.json (temporary file in the workflow)
3. Your oss-analyzer action reads that sbom.json
3. Analyzes it and generates the risk report


