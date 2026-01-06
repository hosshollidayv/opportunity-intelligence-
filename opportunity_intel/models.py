from dataclasses import dataclass
from typing import List, Optional


@dataclass
class RawSignal:
    source_url: Optional[str]
    retrieved_at_iso: str
    title: Optional[str]
    excerpt: str
    raw_text: str


@dataclass
class Entity:
    company_name: Optional[str]
    canonical_domain: Optional[str]
    confidence: str
    notes: List[str]


@dataclass
class Route:
    route_type: str  # url | email | phone
    value: str
    label: str
    rank_reason: str


@dataclass
class Pack:
    signal_summary: str
    entity_resolution: Entity
    evidence: List[str]
    relevance: List[str]
    recommended_engagement: str
    contact_routes: List[Route]
    suggested_copy: str
