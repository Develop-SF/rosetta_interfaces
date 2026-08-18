# rosetta_interfaces

<!-- BEGIN sns_ci managed block -->
Org-wide invariants (synced from Develop-SF/sns_ci — do not edit here; change `agents/org-policy.md` in sns_ci instead):

- `main` is PR-only; never push to it directly. The **reviewer** merges the PR.
- Merge strategy: merge commits. Autosquash `fixup!` commits and rebase the branch on the target before merge; never use the GitHub "Update branch" merge-commit button on repos with commit lint.
- PR titles: start with an uppercase letter (an optional `[TICKET-123] ` prefix is allowed before it), no trailing period. No length limits on PR titles, commit subjects, or bodies.
- Branch naming: `{user-id}/feature/<name>` or `{user-id}/bugfix/<name>`.
- Releases use CalVer `YYYYMMDD-NN`. Never bump ROS `package.xml` versions.
- Registry etiquette (registry.snslocal.cc): scratch/experimental images go to `sandbox/`; never hand-tag anything in `release/`.
- Dependency updates to built images go through `sources.lock.yaml` PRs in `sns_docker`, never by editing image refs ad hoc.
- Cross-repo interface changes merge `sns_msgs` first, then consumers.
- Markdown prose: never hard-wrap to a column width — write each sentence or paragraph as one line and let editors soft-wrap. This applies to markdown files only: comments/annotations in config files and code keep their existing wrapping, and formatter-enforced line limits (e.g. Ruff's 79 for Python) still apply.
- A PR that changes commands, workflows, or policy this file describes must update `AGENTS.md` (repo-specific section) in the same PR.
- `CLAUDE.md` is a symlink to `AGENTS.md` — never replace it with a real file.
<!-- END sns_ci managed block -->

## Repo-specific

Pure ROS 2 Humble interface package (`ament_cmake` + rosidl): 3 actions (`ManageEpisode`, `RecordEpisode`, `RunPolicy`) and 2 services (`StartHILEpisode`, `StartRecording`). No nodes, no launch files. Consumed by `rosetta` (HIL support) and checked out directly by `sns_studio` CI — interface changes here follow the org's interfaces-first merge ordering (merge this repo before its consumers).

### Build / test / lint

```bash
# In a ROS 2 Humble workspace (ros:humble container works; the only
# dependency, action_msgs, ships with the base image):
rosdep install --from-paths src --ignore-src -r -y
colcon build --packages-select rosetta_interfaces
source install/setup.bash   # required before colcon test (import smoke test)
colcon test --packages-select rosetta_interfaces && colcon test-result --verbose
pre-commit run --all-files
```

### Required checks (stable names)

- `quality / quality` — pre-commit, AGENTS.md drift guards, PR-title format.
- `build / build` — colcon build (rosidl parses every `.msg`/`.srv`/`.action`)
  + colcon test (interface import smoke test, `ament_lint_auto`), in plain `ros:humble` mode via `Develop-SF/sns_ci` ros-build.yaml. No secrets on PRs.

### Local gotchas

- Adding/renaming an interface file: update `rosidl_generate_interfaces` in `CMakeLists.txt` and extend `test/test_interfaces_import.py` in the same PR.
- `colcon test` must run with `install/setup.bash` sourced or the import smoke test cannot find the generated Python modules.
- Never bump the `package.xml` version (org policy; releases are CalVer tags).
- No standalone IDL linter exists as a pre-commit hook; the `build / build` check is the IDL validation gate.
