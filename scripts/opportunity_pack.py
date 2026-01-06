import argparse
import yaml
from opportunity_intel.pack import create_opportunity_pack

def main():
    parser = argparse.ArgumentParser(description='Generate Opportunity Pack')
    parser.add_argument('--signal_url', required=True, help='URL to fetch signals from')
    parser.add_argument('--offer_config', required=True, help='Path to offer configuration YAML file')
    
    args = parser.parse_args()
    
    with open(args.offer_config, 'r') as file:
        offer_config = yaml.safe_load(file)

    opportunities = create_opportunity_pack(args.signal_url)
    
    for opportunity in opportunities:
        print(opportunity.to_markdown())

if __name__ == '__main__':
    main()
