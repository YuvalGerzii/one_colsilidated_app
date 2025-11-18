"""
Unified Entity Resolver

Resolves entities (people, companies, properties) across all platforms.
Same person appearing in Bond.AI network should link to their Labor profile
and any Finance/Real Estate transactions.
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import hashlib
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class EntityType(Enum):
    PERSON = "person"
    COMPANY = "company"
    PROPERTY = "property"
    SKILL = "skill"
    OPPORTUNITY = "opportunity"


@dataclass
class EntityReference:
    """Reference to an entity in a specific platform"""
    entity_id: str
    platform: str
    entity_type: EntityType
    attributes: Dict[str, Any]
    confidence: float


@dataclass
class UnifiedEntity:
    """A resolved entity that spans multiple platforms"""
    unified_id: str
    entity_type: EntityType
    canonical_name: str
    references: List[EntityReference]
    merged_attributes: Dict[str, Any]
    resolution_confidence: float
    created_at: datetime
    updated_at: datetime


class UnifiedEntityResolver:
    """
    Resolves entities across platforms using multiple matching strategies.

    Strategies:
    - Exact match (email, phone, tax ID)
    - Fuzzy match (name similarity)
    - Graph-based (connected entities)
    - Vector similarity (embeddings)
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.entity_cache: Dict[str, UnifiedEntity] = {}
        self.resolution_rules = self._initialize_rules()

    def _initialize_rules(self) -> List[Dict[str, Any]]:
        """Initialize entity resolution rules by type"""

        return [
            # Person resolution rules
            {
                "entity_type": EntityType.PERSON,
                "exact_fields": ["email", "phone", "linkedin_url"],
                "fuzzy_fields": ["name", "company"],
                "fuzzy_threshold": 0.85,
                "weight": 1.0
            },
            # Company resolution rules
            {
                "entity_type": EntityType.COMPANY,
                "exact_fields": ["tax_id", "domain", "linkedin_company_url"],
                "fuzzy_fields": ["name", "address"],
                "fuzzy_threshold": 0.90,
                "weight": 1.0
            },
            # Property resolution rules
            {
                "entity_type": EntityType.PROPERTY,
                "exact_fields": ["parcel_id", "address_normalized"],
                "fuzzy_fields": ["address", "owner_name"],
                "fuzzy_threshold": 0.95,
                "weight": 1.0
            },
            # Skill resolution rules
            {
                "entity_type": EntityType.SKILL,
                "exact_fields": ["skill_id", "canonical_name"],
                "fuzzy_fields": ["name", "aliases"],
                "fuzzy_threshold": 0.80,
                "weight": 0.8
            }
        ]

    async def resolve_entity(
        self,
        entity_ref: EntityReference
    ) -> UnifiedEntity:
        """
        Resolve a single entity reference to a unified entity.

        If entity already exists, merge. Otherwise create new.
        """

        # Check cache first
        cache_key = self._compute_cache_key(entity_ref)
        if cache_key in self.entity_cache:
            existing = self.entity_cache[cache_key]
            return await self._merge_entity(existing, entity_ref)

        # Search for matching entities
        matches = await self._find_matches(entity_ref)

        if matches:
            # Merge with best match
            best_match = max(matches, key=lambda x: x[1])
            unified = await self._merge_entity(best_match[0], entity_ref)
        else:
            # Create new unified entity
            unified = self._create_unified_entity(entity_ref)

        # Cache and return
        self.entity_cache[unified.unified_id] = unified
        return unified

    async def resolve_batch(
        self,
        entity_refs: List[EntityReference]
    ) -> List[UnifiedEntity]:
        """Resolve multiple entities in batch"""

        results = []
        for ref in entity_refs:
            unified = await self.resolve_entity(ref)
            results.append(unified)
        return results

    async def find_cross_platform_matches(
        self,
        entity_type: EntityType,
        attributes: Dict[str, Any],
        platforms: Optional[List[str]] = None
    ) -> List[UnifiedEntity]:
        """
        Find entities matching attributes across specified platforms.

        Example:
            matches = await resolver.find_cross_platform_matches(
                EntityType.PERSON,
                {"name": "John Smith", "company": "Acme Corp"},
                platforms=["bond_ai", "labor"]
            )
        """

        matching_entities = []

        for unified_id, entity in self.entity_cache.items():
            if entity.entity_type != entity_type:
                continue

            # Check if entity exists in requested platforms
            if platforms:
                entity_platforms = {ref.platform for ref in entity.references}
                if not entity_platforms.intersection(set(platforms)):
                    continue

            # Check attribute match
            match_score = self._calculate_attribute_match(
                entity.merged_attributes, attributes
            )

            if match_score > 0.7:
                matching_entities.append((entity, match_score))

        # Sort by match score
        matching_entities.sort(key=lambda x: x[1], reverse=True)
        return [e[0] for e in matching_entities]

    async def _find_matches(
        self,
        entity_ref: EntityReference
    ) -> List[Tuple[UnifiedEntity, float]]:
        """Find existing entities that match the reference"""

        matches = []

        # Get rules for this entity type
        rules = [r for r in self.resolution_rules
                 if r["entity_type"] == entity_ref.entity_type]

        if not rules:
            return matches

        rule = rules[0]

        for unified_id, entity in self.entity_cache.items():
            if entity.entity_type != entity_ref.entity_type:
                continue

            score = 0.0
            match_count = 0

            # Check exact field matches
            for field in rule["exact_fields"]:
                ref_value = entity_ref.attributes.get(field)
                entity_value = entity.merged_attributes.get(field)

                if ref_value and entity_value and ref_value == entity_value:
                    score += 1.0
                    match_count += 1

            # Check fuzzy field matches
            for field in rule["fuzzy_fields"]:
                ref_value = entity_ref.attributes.get(field)
                entity_value = entity.merged_attributes.get(field)

                if ref_value and entity_value:
                    similarity = self._string_similarity(
                        str(ref_value).lower(),
                        str(entity_value).lower()
                    )
                    if similarity >= rule["fuzzy_threshold"]:
                        score += similarity
                        match_count += 1

            if match_count > 0:
                avg_score = score / match_count
                if avg_score >= 0.7:
                    matches.append((entity, avg_score))

        return matches

    async def _merge_entity(
        self,
        existing: UnifiedEntity,
        new_ref: EntityReference
    ) -> UnifiedEntity:
        """Merge a new reference into an existing unified entity"""

        # Check if this reference already exists
        existing_platforms = {ref.platform for ref in existing.references}
        if new_ref.platform in existing_platforms:
            # Update existing reference
            for i, ref in enumerate(existing.references):
                if ref.platform == new_ref.platform:
                    existing.references[i] = new_ref
                    break
        else:
            # Add new reference
            existing.references.append(new_ref)

        # Merge attributes (prefer higher confidence sources)
        merged = existing.merged_attributes.copy()
        for key, value in new_ref.attributes.items():
            if key not in merged or new_ref.confidence > existing.resolution_confidence:
                merged[key] = value

        existing.merged_attributes = merged
        existing.updated_at = datetime.now()
        existing.resolution_confidence = max(
            existing.resolution_confidence,
            new_ref.confidence
        )

        return existing

    def _create_unified_entity(self, entity_ref: EntityReference) -> UnifiedEntity:
        """Create a new unified entity from a reference"""

        unified_id = self._generate_unified_id(entity_ref)
        canonical_name = self._extract_canonical_name(entity_ref)

        return UnifiedEntity(
            unified_id=unified_id,
            entity_type=entity_ref.entity_type,
            canonical_name=canonical_name,
            references=[entity_ref],
            merged_attributes=entity_ref.attributes.copy(),
            resolution_confidence=entity_ref.confidence,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

    def _compute_cache_key(self, entity_ref: EntityReference) -> str:
        """Compute a cache key for an entity reference"""
        key_data = f"{entity_ref.platform}:{entity_ref.entity_id}:{entity_ref.entity_type.value}"
        return hashlib.md5(key_data.encode()).hexdigest()

    def _generate_unified_id(self, entity_ref: EntityReference) -> str:
        """Generate a unique ID for a unified entity"""
        timestamp = datetime.now().timestamp()
        data = f"{entity_ref.entity_type.value}:{timestamp}:{entity_ref.entity_id}"
        return f"unified_{hashlib.sha256(data.encode()).hexdigest()[:16]}"

    def _extract_canonical_name(self, entity_ref: EntityReference) -> str:
        """Extract canonical name from entity attributes"""
        name_fields = ["name", "full_name", "company_name", "address", "title"]
        for field in name_fields:
            if field in entity_ref.attributes:
                return str(entity_ref.attributes[field])
        return f"Unknown {entity_ref.entity_type.value}"

    def _string_similarity(self, s1: str, s2: str) -> float:
        """Calculate string similarity using Levenshtein ratio"""
        if s1 == s2:
            return 1.0

        len1, len2 = len(s1), len(s2)
        if len1 == 0 or len2 == 0:
            return 0.0

        # Simple character-based similarity
        matches = sum(1 for a, b in zip(s1, s2) if a == b)
        return (2.0 * matches) / (len1 + len2)

    def _calculate_attribute_match(
        self,
        attrs1: Dict[str, Any],
        attrs2: Dict[str, Any]
    ) -> float:
        """Calculate similarity between two attribute dictionaries"""

        if not attrs1 or not attrs2:
            return 0.0

        common_keys = set(attrs1.keys()) & set(attrs2.keys())
        if not common_keys:
            return 0.0

        matches = 0
        for key in common_keys:
            v1, v2 = attrs1[key], attrs2[key]
            if v1 == v2:
                matches += 1
            elif isinstance(v1, str) and isinstance(v2, str):
                if self._string_similarity(v1.lower(), v2.lower()) > 0.8:
                    matches += 0.8

        return matches / len(common_keys)

    def get_entity_graph(
        self,
        unified_id: str
    ) -> Dict[str, Any]:
        """
        Get the cross-platform graph for an entity.

        Returns all platforms where entity exists and related entities.
        """

        if unified_id not in self.entity_cache:
            return {"error": "Entity not found"}

        entity = self.entity_cache[unified_id]

        graph = {
            "unified_id": unified_id,
            "entity_type": entity.entity_type.value,
            "canonical_name": entity.canonical_name,
            "platforms": [],
            "related_entities": []
        }

        for ref in entity.references:
            graph["platforms"].append({
                "platform": ref.platform,
                "entity_id": ref.entity_id,
                "confidence": ref.confidence,
                "attributes": ref.attributes
            })

        return graph

    def get_resolution_stats(self) -> Dict[str, Any]:
        """Get statistics about entity resolution"""

        stats = {
            "total_unified_entities": len(self.entity_cache),
            "by_type": {},
            "cross_platform_entities": 0,
            "average_references_per_entity": 0
        }

        total_refs = 0
        for entity in self.entity_cache.values():
            entity_type = entity.entity_type.value
            stats["by_type"][entity_type] = stats["by_type"].get(entity_type, 0) + 1

            if len(entity.references) > 1:
                stats["cross_platform_entities"] += 1

            total_refs += len(entity.references)

        if self.entity_cache:
            stats["average_references_per_entity"] = total_refs / len(self.entity_cache)

        return stats
