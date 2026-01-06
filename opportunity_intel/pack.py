from .models import Opportunity
from .signals import fetch_signal
from .entity_resolution import resolve_entities
from .huntrix import analyze_opportunity

def create_opportunity_pack(signal_url):
    signal_data = fetch_signal(signal_url)
    resolved_data = resolve_entities(signal_data)
    opportunities = [Opportunity(**item) for item in resolved_data]
    return opportunities
