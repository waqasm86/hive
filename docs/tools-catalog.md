# Aden Tools Catalog

This document provides an initial inventory of MCP tools included with the `aden_tools` package. It is a living document — please update when adding or removing tools.

## Overview

The tools are organized by capability. The list below represents the current implemented tools discovered in the `tools/src/aden_tools/tools/` directory.

## File System Tools
- `apply_diff` — Apply a unified diff to a file
- `apply_patch` — Apply a patch to one or more files
- `execute_command` — Run shell commands in a safe subprocess helper
- `grep_search` — Search file contents using patterns
- `list_dir` — List directory contents
- `view_file` — Read and return file contents
- `write_to_file` — Write content to a file

## Web Tools
- `web_search` — Search the web (Brave / other providers)
- `web_scrape` — Fetch and parse web pages

## Document Tools
- `pdf_read` — Extract text from PDF documents

## Example / Template Tools
- `example_tool` — Template/example implementation for custom tools

## Notes
- This inventory is initial and should be audited against `tools/src/aden_tools/tools/` when new tools are added.
- Consider adding an automated test to verify the documented inventory matches the implementation.

## How to Contribute
If you add a new tool, please update this file with the tool name and a short description, and ensure any new tool has unit tests under `tools/tests/`.
