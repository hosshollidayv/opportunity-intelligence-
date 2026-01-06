import argparse
import os
from datetime import datetime, timezone
import yaml

from opportunity_intel.signals import fetch_signal
from opportunity_intel.entity_resolution import resolve_entities
from opportunity_intel.huntrix import analyze_opportunity
from opportunity_intel.pack import generate_pack, render_markdown


def load_previous_pack(output_dir, company_slug):
    if not os.path.exists(output_dir):
        return None

    runs = sorted(
        [
            d
            for d in os.listdir(output_dir)
            if os.path.isdir(os.path.join(output_dir, d))
        ],
        reverse=True,
    )

    for run in runs:
        path = os.path.join(output_dir, run, f"{company_slug}.md")
        if os.path.exists(path):
            with open(path, "r") as f:
                return f.read()

    return None


def normalize_for_comparison(markdown: str) -> str:
    """
    Remove run-specific metadata so only semantic signal content is compared.
    """
    lines = markdown.splitlines()

    normalized = []
    skip_prefixes = (
        "⚠️ SIGNAL CHANGE DETECTED",
        "No material change detected.",
        "Signal detected at",
    )

    for line in lines:
        if any(line.startswith(p) for p in skip_prefixes):
            continue
        normalized.append(line)

    return "\n".join(normalized).strip()


def main():
    parser = argparse.ArgumentParser(description="Run hiring signal batch")
    parser.add_argument("--sources", required=True, help="Path to hiring_sources.yaml")
    parser.add_argument("--output_dir", default="outputs", help="Base output directory")
    args = parser.parse_args()

    with open(args.sources, "r") as f:
        sources_config = yaml.safe_load(f)

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
    run_dir = os.path.join(args.output_dir, timestamp)
    os.makedirs(run_dir, exist_ok=True)

    changed_entries = []  # (CompanyName, relative_path)

    for source in sources_config.get("sources", []):
        company = source.get("company")
        url = source.get("url")
        company_slug = company.lower().replace(" ", "_")

        try:
            raw_signal = fetch_signal(url)
            entity = resolve_entities(raw_signal)
            routes = analyze_opportunity(raw_signal)

            pack = generate_pack(
                raw_signal=raw_signal,
                entity=entity,
                routes=routes,
                offer_config={"primary_buyer_roles": []},
            )

            current_md = render_markdown(pack)
            current_norm = normalize_for_comparison(current_md)

            previous_md = load_previous_pack(args.output_dir, company_slug)
            previous_norm = (
                normalize_for_comparison(previous_md) if previous_md else None
            )

            changed = previous_norm != current_norm

            header = (
                "⚠️ SIGNAL CHANGE DETECTED\n\n"
                if changed
                else "No material change detected.\n\n"
            )

            output_path = os.path.join(run_dir, f"{company_slug}.md")
            with open(output_path, "w") as out:
                out.write(header + current_md)

            print(f"[{'CHANGED' if changed else 'UNCHANGED'}] {company}")

            if changed:
                changed_entries.append(
                    (company, os.path.relpath(output_path, start=run_dir))
                )

        except Exception as e:
            print(f"[ERROR] {company}: {e}")

    if changed_entries:
        summary_path = os.path.join(run_dir, "CHANGED_SUMMARY.md")
        lines = []
        lines.append("# Changed Signals\n")
        lines.append(f"Run: {timestamp}\n")
        lines.append(f"Changed companies: {len(changed_entries)}\n")
        for company, relpath in changed_entries:
            lines.append(f"- **{company}**: `{relpath}`")
        lines.append("")
        with open(summary_path, "w") as f:
            f.write("\n".join(lines))


if __name__ == "__main__":
    main()
