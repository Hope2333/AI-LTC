# Packaging Workflows Pattern

## Overview

Automated packaging workflow for distributing builds across platforms.

## Structure

```
.github/workflows/release.yml
├── Trigger: on push of v* tags
├── Prepare: install dependencies, configure build
├── Build matrix: Linux (deb/pacman/AppImage), Windows, macOS
├── Upload: GitHub Releases with artifacts
└── Notify: optional Discord/Slack notification
```

## Key Patterns

### 1. Tag-Triggered Release

```yaml
on:
  push:
    tags:
      - 'v*'
```

### 2. Multi-Format Packaging

- **deb**: Debian/Ubuntu packages
- **pacman**: Arch Linux packages
- **AppImage**: Portable Linux binary

### 3. Auto-Upload to GitHub Releases

```yaml
- uses: softprops/action-gh-release@v2
  with:
    files: |
      *.deb
      *.pkg.tar.zst
      *.AppImage
```

## Lessons Learned

1. **deb version format** — remove `-1` suffix for native packages
2. **AppImage on Arch** — use `appimagetool` instead of linuxdeploy on Ubuntu 22.04
3. **PKGBUILD generation** — dynamic version extraction from git tags
4. **debian/changelog** — use `dch` without `--create` if file exists

## Checklist

- [ ] Workflow triggers on v* tags
- [ ] All package formats build successfully
- [ ] Artifacts uploaded to GitHub Releases
- [ ] Version numbers extracted correctly from git tags
- [ ] Package metadata (description, maintainer) is accurate
