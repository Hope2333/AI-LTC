# Manual Testing Checklist Template

## Purpose

Document manual tests that cannot be automated on headless CI runners.

## Prerequisites

- [ ] Download latest build: `gh release download vX.Y.Z --repo owner/repo`
- [ ] Install on test machine
- [ ] Verify basic launch works

## Test Categories

### Rendering
- [ ] Canvas renders correctly
- [ ] Vector drawing works
- [ ] Text rendering (all fonts)
- [ ] Image import and display
- [ ] Blur effects and filters
- [ ] GPU acceleration (if applicable)

### Animation
- [ ] Timeline playback works
- [ ] Keyframe interpolation correct
- [ ] Loop playback
- [ ] Speed control

### Import/Export
- [ ] PNG import/export
- [ ] SVG export
- [ ] XEV import/export (native format)
- [ ] OpenRaster (ORA) import/export
- [ ] Video export (FFmpeg)

### Stability
- [ ] No crashes during normal use
- [ ] No rendering artifacts
- [ ] Memory usage reasonable over time
- [ ] Undo/redo works correctly

### Performance
- [ ] Startup time acceptable
- [ ] Canvas responsiveness
- [ ] Export speed
- [ ] Compare with previous version (if applicable)

## Results

| Test | Result | Notes |
|------|--------|-------|
| | ✅/❌ | |

## Blockers

| Issue | Severity | Workaround |
|-------|----------|------------|
| | High/Med/Low | |
