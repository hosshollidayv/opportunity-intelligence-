from urllib.parse import urlparse
from opportunity_intel.models import Entity


def resolve_entities(raw_signal):
    notes = []

    if raw_signal.source_url:
        parsed = urlparse(raw_signal.source_url)
        domain = parsed.netloc
        confidence = "HIGH"
        notes.append("Domain extracted from source URL.")
    else:
        domain = None
        confidence = "LOW"
        notes.append("No source URL provided.")

    company_name = None
    if domain:
        company_name = domain.split(".")[0].capitalize()
        notes.append("Company name derived from domain heuristic.")

    return Entity(
        company_name=company_name,
        canonical_domain=domain,
        confidence=confidence,
        notes=notes,
    )
