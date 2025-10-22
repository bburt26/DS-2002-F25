import sys
import os

# Support running as a module (python -m pokemon_lab.pipeline) and as a script (python pipeline.py)
try:
    from . import update_portfolio, generate_summary  # type: ignore
except Exception:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    import update_portfolio  # type: ignore
    import generate_summary  # type: ignore


def run_production_pipeline():
    """
    Runs the full production pipeline:
    1. ETL (update_portfolio.main)
    2. Reporting (generate_summary.main)
    """
    print("--- Starting Full Production Pipeline ---", file=sys.stderr)

    print("Running ETL step (update_portfolio.main)...", file=sys.stdout)
    update_portfolio.main()

    print("Running Reporting step (generate_summary.main)...", file=sys.stdout)
    generate_summary.main()

    print("--- Production Pipeline Completed Successfully ---", file=sys.stderr)


if __name__ == "__main__":
    run_production_pipeline()
