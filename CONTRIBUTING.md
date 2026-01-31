# Contributing

## Commit Guidelines

This project uses [Conventional Commits](https://www.conventionalcommits.org/).

### Format

```
<type>(<scope>): <description>
```

### Types

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation |
| `style` | Formatting (no code change) |
| `refactor` | Code restructuring |
| `perf` | Performance improvement |
| `test` | Tests |
| `chore` | Maintenance |

### Examples

```
feat: add settings dialog
fix: icon not showing in dark mode
docs: update readme
refactor: simplify icon loading
chore: update dependencies
```

### Breaking Changes

```
feat!: change config location

BREAKING CHANGE: configs now stored in ~/.config/wgtray
```

## Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feat/my-feature`)
3. Commit your changes (following the guidelines above)
4. Push to your fork
5. Open a Pull Request