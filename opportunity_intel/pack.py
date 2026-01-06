from .models import Opportunity
from .signals import fetch_signal
from .entity_resolution import resolve_entities
from .huntrix import discover_routes, generate_pack

def assemble_pack(signal_url, offer_config):
    raw_signal = fetch_signal(signal_url)
    entity = resolve_entities(raw_signal)
    routes = discover_routes(raw_signal)
    pack = generate_pack(entity, routes, offer_config)
    return pack
