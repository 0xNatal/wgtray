#!/bin/bash
set -euo pipefail

# Check that we are on the main branch
if [ "$(git branch --show-current)" != "main" ]; then
    echo "ERROR: Current branch is not 'main'" >&2
    exit 1
fi

# Check that github-cli is authenticated
if ! gh auth status > /dev/null 2>&1; then
    echo "ERROR: github-cli is not authenticated" >&2
    exit 2
fi

# Check that git-cliff is installed
if ! command -v git-cliff > /dev/null; then
    echo "ERROR: git-cliff is not installed (sudo pacman -S git-cliff)" >&2
    exit 3
fi

# Pull repo and fetch tags
git pull
git fetch --tags

# Check version argument
VERSION="${1:-}"
if [ -z "$VERSION" ]; then
    echo "Usage: ./scripts/release.sh 1.0.0" >&2
    exit 4
fi

LATEST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "none")

echo ""
echo "Latest tag:  $LATEST_TAG"
echo "New version: v$VERSION"
echo ""
read -rp "Continue? [y/N] " answer
case "$answer" in
    y|Y) ;;
    *) echo "Aborted." >&2; exit 5 ;;
esac

# Update version in PKGBUILD
sed -i "s/pkgver=.*/pkgver=$VERSION/" PKGBUILD

# Update version in constants.conf (single source of truth)
sed -i "s/VERSION=.*/VERSION=$VERSION/" res/constants.conf

# Update changelog
git-cliff --tag "v$VERSION" -o CHANGELOG.md

# Show changes
echo ""
git diff
echo ""
read -rp "Commit and release? [y/N] " answer
case "$answer" in
    y|Y) ;;
    *) echo "Aborted." >&2; exit 6 ;;
esac

# Commit, tag, push
git add PKGBUILD CHANGELOG.md res/constants.conf
git commit -m "release: v$VERSION"
git tag "v$VERSION"
git push
git push origin "v$VERSION"

# Create GitHub release with changelog as notes
echo ""
echo "Creating GitHub release..."
git-cliff --tag "v$VERSION" --latest --strip header | gh release create "v$VERSION" --title "v$VERSION" --notes-file -

echo ""
echo "Done! https://github.com/0xNatal/wgtray/releases/tag/v$VERSION"