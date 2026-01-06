import argparse
import os
from datetime import datetime
import yaml

from opportunity_intel.signals import fetch_signal
from opportunity_intel.entity_resolution import resolve_entities
from opportunity_intel.huntrix import analyze_opportunity
from opportunity_intel.pack import generate_pack, render_markdown


def main():
    parser = argparse.ArgumentParser(description="Run hiring signal batch")
    parser.add_argument("--sources", required=True, help="Path to hiring_sources.yaml")
    parser.add_argument("--output_dir", default="outputs", help="Base output directory")

    args = parser.parse_args()

    with open(args.sources, "r") as f:
        sources_config = yaml.safe_load(f)

    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%SZ")
    run_dir = os.path.join(args.output_dir, timestamp)
    os.makedirs(run_dir, exist_ok=True)

    for source in sources_config.get("sources", []):
        company = source.get("company")
        url = source.get("url")

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

            output_path = os.path.join(
                run_dir, f"{company.lower().replace(' ', '_')}.md"
            )

            with open(output_path, "w") as out:
                out.write(render_markdown(pack))

            print(f"[OK] Generated pack for {company}")

        except Exception as e:
            print(f"[ERROR] {company}: {e}")


if __name__ == "__main__":
    main()
