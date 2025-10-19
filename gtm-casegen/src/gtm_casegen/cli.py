"""CLI commands for gtm-casegen."""

import base64
import os
from pathlib import Path
from typing import Optional

import typer
import yaml
from jinja2 import Environment, FileSystemLoader
from rich.console import Console
from rich.logging import RichHandler

# Initialize Rich console and logging
console = Console()
app = typer.Typer(help="Generate GTM case studies from YAML metrics")


def create_placeholder_png(path: Path) -> None:
    """Create a 1x1 placeholder PNG from base64."""
    # 1x1 transparent PNG in base64
    png_data = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(png_data)


def compute_deltas(baseline: dict, after: dict) -> dict:
    """Compute percentage and percentage point deltas."""
    deltas = {}
    
    # Ramp days percentage change
    if baseline.get("ramp_days", 0) > 0:
        deltas["ramp_days_pct"] = round(
            (after.get("ramp_days", 0) - baseline.get("ramp_days", 0)) / baseline.get("ramp_days", 1) * 100, 1
        )
    else:
        deltas["ramp_days_pct"] = 0.0
    
    # Meetings per rep per week percentage change
    if baseline.get("avg_meetings_per_rep_week", 0) > 0:
        deltas["meetings_pct"] = round(
            (after.get("avg_meetings_per_rep_week", 0) - baseline.get("avg_meetings_per_rep_week", 0)) / baseline.get("avg_meetings_per_rep_week", 1) * 100, 1
        )
    else:
        deltas["meetings_pct"] = 0.0
    
    # Qualified rate percentage points change
    deltas["qualified_pp"] = round(
        after.get("qualified_rate_pct", 0) - baseline.get("qualified_rate_pct", 0), 1
    )
    
    return deltas


@app.command()
def init(
    dir: Path = typer.Option(..., "--dir", help="Directory to create sample files in")
) -> None:
    """Initialize a sample case.yaml and placeholder assets."""
    console.print(f"[green]Initializing sample files in {dir}[/green]")
    
    # Create directory
    dir.mkdir(parents=True, exist_ok=True)
    
    # Create sample case.yaml
    sample_data = {
        "project": {
            "title": "Reduced SDR ramp time with GenAI call notes",
            "anonymize": True,
            "timeframe": "Jan–Mar 2025"
        },
        "customer": {
            "industry": "SaaS",
            "size": "Series B (~120)",
            "region": "US"
        },
        "problem": {
            "summary": "Slow ramp & inconsistent handoffs SDR → AE."
        },
        "metrics": {
            "baseline": {
                "ramp_days": 60,
                "avg_meetings_per_rep_week": 4.2,
                "qualified_rate_pct": 21
            },
            "after": {
                "ramp_days": 38,
                "avg_meetings_per_rep_week": 6.1,
                "qualified_rate_pct": 29
            }
        },
        "evidence": {
            "notes": "LLM prompts standardized notes & summaries.",
            "assets": [
                {
                    "path": "examples/assets/placeholder.png",
                    "caption": "Pipeline growth (redacted)"
                }
            ]
        },
        "results": {
            "highlights": [
                "Ramp time ↓ 36.7% (60 → 38 days)",
                "Meetings/rep/week ↑ 45% (4.2 → 6.1)",
                "Qualified rate ↑ 8pp (21% → 29%)"
            ]
        },
        "cta": {
            "contact_email": "michael@letsexperiment.com",
            "link": "https://linkedin.com/in/michael-schaeffer-ba3762382/"
        }
    }
    
    case_yaml_path = dir / "case.yaml"
    with open(case_yaml_path, "w") as f:
        yaml.dump(sample_data, f, default_flow_style=False, sort_keys=False)
    
    console.print(f"[green]✓ Created {case_yaml_path}[/green]")
    
    # Create placeholder PNG
    assets_dir = dir / "assets"
    placeholder_path = assets_dir / "placeholder.png"
    create_placeholder_png(placeholder_path)
    console.print(f"[green]✓ Created {placeholder_path}[/green]")


@app.command()
def generate(
    input: Path = typer.Option(..., "--input", help="Path to input YAML file"),
    out: Path = typer.Option(..., "--out", help="Output directory")
) -> None:
    """Generate a case study from YAML metrics."""
    console.print(f"[green]Generating case study from {input}[/green]")
    
    # Load YAML data
    try:
        with open(input, "r") as f:
            data = yaml.safe_load(f)
    except Exception as e:
        console.print(f"[red]Error loading YAML: {e}[/red]")
        raise typer.Exit(1)
    
    # Compute deltas
    deltas = compute_deltas(data["metrics"]["baseline"], data["metrics"]["after"])
    data["deltas"] = deltas
    
    # Load Jinja2 template
    template_dir = Path(__file__).parent / "templates"
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("case.md.j2")
    
    # Render template
    try:
        rendered = template.render(**data)
    except Exception as e:
        console.print(f"[red]Error rendering template: {e}[/red]")
        raise typer.Exit(1)
    
    # Write output
    out.mkdir(parents=True, exist_ok=True)
    output_path = out / "case-study.md"
    with open(output_path, "w") as f:
        f.write(rendered)
    
    console.print(f"[green]✓ Generated {output_path}[/green]")


if __name__ == "__main__":
    app()
