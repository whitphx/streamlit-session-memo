# Changelog

<!-- scriv-insert-here -->

<a id='changelog-0.5.0'></a>
## 0.5.0 — 2026-08-24

### Removed

- Dropped support for Python 3.9, which reached end of life. The minimum supported version is now 3.10, and the `typing-extensions` dependency it required is gone.

<a id='changelog-0.4.2'></a>
## 0.4.2 — 2026-08-24

### Chore

- GitHub Releases now carry the version's `CHANGELOG.md` entry as their release notes, instead of an empty body.

<a id='changelog-0.4.1'></a>
## 0.4.1 — 2026-08-24

### Chore

- Bumped `pypa/gh-action-pypi-publish` to v1.14.2, whose Twine 7.0.0 accepts the `Metadata-Version: 2.5` that `hatchling` 1.32.0 now emits by default.

- Automated the release flow with [`scriv-release`](https://github.com/whitphx/scriv-release): changelog fragments merged into `main` are collected into a preview PR, and merging that PR tags the release.
