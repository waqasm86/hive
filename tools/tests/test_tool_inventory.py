import pathlib


def test_tools_directory_has_entries():
    """Ensure the aden_tools tools directory exists and contains tool subfolders/files."""
    repo_root = pathlib.Path(__file__).resolve().parents[3]
    tools_dir = repo_root / "tools" / "src" / "aden_tools" / "tools"

    assert tools_dir.exists(), f"Tools directory not found: {tools_dir}"

    # Count immediate children (files and folders) - must be at least 1
    entries = [p for p in tools_dir.iterdir() if p.name != "__pycache__"]
    assert len(entries) >= 1, f"Expected at least one tool implementation, found {len(entries)}"
