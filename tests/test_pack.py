import pytest
from opportunity_intel.models import Pack, RawSignal, Entity, Route
from opportunity_intel.pack.generate import generate_pack

def test_pack_generation():
    entity = Entity(domain="example.com", company_name="Example")
    evidence = ["Snippet 1 with relevant information.", "Snippet 2 with more details.", "Snippet 3 with additional context."]
    relevance = ["Hypothesis: This is relevant to the opportunity."]
    contact_routes = [Route(name="John Doe", position="Manager", email="john@example.com")]
    
    pack = generate_pack(
        signal_summary="Example Opportunity",
        entity=entity,
        evidence=evidence,
        relevance=relevance,
        recommended_engagement="Reach out via email.",
        contact_routes=contact_routes
    )
    
    assert len(pack.evidence) <= 3
    assert all(len(snippet.split()) <= 25 for snippet in pack.evidence)
    assert all("Hypothesis:" in line for line in pack.relevance)
    assert all(field in pack.__dict__ for field in ['signal_summary', 'entity_resolution', 'evidence', 'relevance', 'recommended_engagement', 'contact_routes'])
