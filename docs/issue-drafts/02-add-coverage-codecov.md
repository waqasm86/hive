---
title: "test: Add test coverage reporting with Codecov integration"
labels: enhancement, testing, ci/cd
---

### Problem

There is currently no test coverage reporting. We need visibility into coverage to prevent regressions and identify untested code.

### Proposed Solution

Add `pytest-cov` to dev dependencies, configure coverage reporting, and upload results to Codecov in CI. Add a coverage badge to the README.

Suggested CI steps:

```yaml
test:
  name: Run Tests with Coverage
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
        pip install -e ./tools
        pip install -r core/requirements-dev.txt
    - name: Run tests with coverage
      run: |
        cd core
        pytest --cov=framework --cov-report=xml --cov-report=term
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./core/coverage.xml
        flags: core-framework
        name: codecov-core
        fail_ci_if_error: false
```

Add to README:

```markdown
[![codecov](https://codecov.io/gh/adenhq/hive/branch/main/graph/badge.svg)](https://codecov.io/gh/adenhq/hive)
```

### Benefits

- Visibility into test coverage
- Prevent coverage regressions on PRs
- Identify untested modules to prioritize tests

### Estimated Effort

3-4 hours (requires maintainers to set `CODECOV_TOKEN` if needed)

---
I can implement CI config and docs; Codecov token must be added by repo admins.
