"""
Cross-Platform Knowledge Graph

Unified knowledge representation connecting entities across all platforms:
- People (investors, professionals, contacts)
- Companies (firms, startups, employers)
- Properties (real estate assets)
- Skills (capabilities, certifications)
- Opportunities (jobs, deals, investments)
"""

from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)


class NodeType(Enum):
    """Types of nodes in the knowledge graph"""
    PERSON = "person"
    COMPANY = "company"
    PROPERTY = "property"
    SKILL = "skill"
    OPPORTUNITY = "opportunity"
    DOCUMENT = "document"
    EVENT = "event"
    LOCATION = "location"
    INDUSTRY = "industry"
    CERTIFICATION = "certification"


class EdgeType(Enum):
    """Types of relationships between nodes"""
    WORKS_AT = "works_at"
    OWNS = "owns"
    INVESTED_IN = "invested_in"
    KNOWS = "knows"
    HAS_SKILL = "has_skill"
    LOCATED_IN = "located_in"
    INTERESTED_IN = "interested_in"
    APPLIED_TO = "applied_to"
    MANAGES = "manages"
    PARTNERS_WITH = "partners_with"
    REQUIRES = "requires"
    SIMILAR_TO = "similar_to"
    MENTIONED_IN = "mentioned_in"
    ATTENDED = "attended"


@dataclass
class GraphNode:
    """A node in the knowledge graph"""
    node_id: str
    node_type: NodeType
    name: str
    properties: Dict[str, Any] = field(default_factory=dict)
    source_platforms: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    confidence: float = 1.0


@dataclass
class GraphEdge:
    """An edge (relationship) in the knowledge graph"""
    edge_id: str
    edge_type: EdgeType
    source_id: str
    target_id: str
    properties: Dict[str, Any] = field(default_factory=dict)
    weight: float = 1.0
    bidirectional: bool = False
    source_platform: str = ""
    created_at: datetime = field(default_factory=datetime.now)


class CrossPlatformKnowledgeGraph:
    """
    Unified knowledge graph connecting entities across all platforms.

    Features:
    - Entity storage and retrieval
    - Relationship management
    - Graph traversal and path finding
    - Pattern detection
    - Knowledge inference
    """

    def __init__(self):
        self.nodes: Dict[str, GraphNode] = {}
        self.edges: Dict[str, GraphEdge] = {}
        self.adjacency: Dict[str, List[str]] = defaultdict(list)  # node_id -> [edge_ids]
        self.type_index: Dict[NodeType, Set[str]] = defaultdict(set)  # type -> {node_ids}

    async def add_node(
        self,
        node_type: NodeType,
        name: str,
        properties: Optional[Dict[str, Any]] = None,
        source_platform: str = "unknown"
    ) -> GraphNode:
        """Add a node to the knowledge graph"""

        node_id = f"{node_type.value}_{name.lower().replace(' ', '_')}_{datetime.now().timestamp()}"

        node = GraphNode(
            node_id=node_id,
            node_type=node_type,
            name=name,
            properties=properties or {},
            source_platforms=[source_platform]
        )

        self.nodes[node_id] = node
        self.type_index[node_type].add(node_id)

        logger.info(f"Added node: {node_id} ({node_type.value})")
        return node

    async def add_edge(
        self,
        edge_type: EdgeType,
        source_id: str,
        target_id: str,
        properties: Optional[Dict[str, Any]] = None,
        weight: float = 1.0,
        bidirectional: bool = False,
        source_platform: str = "unknown"
    ) -> GraphEdge:
        """Add an edge (relationship) to the knowledge graph"""

        if source_id not in self.nodes:
            raise ValueError(f"Source node {source_id} not found")
        if target_id not in self.nodes:
            raise ValueError(f"Target node {target_id} not found")

        edge_id = f"{edge_type.value}_{source_id}_{target_id}_{datetime.now().timestamp()}"

        edge = GraphEdge(
            edge_id=edge_id,
            edge_type=edge_type,
            source_id=source_id,
            target_id=target_id,
            properties=properties or {},
            weight=weight,
            bidirectional=bidirectional,
            source_platform=source_platform
        )

        self.edges[edge_id] = edge
        self.adjacency[source_id].append(edge_id)

        if bidirectional:
            self.adjacency[target_id].append(edge_id)

        logger.info(f"Added edge: {source_id} --{edge_type.value}--> {target_id}")
        return edge

    async def get_node(self, node_id: str) -> Optional[GraphNode]:
        """Get a node by ID"""
        return self.nodes.get(node_id)

    async def get_nodes_by_type(self, node_type: NodeType) -> List[GraphNode]:
        """Get all nodes of a specific type"""
        node_ids = self.type_index.get(node_type, set())
        return [self.nodes[nid] for nid in node_ids if nid in self.nodes]

    async def get_neighbors(
        self,
        node_id: str,
        edge_types: Optional[List[EdgeType]] = None,
        direction: str = "outgoing"  # outgoing, incoming, both
    ) -> List[Tuple[GraphNode, GraphEdge]]:
        """Get neighboring nodes and their connecting edges"""

        if node_id not in self.nodes:
            return []

        neighbors = []

        for edge_id in self.adjacency.get(node_id, []):
            edge = self.edges.get(edge_id)
            if not edge:
                continue

            # Filter by edge type
            if edge_types and edge.edge_type not in edge_types:
                continue

            # Determine neighbor based on direction
            if direction == "outgoing" and edge.source_id == node_id:
                neighbor_id = edge.target_id
            elif direction == "incoming" and edge.target_id == node_id:
                neighbor_id = edge.source_id
            elif direction == "both":
                neighbor_id = edge.target_id if edge.source_id == node_id else edge.source_id
            else:
                continue

            neighbor = self.nodes.get(neighbor_id)
            if neighbor:
                neighbors.append((neighbor, edge))

        return neighbors

    async def find_path(
        self,
        start_id: str,
        end_id: str,
        max_depth: int = 5
    ) -> Optional[List[Tuple[GraphNode, GraphEdge]]]:
        """Find shortest path between two nodes using BFS"""

        if start_id not in self.nodes or end_id not in self.nodes:
            return None

        if start_id == end_id:
            return [(self.nodes[start_id], None)]

        # BFS
        visited = {start_id}
        queue = [(start_id, [(self.nodes[start_id], None)])]

        while queue:
            current_id, path = queue.pop(0)

            if len(path) > max_depth:
                continue

            neighbors = await self.get_neighbors(current_id, direction="both")

            for neighbor, edge in neighbors:
                if neighbor.node_id == end_id:
                    return path + [(neighbor, edge)]

                if neighbor.node_id not in visited:
                    visited.add(neighbor.node_id)
                    queue.append((neighbor.node_id, path + [(neighbor, edge)]))

        return None

    async def find_connections(
        self,
        node_id: str,
        target_type: NodeType,
        max_hops: int = 3
    ) -> List[Dict[str, Any]]:
        """Find all connections to nodes of a specific type within N hops"""

        if node_id not in self.nodes:
            return []

        connections = []
        visited = {node_id}
        queue = [(node_id, 0, [])]

        while queue:
            current_id, depth, path = queue.pop(0)

            if depth > max_hops:
                continue

            neighbors = await self.get_neighbors(current_id, direction="both")

            for neighbor, edge in neighbors:
                if neighbor.node_id in visited:
                    continue

                visited.add(neighbor.node_id)
                new_path = path + [(neighbor.node_id, edge.edge_type.value)]

                if neighbor.node_type == target_type:
                    connections.append({
                        "node": neighbor,
                        "hops": depth + 1,
                        "path": new_path
                    })

                if depth + 1 < max_hops:
                    queue.append((neighbor.node_id, depth + 1, new_path))

        # Sort by number of hops
        connections.sort(key=lambda x: x["hops"])
        return connections

    async def get_subgraph(
        self,
        center_id: str,
        radius: int = 2
    ) -> Dict[str, Any]:
        """Extract a subgraph around a central node"""

        if center_id not in self.nodes:
            return {"nodes": [], "edges": []}

        # BFS to find all nodes within radius
        node_ids = {center_id}
        edge_ids = set()
        queue = [(center_id, 0)]

        while queue:
            current_id, depth = queue.pop(0)

            if depth >= radius:
                continue

            for edge_id in self.adjacency.get(current_id, []):
                edge = self.edges.get(edge_id)
                if not edge:
                    continue

                edge_ids.add(edge_id)
                neighbor_id = edge.target_id if edge.source_id == current_id else edge.source_id

                if neighbor_id not in node_ids:
                    node_ids.add(neighbor_id)
                    queue.append((neighbor_id, depth + 1))

        return {
            "nodes": [self.nodes[nid] for nid in node_ids],
            "edges": [self.edges[eid] for eid in edge_ids]
        }

    async def find_similar_nodes(
        self,
        node_id: str,
        limit: int = 10
    ) -> List[Tuple[GraphNode, float]]:
        """Find nodes similar to the given node based on shared connections"""

        if node_id not in self.nodes:
            return []

        node = self.nodes[node_id]
        candidates = list(self.type_index.get(node.node_type, set()))

        # Get neighbors of the target node
        target_neighbors = set()
        for edge_id in self.adjacency.get(node_id, []):
            edge = self.edges.get(edge_id)
            if edge:
                neighbor_id = edge.target_id if edge.source_id == node_id else edge.source_id
                target_neighbors.add(neighbor_id)

        # Score candidates by shared neighbors (Jaccard similarity)
        similarities = []
        for candidate_id in candidates:
            if candidate_id == node_id:
                continue

            candidate_neighbors = set()
            for edge_id in self.adjacency.get(candidate_id, []):
                edge = self.edges.get(edge_id)
                if edge:
                    neighbor_id = edge.target_id if edge.source_id == candidate_id else edge.source_id
                    candidate_neighbors.add(neighbor_id)

            # Jaccard similarity
            intersection = len(target_neighbors & candidate_neighbors)
            union = len(target_neighbors | candidate_neighbors)

            if union > 0:
                similarity = intersection / union
                if similarity > 0:
                    similarities.append((self.nodes[candidate_id], similarity))

        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:limit]

    async def detect_communities(self) -> Dict[int, List[str]]:
        """Detect communities in the graph using label propagation"""

        # Simple label propagation
        labels = {node_id: i for i, node_id in enumerate(self.nodes.keys())}

        for _ in range(10):  # Iterations
            changed = False

            for node_id in self.nodes:
                neighbor_labels = []

                for edge_id in self.adjacency.get(node_id, []):
                    edge = self.edges.get(edge_id)
                    if edge:
                        neighbor_id = edge.target_id if edge.source_id == node_id else edge.source_id
                        neighbor_labels.append(labels[neighbor_id])

                if neighbor_labels:
                    # Most common label among neighbors
                    label_counts = defaultdict(int)
                    for label in neighbor_labels:
                        label_counts[label] += 1

                    new_label = max(label_counts, key=label_counts.get)
                    if labels[node_id] != new_label:
                        labels[node_id] = new_label
                        changed = True

            if not changed:
                break

        # Group by label
        communities = defaultdict(list)
        for node_id, label in labels.items():
            communities[label].append(node_id)

        return dict(communities)

    async def get_insights(self, node_id: str) -> Dict[str, Any]:
        """Generate insights about a node based on graph analysis"""

        if node_id not in self.nodes:
            return {}

        node = self.nodes[node_id]
        neighbors = await self.get_neighbors(node_id, direction="both")

        # Analyze connections by type
        connection_types = defaultdict(int)
        for _, edge in neighbors:
            connection_types[edge.edge_type.value] += 1

        # Find strongly connected nodes
        strong_connections = [
            (n.name, e.weight)
            for n, e in neighbors
            if e.weight > 0.7
        ]

        # Calculate centrality (degree centrality)
        total_edges = sum(len(edges) for edges in self.adjacency.values())
        degree_centrality = len(neighbors) / max(total_edges, 1)

        return {
            "node_id": node_id,
            "node_type": node.node_type.value,
            "name": node.name,
            "total_connections": len(neighbors),
            "connection_breakdown": dict(connection_types),
            "strong_connections": strong_connections[:5],
            "degree_centrality": degree_centrality,
            "source_platforms": node.source_platforms
        }

    def get_stats(self) -> Dict[str, Any]:
        """Get knowledge graph statistics"""

        return {
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges),
            "nodes_by_type": {
                t.value: len(ids)
                for t, ids in self.type_index.items()
            },
            "edges_by_type": self._count_edges_by_type(),
            "avg_connections_per_node": self._avg_connections()
        }

    def _count_edges_by_type(self) -> Dict[str, int]:
        """Count edges by type"""
        counts = defaultdict(int)
        for edge in self.edges.values():
            counts[edge.edge_type.value] += 1
        return dict(counts)

    def _avg_connections(self) -> float:
        """Calculate average connections per node"""
        if not self.nodes:
            return 0.0
        total = sum(len(edges) for edges in self.adjacency.values())
        return total / len(self.nodes)

    async def merge_duplicate_nodes(
        self,
        node_id_1: str,
        node_id_2: str,
        keep_id: str = None
    ) -> str:
        """Merge two nodes that represent the same entity"""

        if node_id_1 not in self.nodes or node_id_2 not in self.nodes:
            raise ValueError("Both nodes must exist")

        # Determine which to keep
        keep = keep_id or node_id_1
        remove = node_id_2 if keep == node_id_1 else node_id_1

        keep_node = self.nodes[keep]
        remove_node = self.nodes[remove]

        # Merge properties
        keep_node.properties.update(remove_node.properties)
        keep_node.source_platforms = list(set(
            keep_node.source_platforms + remove_node.source_platforms
        ))
        keep_node.updated_at = datetime.now()

        # Redirect edges
        for edge_id in list(self.adjacency.get(remove, [])):
            edge = self.edges.get(edge_id)
            if edge:
                if edge.source_id == remove:
                    edge.source_id = keep
                if edge.target_id == remove:
                    edge.target_id = keep
                self.adjacency[keep].append(edge_id)

        # Remove old node
        del self.nodes[remove]
        del self.adjacency[remove]
        self.type_index[remove_node.node_type].discard(remove)

        logger.info(f"Merged node {remove} into {keep}")
        return keep

    async def export_to_dict(self) -> Dict[str, Any]:
        """Export the entire graph to a dictionary"""

        return {
            "nodes": [
                {
                    "id": n.node_id,
                    "type": n.node_type.value,
                    "name": n.name,
                    "properties": n.properties,
                    "sources": n.source_platforms
                }
                for n in self.nodes.values()
            ],
            "edges": [
                {
                    "id": e.edge_id,
                    "type": e.edge_type.value,
                    "source": e.source_id,
                    "target": e.target_id,
                    "weight": e.weight,
                    "properties": e.properties
                }
                for e in self.edges.values()
            ]
        }
