# Multi-Distro CI Pattern

## Overview

Test builds across multiple Linux distributions to ensure compatibility.

## Structure

```
.github/workflows/multi-distro.yml
├── Matrix strategy (OS, FFmpeg version, compiler)
├── Container jobs for each distro
├── Shared build steps
└── Per-distro dependency installation
```

## Key Patterns

### 1. Container-Based Isolation

Use Docker containers for each distro to avoid host pollution:

```yaml
strategy:
  matrix:
    include:
      - os: ubuntu-22.04
        ffmpeg: "4.4"
        compiler: gcc-11
      - os: ubuntu-24.04
        ffmpeg: "6.x"
        compiler: gcc-13
```

### 2. Compatibility Layers

When dependencies have breaking APIs across versions, create a compat header:

```c
// ffmpeg_compat.h
#if LIBAVUTIL_VERSION_INT < AV_VERSION_INT(57, 0, 0)
  // Old API shims
#else
  // New API
#endif
```

### 3. Per-Distro Dependency Installation

```yaml
- name: Install dependencies
  run: |
    case ${{ matrix.distro }} in
      ubuntu*) apt-get install -y ... ;;
      arch)    pacman -S --noconfirm ... ;;
      debian)  apt-get install -y ... ;;
    esac
```

## Lessons Learned

1. **Split incompatible distros into separate jobs** — Arch and Debian may need different compilers
2. **Install git before checkout** — container images may not have git
3. **Use clang for older distros** — GCC 12+ may not be available
4. **Python version matters** — some build systems need `python-is-python3`

## Checklist

- [ ] All target distros defined in matrix
- [ ] Per-distro dependency installation tested
- [ ] Compatibility layer covers all API differences
- [ ] Build artifacts uploaded per distro
- [ ] Failure logs clearly identify which distro failed
