# Development of `streamlit-session-memo`

## Set up
* Install `uv`
* Install dependencies
  ```shell
  $ uv sync
  ```
* Install pre-commit
  ```shell
  $ pre-commit install
  ```

## Release
Releases are automated by [`scriv-release`](https://github.com/whitphx/scriv-release), which runs on every push to `main` (`.github/workflows/release.yml`).

1. Add a changelog fragment to any PR whose change should be released.
   ```shell
   $ uvx scriv create --edit
   ```
   This writes a new file under `changelog.d/`. Fill in the relevant section (`### Added`, `### Fixed`, ...) and commit it with the PR.
   The categories of the pending fragments decide the version bump: `Removed` is major, `Added` / `Changed` / `Deprecated` are minor, and the rest are patch. While the version is still `0.x`, a major bump is downshifted to a minor one.
2. Once such a PR is merged, the workflow collects the pending fragments into `CHANGELOG.md` and opens a "Changelog Preview for Next Release" PR.
3. Merging that PR creates and pushes the `v<version>` tag, which triggers the build, PyPI publish, and GitHub Release jobs in `main.yml`.

The version number lives only in the Git tags, from which `hatch-vcs` derives the package version, so no file needs to be edited to bump it.

The workflow needs a GitHub App to push the release tag, because a tag pushed with the default `GITHUB_TOKEN` does not trigger `main.yml`. The App's credentials are read from the `RELEASE_APP_CLIENT_ID` repository variable and the `RELEASE_APP_KEY` repository secret. See [the `scriv-release` token setup doc](https://github.com/whitphx/scriv-release/blob/main/docs/token-setup.md).
