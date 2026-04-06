# Version Adaptation Documentation

## Overview

When upgrading a major dependency, document API differences and adaptation strategies.

## Template

### [Dependency] [Old Version] → [New Version]

**Date**: YYYY-MM-DD
**Primary Version**: [New Version]
**Fallback Version**: [Old Version] (if needed)

### Breaking Changes

| Old API | New API | Files Affected |
|---------|---------|---------------|
| | | |

### Compatibility Layer

```c
// version_compat.h
#if DEPENDENCY_VERSION >= VERSION(100)
  // New API
#else
  // Old API shim
#endif
```

### Build Configuration Changes

```cmake
# CMakeLists.txt changes
find_package(Dependency 100 REQUIRED)
```

### Testing Strategy

- [ ] Build on all target distros
- [ ] Run smoke tests
- [ ] Manual UI/rendering validation
- [ ] Performance benchmark (old vs new)

### Rollback Plan

If the upgrade fails:
1. Revert to previous version tag
2. Remove compatibility layer
3. Document failure reason
