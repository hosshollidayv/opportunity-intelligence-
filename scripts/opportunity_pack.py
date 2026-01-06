import argparse
import yaml
from opportunity_intel.pack import assemble_pack
from opportunity_intel.signals import fetch_signal

def main():
    parser = argparse.ArgumentParser(description='Generate Opportunity Pack')
    parser.add_argument('--signal_url', required=True, help='URL to fetch signals from')
    parser.add_argument('--offer_config', required=True, help='Path to offer configuration YAML file')
    
    args = parser.parse_args()
    
    with open(args.offer_config, 'r') as file:
        offer_config = yaml.safe_load(file)

    pack = assemble_pack(args.signal_url, offer_config)
    
    print(render_markdown(pack))

if __name__ == '__main__':
    main()
