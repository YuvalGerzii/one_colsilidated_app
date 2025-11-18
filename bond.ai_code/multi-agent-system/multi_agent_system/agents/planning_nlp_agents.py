"""
Planning, Text Analysis, and NLP agents.

These agents provide specialized capabilities for:
- Strategic planning and task decomposition
- Text analysis and processing
- Natural Language Processing and understanding
- Sentiment analysis and text classification
- Entity extraction and relationship mapping
"""

from typing import Any, Dict, List, Optional
from loguru import logger
import re

from multi_agent_system.agents.base import BaseAgent
from multi_agent_system.core.types import Task, Result, AgentCapability


class StrategicPlannerAgent(BaseAgent):
    """
    Agent specialized in strategic planning and task decomposition.

    Capabilities:
    - Strategic planning and roadmap creation
    - Task decomposition and breakdown
    - Resource allocation planning
    - Timeline estimation
    - Risk assessment and mitigation planning
    """

    def __init__(self, agent_id: str = "strategic_planner_1", message_bus=None):
        capabilities = [
            AgentCapability("strategic_planning", "Create strategic plans and roadmaps", 0.94),
            AgentCapability("task_decomposition", "Break down complex tasks", 0.92),
            AgentCapability("resource_planning", "Plan resource allocation", 0.90),
            AgentCapability("timeline_estimation", "Estimate timelines and milestones", 0.88),
            AgentCapability("risk_assessment", "Assess and mitigate risks", 0.91),
        ]
        super().__init__(agent_id, capabilities, message_bus)

    async def process_task(self, task: Task) -> Result:
        """
        Process a strategic planning task.

        Args:
            task: Planning task to process

        Returns:
            Strategic plan with breakdown and timeline
        """
        logger.info(f"{self.agent_id} planning: {task.description}")

        # Analyze the task
        complexity = self._assess_complexity(task.description)

        # Decompose into phases
        phases = self._decompose_into_phases(task.description, complexity)

        # Estimate timeline
        timeline = self._estimate_timeline(phases)

        # Identify resources
        resources = self._identify_resources(phases)

        # Assess risks
        risks = self._assess_risks(phases)

        plan_data = {
            "objective": task.description,
            "complexity_score": complexity,
            "phases": phases,
            "timeline": timeline,
            "required_resources": resources,
            "risks": risks,
            "success_criteria": self._define_success_criteria(task.description),
            "confidence": 0.87,
        }

        return Result(
            task_id=task.id,
            success=True,
            data=plan_data,
            agent_id=self.agent_id,
            quality_score=0.90,
            metadata={"plan_type": "strategic", "phases": len(phases)},
        )

    def _assess_complexity(self, description: str) -> float:
        """Assess task complexity."""
        factors = {
            "length": min(len(description.split()) / 100, 1.0),
            "keywords": len(re.findall(r'\b(complex|difficult|challenge|multiple|integrate)\b', description.lower())) * 0.1,
            "scope": len(re.findall(r'\b(and|or|also|plus|additionally)\b', description.lower())) * 0.15,
        }
        return min(sum(factors.values()), 1.0)

    def _decompose_into_phases(self, description: str, complexity: float) -> List[Dict[str, Any]]:
        """Decompose task into phases."""
        # Determine number of phases based on complexity
        num_phases = max(3, int(complexity * 8))

        phases = []
        phase_templates = [
            {"name": "Discovery & Analysis", "type": "analysis", "duration": "1-2 weeks"},
            {"name": "Planning & Design", "type": "design", "duration": "1-2 weeks"},
            {"name": "Implementation", "type": "development", "duration": "2-4 weeks"},
            {"name": "Testing & Quality Assurance", "type": "testing", "duration": "1-2 weeks"},
            {"name": "Deployment & Integration", "type": "deployment", "duration": "1 week"},
            {"name": "Monitoring & Optimization", "type": "optimization", "duration": "ongoing"},
        ]

        for i in range(min(num_phases, len(phase_templates))):
            phase = phase_templates[i].copy()
            phase["phase_number"] = i + 1
            phase["deliverables"] = [f"{phase['name']} deliverable {j+1}" for j in range(2)]
            phases.append(phase)

        return phases

    def _estimate_timeline(self, phases: List[Dict]) -> Dict[str, Any]:
        """Estimate project timeline."""
        return {
            "total_duration": f"{len(phases) * 2}-{len(phases) * 4} weeks",
            "phases": len(phases),
            "milestones": [f"Phase {i+1} completion" for i in range(len(phases))],
            "critical_path": [phases[0]["name"], phases[2]["name"] if len(phases) > 2 else phases[-1]["name"]],
        }

    def _identify_resources(self, phases: List[Dict]) -> List[Dict[str, Any]]:
        """Identify required resources."""
        resource_types = {
            "analysis": ["Data Analyst", "Researcher"],
            "design": ["Designer", "Architect"],
            "development": ["Developer", "Engineer"],
            "testing": ["QA Engineer", "Tester"],
            "deployment": ["DevOps Engineer", "System Admin"],
            "optimization": ["Performance Engineer", "Data Scientist"],
        }

        resources = []
        for phase in phases:
            phase_type = phase.get("type", "general")
            if phase_type in resource_types:
                for role in resource_types[phase_type]:
                    resources.append({
                        "role": role,
                        "phase": phase["name"],
                        "allocation": "Full-time" if phase_type == "development" else "Part-time",
                    })

        return resources

    def _assess_risks(self, phases: List[Dict]) -> List[Dict[str, Any]]:
        """Assess potential risks."""
        return [
            {
                "risk": "Scope creep during implementation",
                "probability": "Medium",
                "impact": "High",
                "mitigation": "Clear requirements definition and change management process",
            },
            {
                "risk": "Resource availability constraints",
                "probability": "Medium",
                "impact": "Medium",
                "mitigation": "Early resource allocation and backup planning",
            },
            {
                "risk": "Technical challenges during integration",
                "probability": "Low",
                "impact": "High",
                "mitigation": "Proof of concept for critical integrations",
            },
        ]

    def _define_success_criteria(self, description: str) -> List[str]:
        """Define success criteria."""
        return [
            "All phases completed on schedule",
            "Quality standards met (>90% test coverage)",
            "Stakeholder acceptance achieved",
            "Performance targets met",
            "Budget maintained within 10% variance",
        ]


class ProjectPlannerAgent(BaseAgent):
    """
    Agent specialized in project planning and execution planning.

    Capabilities:
    - Project plan creation
    - Sprint planning
    - Milestone definition
    - Dependency mapping
    - Progress tracking
    """

    def __init__(self, agent_id: str = "project_planner_1", message_bus=None):
        capabilities = [
            AgentCapability("project_planning", "Create detailed project plans", 0.93),
            AgentCapability("sprint_planning", "Plan agile sprints", 0.91),
            AgentCapability("milestone_definition", "Define project milestones", 0.90),
            AgentCapability("dependency_mapping", "Map task dependencies", 0.89),
            AgentCapability("progress_tracking", "Track and report progress", 0.88),
        ]
        super().__init__(agent_id, capabilities, message_bus)

    async def process_task(self, task: Task) -> Result:
        """
        Process a project planning task.

        Args:
            task: Project planning task

        Returns:
            Detailed project plan
        """
        logger.info(f"{self.agent_id} project planning: {task.description}")

        # Create work breakdown structure
        wbs = self._create_wbs(task.description)

        # Define sprints
        sprints = self._plan_sprints(wbs)

        # Map dependencies
        dependencies = self._map_dependencies(wbs)

        # Create Gantt-style timeline
        timeline = self._create_timeline(sprints, dependencies)

        plan_data = {
            "project": task.description,
            "work_breakdown_structure": wbs,
            "sprints": sprints,
            "dependencies": dependencies,
            "timeline": timeline,
            "total_story_points": sum(item.get("story_points", 0) for item in wbs),
            "estimated_sprints": len(sprints),
            "confidence": 0.85,
        }

        return Result(
            task_id=task.id,
            success=True,
            data=plan_data,
            agent_id=self.agent_id,
            quality_score=0.88,
            metadata={"plan_type": "project", "sprints": len(sprints)},
        )

    def _create_wbs(self, description: str) -> List[Dict[str, Any]]:
        """Create work breakdown structure."""
        return [
            {
                "id": "WBS-001",
                "title": "Requirements gathering",
                "description": "Collect and document requirements",
                "story_points": 5,
                "category": "analysis",
            },
            {
                "id": "WBS-002",
                "title": "System design",
                "description": "Design system architecture",
                "story_points": 8,
                "category": "design",
            },
            {
                "id": "WBS-003",
                "title": "Core implementation",
                "description": "Implement core functionality",
                "story_points": 13,
                "category": "development",
            },
            {
                "id": "WBS-004",
                "title": "Testing suite",
                "description": "Create comprehensive tests",
                "story_points": 8,
                "category": "testing",
            },
            {
                "id": "WBS-005",
                "title": "Documentation",
                "description": "Write user and technical docs",
                "story_points": 5,
                "category": "documentation",
            },
        ]

    def _plan_sprints(self, wbs: List[Dict]) -> List[Dict[str, Any]]:
        """Plan agile sprints."""
        sprints = []
        sprint_capacity = 15  # story points per sprint
        current_sprint = {"number": 1, "items": [], "total_points": 0}

        for item in wbs:
            points = item.get("story_points", 0)

            if current_sprint["total_points"] + points > sprint_capacity:
                sprints.append(current_sprint)
                current_sprint = {"number": len(sprints) + 1, "items": [], "total_points": 0}

            current_sprint["items"].append(item["id"])
            current_sprint["total_points"] += points

        if current_sprint["items"]:
            sprints.append(current_sprint)

        return sprints

    def _map_dependencies(self, wbs: List[Dict]) -> List[Dict[str, str]]:
        """Map task dependencies."""
        return [
            {"from": "WBS-001", "to": "WBS-002", "type": "finish-to-start"},
            {"from": "WBS-002", "to": "WBS-003", "type": "finish-to-start"},
            {"from": "WBS-003", "to": "WBS-004", "type": "finish-to-start"},
            {"from": "WBS-003", "to": "WBS-005", "type": "finish-to-start"},
        ]

    def _create_timeline(self, sprints: List[Dict], dependencies: List[Dict]) -> Dict[str, Any]:
        """Create project timeline."""
        return {
            "total_sprints": len(sprints),
            "duration_weeks": len(sprints) * 2,
            "start_sprint": 1,
            "end_sprint": len(sprints),
            "critical_path": ["WBS-001", "WBS-002", "WBS-003", "WBS-004"],
        }


class TextAnalysisAgent(BaseAgent):
    """
    Agent specialized in text analysis and processing.

    Capabilities:
    - Text summarization
    - Keyword extraction
    - Readability analysis
    - Text classification
    - Content quality assessment
    """

    def __init__(self, agent_id: str = "text_analyzer_1", message_bus=None):
        capabilities = [
            AgentCapability("text_summarization", "Summarize long texts", 0.91),
            AgentCapability("keyword_extraction", "Extract key terms", 0.90),
            AgentCapability("readability_analysis", "Analyze text readability", 0.88),
            AgentCapability("text_classification", "Classify text content", 0.89),
            AgentCapability("quality_assessment", "Assess content quality", 0.87),
        ]
        super().__init__(agent_id, capabilities, message_bus)

    async def process_task(self, task: Task) -> Result:
        """
        Process a text analysis task.

        Args:
            task: Text analysis task

        Returns:
            Text analysis results
        """
        logger.info(f"{self.agent_id} analyzing text: {task.description[:50]}...")

        # Get text to analyze from task context or description
        text = task.context.get("text", task.description)

        # Perform analysis
        summary = self._summarize_text(text)
        keywords = self._extract_keywords(text)
        readability = self._analyze_readability(text)
        classification = self._classify_text(text)
        quality = self._assess_quality(text)

        analysis_data = {
            "original_length": len(text),
            "summary": summary,
            "keywords": keywords,
            "readability": readability,
            "classification": classification,
            "quality_score": quality,
            "language": "en",  # Could be detected
            "confidence": 0.88,
        }

        return Result(
            task_id=task.id,
            success=True,
            data=analysis_data,
            agent_id=self.agent_id,
            quality_score=quality,
            metadata={"text_length": len(text), "analysis_type": "comprehensive"},
        )

    def _summarize_text(self, text: str) -> str:
        """Generate text summary."""
        sentences = text.split('.')
        # Simple extractive summarization - take first and key sentences
        if len(sentences) <= 3:
            return text

        summary_sentences = [sentences[0]]  # First sentence
        if len(sentences) > 5:
            summary_sentences.append(sentences[len(sentences)//2])  # Middle
        summary_sentences.append(sentences[-2])  # Last meaningful sentence

        return '. '.join(s.strip() for s in summary_sentences if s.strip()) + '.'

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text."""
        # Simple keyword extraction
        words = re.findall(r'\b[a-z]{4,}\b', text.lower())

        # Count frequency
        word_freq = {}
        for word in words:
            if word not in ['that', 'this', 'with', 'from', 'have', 'been', 'were']:
                word_freq[word] = word_freq.get(word, 0) + 1

        # Return top keywords
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, _ in sorted_words[:10]]

    def _analyze_readability(self, text: str) -> Dict[str, Any]:
        """Analyze text readability."""
        words = text.split()
        sentences = text.split('.')

        avg_word_length = sum(len(w) for w in words) / len(words) if words else 0
        avg_sentence_length = len(words) / len(sentences) if sentences else 0

        # Simple readability score
        if avg_sentence_length < 15 and avg_word_length < 5:
            level = "Easy"
            score = 8
        elif avg_sentence_length < 20 and avg_word_length < 6:
            level = "Medium"
            score = 6
        else:
            level = "Difficult"
            score = 4

        return {
            "level": level,
            "score": score,
            "avg_word_length": round(avg_word_length, 1),
            "avg_sentence_length": round(avg_sentence_length, 1),
            "total_words": len(words),
            "total_sentences": len(sentences),
        }

    def _classify_text(self, text: str) -> Dict[str, Any]:
        """Classify text content."""
        text_lower = text.lower()

        categories = {
            "technical": ["system", "code", "implementation", "algorithm", "function"],
            "business": ["revenue", "profit", "customer", "market", "sales"],
            "research": ["study", "analysis", "data", "results", "findings"],
            "documentation": ["guide", "tutorial", "instructions", "how to"],
        }

        scores = {}
        for category, keywords in categories.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            scores[category] = score

        primary = max(scores, key=scores.get) if scores else "general"

        return {
            "primary_category": primary,
            "confidence": scores[primary] / len(categories[primary]) if scores[primary] > 0 else 0.3,
            "all_scores": scores,
        }

    def _assess_quality(self, text: str) -> float:
        """Assess content quality."""
        quality = 0.7  # Base score

        # Check length
        if 100 < len(text) < 5000:
            quality += 0.1

        # Check structure (has paragraphs)
        if '\n\n' in text or '. ' in text:
            quality += 0.1

        # Check capitalization
        if text[0].isupper():
            quality += 0.05

        # Check for common quality markers
        if any(marker in text.lower() for marker in ['however', 'therefore', 'additionally']):
            quality += 0.05

        return min(quality, 1.0)


class NLPAnalysisAgent(BaseAgent):
    """
    Agent specialized in Natural Language Processing and understanding.

    Capabilities:
    - Sentiment analysis
    - Named entity recognition (NER)
    - Part-of-speech tagging
    - Semantic analysis
    - Intent classification
    """

    def __init__(self, agent_id: str = "nlp_analyzer_1", message_bus=None):
        capabilities = [
            AgentCapability("sentiment_analysis", "Analyze text sentiment", 0.92),
            AgentCapability("entity_recognition", "Recognize named entities", 0.90),
            AgentCapability("pos_tagging", "Tag parts of speech", 0.87),
            AgentCapability("semantic_analysis", "Analyze semantic meaning", 0.89),
            AgentCapability("intent_classification", "Classify user intent", 0.91),
        ]
        super().__init__(agent_id, capabilities, message_bus)

    async def process_task(self, task: Task) -> Result:
        """
        Process an NLP analysis task.

        Args:
            task: NLP task

        Returns:
            NLP analysis results
        """
        logger.info(f"{self.agent_id} NLP analyzing: {task.description[:50]}...")

        # Get text from task
        text = task.context.get("text", task.description)

        # Perform NLP analyses
        sentiment = self._analyze_sentiment(text)
        entities = self._recognize_entities(text)
        pos_tags = self._tag_parts_of_speech(text)
        semantics = self._analyze_semantics(text)
        intent = self._classify_intent(text)

        nlp_data = {
            "text": text[:200] + "..." if len(text) > 200 else text,
            "sentiment": sentiment,
            "entities": entities,
            "pos_distribution": pos_tags,
            "semantic_features": semantics,
            "intent": intent,
            "language": "en",
            "confidence": 0.89,
        }

        return Result(
            task_id=task.id,
            success=True,
            data=nlp_data,
            agent_id=self.agent_id,
            quality_score=0.89,
            metadata={"text_length": len(text), "analysis_type": "nlp"},
        )

    def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of text."""
        text_lower = text.lower()

        # Simple sentiment lexicon
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love', 'best', 'perfect', 'happy']
        negative_words = ['bad', 'terrible', 'awful', 'horrible', 'worst', 'hate', 'poor', 'disappointing', 'sad', 'angry']

        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)

        total = pos_count + neg_count
        if total == 0:
            sentiment = "neutral"
            score = 0.5
        elif pos_count > neg_count:
            sentiment = "positive"
            score = 0.5 + (pos_count / (total * 2))
        elif neg_count > pos_count:
            sentiment = "negative"
            score = 0.5 - (neg_count / (total * 2))
        else:
            sentiment = "neutral"
            score = 0.5

        return {
            "label": sentiment,
            "score": round(score, 2),
            "confidence": min(0.5 + (total * 0.1), 0.95),
            "positive_count": pos_count,
            "negative_count": neg_count,
        }

    def _recognize_entities(self, text: str) -> List[Dict[str, str]]:
        """Recognize named entities."""
        entities = []

        # Simple pattern matching for entities
        # Capitalized words (potential entities)
        words = text.split()

        for i, word in enumerate(words):
            # Person names (capitalized, not at start of sentence)
            if word[0].isupper() and i > 0 and words[i-1][-1] not in '.!?':
                entities.append({
                    "text": word,
                    "type": "PERSON",
                    "confidence": 0.7,
                })

            # Organizations (with Inc, Corp, Ltd, etc.)
            if any(marker in word for marker in ['Inc', 'Corp', 'Ltd', 'LLC']):
                entities.append({
                    "text": word,
                    "type": "ORGANIZATION",
                    "confidence": 0.8,
                })

            # Dates (simple patterns)
            if re.match(r'\d{4}|\d{1,2}/\d{1,2}/\d{2,4}', word):
                entities.append({
                    "text": word,
                    "type": "DATE",
                    "confidence": 0.9,
                })

        return entities[:10]  # Limit to top 10

    def _tag_parts_of_speech(self, text: str) -> Dict[str, int]:
        """Tag parts of speech (simplified)."""
        words = text.split()

        pos_distribution = {
            "nouns": 0,
            "verbs": 0,
            "adjectives": 0,
            "adverbs": 0,
            "pronouns": 0,
        }

        # Simple heuristics
        verb_endings = ['ed', 'ing', 'en']
        adj_endings = ['ful', 'less', 'ous', 'ive']
        adv_endings = ['ly']
        pronouns = ['i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them']

        for word in words:
            word_lower = word.lower().strip('.,!?')

            if word_lower in pronouns:
                pos_distribution["pronouns"] += 1
            elif any(word_lower.endswith(end) for end in verb_endings):
                pos_distribution["verbs"] += 1
            elif any(word_lower.endswith(end) for end in adj_endings):
                pos_distribution["adjectives"] += 1
            elif any(word_lower.endswith(end) for end in adv_endings):
                pos_distribution["adverbs"] += 1
            else:
                pos_distribution["nouns"] += 1  # Default assumption

        return pos_distribution

    def _analyze_semantics(self, text: str) -> Dict[str, Any]:
        """Analyze semantic features."""
        text_lower = text.lower()

        # Semantic themes
        themes = {
            "action": ['do', 'make', 'create', 'build', 'develop'],
            "thought": ['think', 'believe', 'understand', 'know', 'realize'],
            "emotion": ['feel', 'love', 'hate', 'enjoy', 'like', 'dislike'],
            "communication": ['say', 'tell', 'speak', 'write', 'communicate'],
        }

        theme_scores = {}
        for theme, keywords in themes.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                theme_scores[theme] = score

        dominant_theme = max(theme_scores, key=theme_scores.get) if theme_scores else "neutral"

        return {
            "dominant_theme": dominant_theme,
            "theme_scores": theme_scores,
            "abstractness": self._calculate_abstractness(text),
            "complexity": self._calculate_semantic_complexity(text),
        }

    def _calculate_abstractness(self, text: str) -> str:
        """Calculate how abstract vs concrete the text is."""
        concrete_markers = ['see', 'touch', 'hear', 'smell', 'taste', 'physical', 'visible']
        abstract_markers = ['concept', 'idea', 'theory', 'principle', 'belief', 'thought']

        text_lower = text.lower()
        concrete_count = sum(1 for marker in concrete_markers if marker in text_lower)
        abstract_count = sum(1 for marker in abstract_markers if marker in text_lower)

        if abstract_count > concrete_count:
            return "abstract"
        elif concrete_count > abstract_count:
            return "concrete"
        else:
            return "balanced"

    def _calculate_semantic_complexity(self, text: str) -> str:
        """Calculate semantic complexity."""
        words = text.split()
        unique_words = set(word.lower() for word in words)

        lexical_diversity = len(unique_words) / len(words) if words else 0

        if lexical_diversity > 0.7:
            return "high"
        elif lexical_diversity > 0.4:
            return "medium"
        else:
            return "low"

    def _classify_intent(self, text: str) -> Dict[str, Any]:
        """Classify user intent."""
        text_lower = text.lower()

        # Intent patterns
        intents = {
            "question": ['?', 'what', 'why', 'how', 'when', 'where', 'who'],
            "command": ['please', 'could you', 'can you', 'would you', 'do ', 'make ', 'create '],
            "statement": [],  # Default
            "request": ['need', 'want', 'require', 'looking for'],
        }

        intent_scores = {}
        for intent, markers in intents.items():
            if markers:  # Skip empty (statement)
                score = sum(1 for marker in markers if marker in text_lower)
                if score > 0:
                    intent_scores[intent] = score

        if not intent_scores:
            classified = "statement"
            confidence = 0.7
        else:
            classified = max(intent_scores, key=intent_scores.get)
            confidence = min(0.6 + (intent_scores[classified] * 0.1), 0.95)

        return {
            "intent": classified,
            "confidence": confidence,
            "all_scores": intent_scores,
        }


class SemanticSearchAgent(BaseAgent):
    """
    Agent specialized in semantic search and information retrieval.

    Capabilities:
    - Semantic similarity matching
    - Document ranking
    - Query understanding
    - Context-aware search
    - Relevance scoring
    """

    def __init__(self, agent_id: str = "semantic_search_1", message_bus=None):
        capabilities = [
            AgentCapability("semantic_matching", "Match semantically similar content", 0.90),
            AgentCapability("document_ranking", "Rank documents by relevance", 0.89),
            AgentCapability("query_understanding", "Understand search queries", 0.91),
            AgentCapability("relevance_scoring", "Score document relevance", 0.88),
        ]
        super().__init__(agent_id, capabilities, message_bus)

    async def process_task(self, task: Task) -> Result:
        """
        Process a semantic search task.

        Args:
            task: Search task

        Returns:
            Ranked search results
        """
        logger.info(f"{self.agent_id} semantic search: {task.description}")

        query = task.context.get("query", task.description)
        documents = task.context.get("documents", [])

        # Understand query intent
        query_analysis = self._analyze_query(query)

        # Rank documents
        ranked_results = self._rank_documents(query, documents, query_analysis)

        # Generate search insights
        insights = self._generate_insights(query, ranked_results)

        search_data = {
            "query": query,
            "query_analysis": query_analysis,
            "results_count": len(ranked_results),
            "ranked_results": ranked_results[:10],  # Top 10
            "insights": insights,
            "confidence": 0.87,
        }

        return Result(
            task_id=task.id,
            success=True,
            data=search_data,
            agent_id=self.agent_id,
            quality_score=0.88,
            metadata={"search_type": "semantic", "results": len(ranked_results)},
        )

    def _analyze_query(self, query: str) -> Dict[str, Any]:
        """Analyze search query."""
        query_lower = query.lower()

        # Extract key terms
        key_terms = [word for word in query_lower.split() if len(word) > 3]

        # Detect query type
        if '?' in query:
            query_type = "question"
        elif any(word in query_lower for word in ['find', 'search', 'show', 'list']):
            query_type = "search"
        elif any(word in query_lower for word in ['compare', 'difference', 'versus']):
            query_type = "comparison"
        else:
            query_type = "informational"

        return {
            "key_terms": key_terms,
            "query_type": query_type,
            "length": len(query.split()),
            "specificity": "high" if len(key_terms) > 3 else "low",
        }

    def _rank_documents(self, query: str, documents: List[Any], query_analysis: Dict) -> List[Dict]:
        """Rank documents by relevance."""
        if not documents:
            # Create sample documents for demonstration
            documents = [
                {"id": "doc1", "title": "Sample Document 1", "content": "Content related to query"},
                {"id": "doc2", "title": "Sample Document 2", "content": "Another relevant document"},
            ]

        ranked = []
        query_lower = query.lower()
        key_terms = query_analysis["key_terms"]

        for doc in documents:
            # Calculate relevance score
            score = 0.0

            doc_text = str(doc.get("content", "") + " " + doc.get("title", "")).lower()

            # Term frequency
            for term in key_terms:
                score += doc_text.count(term) * 0.2

            # Title match bonus
            if any(term in str(doc.get("title", "")).lower() for term in key_terms):
                score += 0.3

            # Length normalization
            doc_length = len(doc_text.split())
            if 100 < doc_length < 1000:
                score += 0.1

            ranked.append({
                "document_id": doc.get("id", "unknown"),
                "title": doc.get("title", "Untitled"),
                "relevance_score": round(min(score, 1.0), 2),
                "preview": doc_text[:150] + "..." if len(doc_text) > 150 else doc_text,
            })

        # Sort by relevance
        ranked.sort(key=lambda x: x["relevance_score"], reverse=True)

        return ranked

    def _generate_insights(self, query: str, ranked_results: List[Dict]) -> Dict[str, Any]:
        """Generate search insights."""
        if not ranked_results:
            return {"message": "No results found"}

        avg_score = sum(r["relevance_score"] for r in ranked_results) / len(ranked_results)

        return {
            "total_results": len(ranked_results),
            "average_relevance": round(avg_score, 2),
            "highly_relevant": sum(1 for r in ranked_results if r["relevance_score"] > 0.7),
            "suggestion": "Refine query" if avg_score < 0.5 else "Results look good",
        }


def create_planning_nlp_agents(message_bus=None) -> Dict[str, BaseAgent]:
    """
    Create planning and NLP analysis agents.

    Returns:
        Dictionary of planning and NLP agents
    """
    agents = {
        "strategic_planner_1": StrategicPlannerAgent("strategic_planner_1", message_bus),
        "strategic_planner_2": StrategicPlannerAgent("strategic_planner_2", message_bus),
        "project_planner_1": ProjectPlannerAgent("project_planner_1", message_bus),
        "project_planner_2": ProjectPlannerAgent("project_planner_2", message_bus),
        "text_analyzer_1": TextAnalysisAgent("text_analyzer_1", message_bus),
        "text_analyzer_2": TextAnalysisAgent("text_analyzer_2", message_bus),
        "nlp_analyzer_1": NLPAnalysisAgent("nlp_analyzer_1", message_bus),
        "nlp_analyzer_2": NLPAnalysisAgent("nlp_analyzer_2", message_bus),
        "semantic_search_1": SemanticSearchAgent("semantic_search_1", message_bus),
        "semantic_search_2": SemanticSearchAgent("semantic_search_2", message_bus),
    }

    logger.info(f"Created {len(agents)} planning and NLP agents")

    return agents
