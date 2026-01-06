from opportunity_intel.models import Pack


def generate_pack(*, raw_signal, entity, routes, offer_config):
    return Pack(
        signal_summary=f"Signal detected at {raw_signal.retrieved_at_iso}",
        entity_resolution=entity,
        evidence=[raw_signal.excerpt[:200]] if raw_signal.excerpt else [],
        relevance=["Hypothesis: None (no strong keyword match)"],
        recommended_engagement=f"Target roles: {offer_config.get('primary_buyer_roles', [])}",
        contact_routes=routes or [],
        suggested_copy="Generic outreach based on observed public signal.",
    )


def render_markdown(pack: Pack) -> str:
    lines = []

    lines.append("# Opportunity Pack\n")

    lines.append("## Signal Summary")
    lines.append(pack.signal_summary + "\n")

    lines.append("## Entity Resolution")
    if pack.entity_resolution:
        lines.append(f"- Company: {pack.entity_resolution.company_name}")
        lines.append(f"- Domain: {pack.entity_resolution.canonical_domain}")
        lines.append(f"- Confidence: {pack.entity_resolution.confidence}\n")

    lines.append("## Evidence")
    for e in pack.evidence:
        lines.append(f"- {e}")

    lines.append("\n## Relevance")
    for r in pack.relevance:
        lines.append(r)

    lines.append("\n## Recommended Engagement")
    lines.append(pack.recommended_engagement)

    lines.append("\n## Contact Routes")
    if pack.contact_routes:
        for route in pack.contact_routes:
            lines.append(f"- {route.route_type}: {route.value}")
    else:
        lines.append("- None found")

    lines.append("\n## Suggested Copy (No-Send)")
    lines.append(pack.suggested_copy)

    return "\n".join(lines)
