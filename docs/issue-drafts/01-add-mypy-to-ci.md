---
title: "chore(ci): Add mypy type checking to CI pipeline"
labels: enhancement, ci/cd, code-quality
---

### Problem

The codebase has partial type hints but no automated type checking in CI. Type errors can slip through reviews and cause runtime issues.

### Proposed Solution

Add `mypy` to the CI workflow and include a `mypy.ini` configuration. Start with lenient settings and gradually tighten.

Suggested `mypy.ini`:

```ini
[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
ignore_missing_imports = True
check_untyped_defs = True
disallow_untyped_calls = False
disallow_untyped_defs = False
files = core/framework, tools/src/aden_tools

[mypy-tests.*]
ignore_errors = True
```

Suggested CI job snippet:

```yaml
type-check:
  name: Type Checking (mypy)
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - name: Set up Python 3.11
      uses: actions/setup-python@v4
      with:
        python-version: 3.11
    - name: Install dependencies
      run: |
        pip install -e ./core
        pip install mypy
    - name: Run mypy
      run: mypy --config-file mypy.ini
```

### Benefits

- Catch type errors early
- Improve refactoring safety and IDE experience
- Foundation for stricter type enforcement later

### Estimated Effort

2-3 hours (create config, add CI job, fix immediate blocking errors)

---
I can implement this in a PR if maintainers approve.
