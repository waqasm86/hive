Title: ci: Windows & CI fixes

Summary

This PR addresses CI failures and Windows compatibility issues:

- Use `working-directory` steps in `.github/workflows/ci.yml` to avoid chained `cd` failures.
- Ensure `core` and `tools` are installed in CI using editable installs so linting/tests can import local packages.
- Fix Windows Unicode write errors by using UTF-8 for file I/O and `json.dump(..., ensure_ascii=False)` in storage backend.
- Remove problematic `tests/__init__.py` files and add `pytest.ini` so pytest collects tests correctly.
- Add runtime skips or Windows-friendly fallbacks for tests that require symlinks or Unix-only tools.
- Apply `ruff` auto-fixes and formatting to satisfy lint checks.

Testing

- Lint: `python -m ruff check core && python -m ruff check tools`
- Format check: `python -m ruff format --check core tools`
- Tests: `cd core && pytest tests/` (CI now uses `working-directory: core`)

Notes

- Ensure `.env` is added to `.gitignore` (already present).
- Revoke any exposed PATs and create new short-lived tokens before creating upstream PRs.

Files changed

- .github/workflows/ci.yml (use working-directory for lint/tests)
- core/framework/storage/backend.py (UTF-8 writes, ensure_ascii=False)
- pytest.ini (repo root)
- Removed `tests/__init__.py` in several locations
- Various `tools` fixes and ruff auto-fixes

Please run CI on the branch `chore/fix-windows-tests-encoding-clean` and review the workflow run for any remaining lint formatting files.
