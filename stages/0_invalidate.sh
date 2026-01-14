#!/usr/bin/env bash
# Fetch the current ToxValDB version info from Clowder/Figshare
# This script detects the latest version and creates a version file for cache invalidation

set -e
mkdir -p download

# Get Figshare article info to detect current version
FIGSHARE_ARTICLE_ID="20394501"
FIGSHARE_API="https://api.figshare.com/v2/articles/${FIGSHARE_ARTICLE_ID}"

echo "Fetching ToxValDB version info from Figshare..."
curl -s "${FIGSHARE_API}" > download/figshare_info.json

# Extract version info
VERSION=$(jq -r '.title' download/figshare_info.json | grep -oP 'v[\d.]+' || echo "unknown")
PUBLISHED=$(jq -r '.published_date' download/figshare_info.json)
FIGSHARE_VERSION=$(jq -r '.version' download/figshare_info.json)

echo "ToxValDB Version: ${VERSION}"
echo "Published: ${PUBLISHED}"
echo "Figshare Version: ${FIGSHARE_VERSION}"

# Create version file for DVC cache invalidation
cat > download/version.json << EOF
{
  "toxvaldb_version": "${VERSION}",
  "figshare_version": ${FIGSHARE_VERSION},
  "published_date": "${PUBLISHED}",
  "fetched_at": "$(date -Iseconds)"
}
EOF

echo "Version info saved to download/version.json"
