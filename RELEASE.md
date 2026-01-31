# Creating a new release

> **Note:** Releases are created by the maintainer only.

## Requirements

- [git-cliff](https://github.com/orhun/git-cliff) (`sudo pacman -S git-cliff`)
- [github-cli](https://cli.github.com/) (`sudo pacman -S github-cli`)

## Run the script

From the root of the repo:

```bash
./scripts/release.sh X.Y.Z
```

Where `X.Y.Z` is the version number to create (e.g. `1.0.0`)

## What the script does

1. Updates version in `PKGBUILD`
2. Generates `CHANGELOG.md`
3. Shows diff for review
4. Creates commit and tag
5. Pushes to GitHub
6. Creates GitHub release with changelog

## AUR Release

After the GitHub release, update the AUR package:

```bash
cd /path/to/wgtray-aur/

# Copy updated PKGBUILD
cp /path/to/wgtray/PKGBUILD .

# Update checksums (if source changed)
updpkgsums

# Generate .SRCINFO
makepkg --printsrcinfo > .SRCINFO

# Commit and push
git add PKGBUILD .SRCINFO
git commit -m "Update to vX.Y.Z"
git push
```