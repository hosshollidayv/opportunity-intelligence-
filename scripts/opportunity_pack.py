import argparse
import yaml

from opportunity_intel.signals import fetch_signal
from opportunity_intel.entity_resolution import resolve_entities
from opportunity_intel.huntrix import analyze_opportunity
from opportunity_intel.pack import generate_pack
from opportunity_intel.pack import render_markdown


def main():
    parser = argparse.ArgumentParser(description="Generate Opportunity Pack (No-Send)")
    parser.add_argument("--signal_url", required=True)
    parser.add_argument("--offer_config", required=True)

    args = parser.parse_args()

    with open(args.offer_config, "r") as f:
        offer_config = yaml.safe_load(f)

    raw_signal = fetch_signal(args.signal_url)
    entity = resolve_entities(raw_signal)
    routes = analyze_opportunity(raw_signal)
    pack = generate_pack(
        raw_signal=raw_signal,
        entity=entity,
        routes=routes,
        offer_config=offer_config,
    )

    print(render_markdown(pack))


if __name__ == "__main__":
    main()
