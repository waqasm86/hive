---
title: "docs: Fix MCP tools count inconsistency and add tools catalog"
labels: documentation, bug
---

### Problem

The README claims a fixed number of MCP tools which appears inaccurate (e.g., "19 MCP tools"). This misleads users and reduces trust in docs.

### Proposed Solution

1. Audit `tools/src/aden_tools/tools/` and produce a canonical `docs/tools-catalog.md` listing implemented tools and short descriptions.
2. Update `README.md` and `tools/README.md` to reference the catalog instead of a hardcoded count.
3. Add a small test to ensure the documented inventory matches the implementation.

Changes to propose:

- `docs/tools-catalog.md` (new) — canonical inventory
- `README.md` — reference catalog
- `tools/tests/test_tool_inventory.py` — simple check that tools directory contains entries

### Benefits

- Accurate documentation and improved trust
- Easier onboarding for contributors
- Automated guard against future documentation drift

### Estimated Effort

1-2 hours

---
This is implemented as a quick PR in `fix/docs-tools-catalog` (see branch on my fork). I can submit a PR for this change if you'd like me to open it via the web UI.
