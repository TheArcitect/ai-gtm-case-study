"""Smoke test for gtm-casegen CLI."""

import tempfile
from pathlib import Path
from subprocess import run


def test_smoke():
    """Test the complete CLI workflow."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        examples_dir = tmp_path / "examples"
        out_dir = tmp_path / "out"
        
        # Test init command
        result = run(
            ["uv", "run", "gtm-casegen", "init", "--dir", str(examples_dir)],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        assert result.returncode == 0, f"Init failed: {result.stderr}"
        
        # Check that files were created
        assert (examples_dir / "case.yaml").exists()
        assert (examples_dir / "assets" / "placeholder.png").exists()
        
        # Test generate command
        result = run(
            ["uv", "run", "gtm-casegen", "generate", "--input", str(examples_dir / "case.yaml"), "--out", str(out_dir)],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        assert result.returncode == 0, f"Generate failed: {result.stderr}"
        
        # Check that output was created
        output_file = out_dir / "case-study.md"
        assert output_file.exists()
        
        # Check that output contains expected content
        content = output_file.read_text()
        assert "Reduced SDR ramp time with GenAI call notes" in content
        assert "36.7%" in content  # Ramp time improvement
        assert "45%" in content    # Meetings improvement
        assert "8pp" in content    # Qualified rate improvement
