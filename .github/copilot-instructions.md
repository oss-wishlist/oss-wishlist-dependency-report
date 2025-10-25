# OSS Wishlist Dependency Report Action - Copilot Instructions

## Action Purpose
This GitHub Action analyzes project dependencies to identify sustainability risks by examining SBOM data and cross-referencing with ecosyste.ms API data. Part of the OSS Wishlist Initiative to help companies identify which dependencies need sustainability support.

## Code Architecture

### Configuration Management
**All hardcoded values are centralized in the `CONFIG` object** at the top of `index.js`. This includes:
- API endpoints and rate limits
- Default thresholds and limits
- Report templates and formatting
- Filtering patterns and exclusions
- Big Tech domain/org identifiers
- Package registry mappings for all ecosystems

**When modifying behavior**: Update the CONFIG object, not inline values.

### Supported Package Ecosystems
All registry mappings are in `CONFIG.REGISTRY_MAP`:
- npm (npmjs.org), PyPI (pypi.org), Cargo (crates.io), Maven (maven.org)
- RubyGems (rubygems.org), Go (pkg.go.dev), NuGet (nuget.org)
- Hex (hex.pm), Pub (pub.dev), Composer (packagist.org)
- Hackage, CocoaPods, Clojars, CPAN, CRAN, Conda

## Core Functionality

### 1. SBOM Processing
- **Input**: Accepts SBOM files in SPDX JSON or CycloneDX JSON format
- **Temp SBOM Creation**: If no SBOM exists, the workflow can generate one using anchore/sbom-action
- **Filtering**: Extracts packages from all supported ecosystems (npm, PyPI, Cargo, Maven, RubyGems, Go, NuGet, Hex, Pub, Composer, etc.)
- **Exclusions**: Filters out GitHub Actions, root packages, and internal tooling
- **Output**: List of components with name, version, PURL (Package URL), supplier, and license info

### 2. Ecosyste.ms Data Enrichment
For each dependency across **all package ecosystems**, fetches from ecosyste.ms API:
- **Supported ecosystems**: npm (npmjs.org), PyPI (pypi.org), Cargo (crates.io), Maven (maven.org), RubyGems (rubygems.org), Go (pkg.go.dev), NuGet (nuget.org), Hex (hex.pm), Pub (pub.dev), Composer (packagist.org), Hackage, CocoaPods, Clojars, CPAN, CRAN, Conda
- **Package name and version**
- **Dependents count** (number of other packages depending on this one)
- **Repository metadata** (stars, age, last update)
- **Repository URL**
- **Maintainer information** (for backing analysis)
- **GitHub Sponsors status** (proxy for oss-wishlist field)

### 3. Big Tech Backing Detection
Determines if a package has organizational support by checking:
- **Maintainer email domains** against list: amazon.com, microsoft.com, google.com, meta.com, facebook.com, openai.com, netflix.com, apple.com, oracle.com, ibm.com, salesforce.com, intel.com, amd.com
- **Repository owner names** against big tech org names (facebook, meta, google, microsoft, amazon, etc.)

### 4. Wishlist Filtering (Primary Filter)
**IMPORTANT**: The action filters based on **wishlist presence**, NOT dependency threshold.
- **Current implementation**: Filters for packages with GitHub Sponsors enabled
- **Future implementation**: Will filter on `oss-wishlist` field when available in ecosyste.ms
- **Purpose**: Report ALL dependencies that have declared wishes/needs, regardless of how many dependents they have
- **Dependency count is SHOWN but not used for filtering** - it's displayed to show the package's impact

## Report Criteria & Data Structure

### Analysis Results Object
```javascript
{
  packages: [
    {
      // From SBOM:
      name: string,
      version: string,
      purl: string,
      supplier: string,
      license: string,
      
      // From ecosyste.ms:
      dependents_count: number,      // Number of packages depending on this (SHOWN, not filtered)
      stars: number,                 // GitHub stars
      age_months: number,            // Age since creation
      last_update_months: number,    // Time since last update
      repository_url: string,        // GitHub/GitLab repo URL
      big_tech_backing: boolean,     // Has organizational support?
      has_wishlist: boolean          // Has wishlist/GitHub Sponsors (PRIMARY FILTER)
    }
  ],
  total_analyzed: number,            // Total dependencies scanned
  with_wishlist_count: number        // Count with wishlists (replaces high_dependency_count)
}
```

### Report Sections
1. **Summary**: Total deps scanned, wishlist count, with/without big tech backing counts
2. **⚠️ Dependencies with Wishlists Needing Support**: Packages with wishlists but no org support (sorted by dependents count for impact visibility)
3. **✅ Dependencies with Wishlists and Big Tech Backing**: Packages with wishlists that have org support

### Key Metrics Per Package
- **Dependents count** (📦) - Shows impact, but NOT used for filtering
- Stars (⭐)
- Age in months
- Last update in months
- Repository URL

## Current Outputs
- `with-wishlist-count`: Number of dependencies with wishlists (GitHub Sponsors)
- `without-backing-count`: Number with wishlists but no big tech backing
- `report-path`: Path to generated markdown report

## Optional Features
- **PR Comments**: Post report as PR comment (default: true)
- **Issue Creation**: Create GitHub issue for deps with wishlists needing support (default: false)

## Areas for Simplification
The core flow is solid:
1. ✅ Parse SBOM (or create temp SBOM)
2. ✅ Extract dependencies from all ecosystems
3. ✅ Fetch ecosyste.ms data
4. ✅ **Filter on wishlist presence** (currently GitHub Sponsors, will be `oss-wishlist` field)
5. ✅ Check for backing
6. ✅ Report generation - Shows dependency count for context but doesn't filter on it
