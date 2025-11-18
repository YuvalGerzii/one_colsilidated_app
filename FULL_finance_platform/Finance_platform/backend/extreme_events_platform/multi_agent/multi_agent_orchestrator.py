"""
Multi-Agent Orchestrator
Coordinates multiple LLM agents for comprehensive analysis
"""

from typing import Dict, List, Optional, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from .llm_agent import LLMAgent, AgentMessage


class MultiAgentOrchestrator:
    """
    Orchestrates multiple LLM agents to analyze extreme events
    Enables agent communication, consensus building, and conflict resolution
    """

    def __init__(self, model: str = "llama2"):
        """
        Initialize multi-agent system

        Args:
            model: LLM model to use for all agents
        """
        self.model = model
        self.agents: Dict[str, LLMAgent] = {}
        self.message_queue: List[AgentMessage] = []
        self.analysis_results = {}

        # Initialize specialized agents
        self._initialize_agents()

    def _initialize_agents(self):
        """Create specialized agent instances"""
        agent_configs = {
            'analyst': {'role': 'analyst', 'temperature': 0.3},
            'predictor': {'role': 'predictor', 'temperature': 0.5},
            'psychologist': {'role': 'psychologist', 'temperature': 0.6},
            'economist': {'role': 'economist', 'temperature': 0.4},
            'strategist': {'role': 'strategist', 'temperature': 0.7},
            'coordinator': {'role': 'coordinator', 'temperature': 0.5}
        }

        for agent_id, config in agent_configs.items():
            self.agents[agent_id] = LLMAgent(
                agent_id=agent_id,
                role=config['role'],
                model=self.model,
                temperature=config['temperature']
            )

    def analyze_event_multi_agent(self, event_data: Dict) -> Dict:
        """
        Analyze event using all agents in parallel

        Args:
            event_data: Event characteristics

        Returns:
            Comprehensive multi-agent analysis
        """
        print("\n" + "="*80)
        print("MULTI-AGENT ANALYSIS INITIATED")
        print("="*80)

        # Phase 1: Parallel independent analysis
        print("\n[Phase 1] Independent Agent Analysis...")
        independent_analyses = self._parallel_analysis(event_data)

        # Phase 2: Agent communication and refinement
        print("\n[Phase 2] Agent Communication & Cross-Validation...")
        refined_analyses = self._agent_communication_phase(independent_analyses, event_data)

        # Phase 3: Consensus building
        print("\n[Phase 3] Consensus Building...")
        consensus = self._build_consensus(refined_analyses, event_data)

        # Phase 4: Conflict resolution
        print("\n[Phase 4] Conflict Resolution...")
        final_analysis = self._resolve_conflicts(consensus, event_data)

        print("\n[Complete] Multi-Agent Analysis Complete")
        print("="*80 + "\n")

        return {
            'independent_analyses': independent_analyses,
            'refined_analyses': refined_analyses,
            'consensus': consensus,
            'final_analysis': final_analysis,
            'agent_contributions': self._calculate_contributions(independent_analyses),
            'confidence_metrics': self._calculate_confidence_metrics(refined_analyses)
        }

    def _parallel_analysis(self, event_data: Dict) -> Dict[str, Dict]:
        """
        Run all agents in parallel for initial analysis

        Args:
            event_data: Event data

        Returns:
            Dictionary of agent_id -> analysis results
        """
        results = {}

        # Define tasks for each agent
        tasks = {
            'analyst': "Analyze the event data and identify key patterns, severity, and historical comparisons.",
            'predictor': "Predict market outcomes, including impact magnitude, timeline, and probability distributions.",
            'psychologist': "Analyze expected human behavioral responses including emotions, risk tolerance, and collective behavior.",
            'economist': "Evaluate economic impacts across sectors, supply/demand effects, and policy implications.",
            'strategist': "Develop actionable strategies for risk mitigation and opportunity capture."
        }

        # Run agents in parallel
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_agent = {
                executor.submit(self.agents[agent_id].analyze, task, event_data): agent_id
                for agent_id, task in tasks.items()
            }

            for future in as_completed(future_to_agent):
                agent_id = future_to_agent[future]
                try:
                    result = future.result()
                    results[agent_id] = result
                    print(f"  ✓ {agent_id.capitalize()} completed")
                except Exception as e:
                    print(f"  ✗ {agent_id.capitalize()} failed: {e}")
                    results[agent_id] = {'error': str(e)}

        return results

    def _agent_communication_phase(self, analyses: Dict[str, Dict], event_data: Dict) -> Dict[str, Dict]:
        """
        Allow agents to communicate and refine their analyses

        Args:
            analyses: Initial analyses from each agent
            event_data: Original event data

        Returns:
            Refined analyses after inter-agent communication
        """
        refined = {}

        # Each agent reviews other agents' analyses and refines their own
        for agent_id, agent in self.agents.items():
            if agent_id == 'coordinator':
                continue

            # Get perspectives from other agents
            other_perspectives = {
                other_id: analysis.get('analysis', '')
                for other_id, analysis in analyses.items()
                if other_id != agent_id and 'error' not in analysis
            }

            # Ask agent to refine their analysis considering others
            refinement_prompt = f"""
            You provided this initial analysis:
            {analyses.get(agent_id, {}).get('analysis', 'N/A')}

            Other experts have provided these perspectives:
            {chr(10).join(f'{expert}: {perspective[:200]}...' for expert, perspective in other_perspectives.items())}

            Please refine your analysis considering these other viewpoints.
            Identify areas of agreement, disagreement, and additional insights.
            """

            refined_analysis = agent.generate_response(refinement_prompt, event_data)

            refined[agent_id] = {
                'original': analyses.get(agent_id, {}),
                'refined': refined_analysis,
                'timestamp': time.time()
            }

            print(f"  ✓ {agent_id.capitalize()} refined")

        return refined

    def _build_consensus(self, refined_analyses: Dict[str, Dict], event_data: Dict) -> Dict:
        """
        Build consensus from refined analyses

        Args:
            refined_analyses: Refined analyses from all agents
            event_data: Event data

        Returns:
            Consensus analysis
        """
        coordinator = self.agents['coordinator']

        # Compile all refined analyses
        all_analyses = "\n\n".join([
            f"=== {agent_id.upper()} ===\n{analysis.get('refined', 'N/A')}"
            for agent_id, analysis in refined_analyses.items()
        ])

        consensus_prompt = f"""
        You are coordinating a multi-expert panel analyzing an extreme event.

        Event Type: {event_data.get('event_type', 'Unknown')}
        Severity: {event_data.get('severity', 'Unknown')}/5

        Expert Analyses:
        {all_analyses}

        Please synthesize these analyses into a consensus view:
        1. Areas of strong agreement
        2. Key insights from each expert
        3. Areas of disagreement (if any)
        4. Overall consensus prediction
        5. Confidence level in consensus
        """

        consensus_text = coordinator.generate_response(consensus_prompt, event_data)

        return {
            'consensus_text': consensus_text,
            'contributing_agents': list(refined_analyses.keys()),
            'timestamp': time.time()
        }

    def _resolve_conflicts(self, consensus: Dict, event_data: Dict) -> Dict:
        """
        Resolve any conflicts in the consensus

        Args:
            consensus: Consensus analysis
            event_data: Event data

        Returns:
            Final reconciled analysis
        """
        coordinator = self.agents['coordinator']

        resolution_prompt = f"""
        The expert panel has reached this consensus:
        {consensus.get('consensus_text', '')}

        Please provide a final, actionable summary including:
        1. Clear prediction with confidence levels
        2. Primary risks and opportunities
        3. Recommended actions (prioritized)
        4. Key uncertainties to monitor
        5. Overall assessment (bullish/bearish/neutral)
        """

        final_analysis = coordinator.generate_response(resolution_prompt, event_data)

        # Extract structured data from text (simple parsing)
        return {
            'final_summary': final_analysis,
            'timestamp': time.time(),
            'event_type': event_data.get('event_type'),
            'severity': event_data.get('severity')
        }

    def _calculate_contributions(self, analyses: Dict[str, Dict]) -> Dict:
        """Calculate each agent's contribution quality"""
        contributions = {}

        for agent_id, analysis in analyses.items():
            if 'error' in analysis:
                contributions[agent_id] = {'quality': 0, 'status': 'failed'}
            else:
                # Simple quality metric based on analysis length and detail
                analysis_text = analysis.get('analysis', '')
                quality = min(1.0, len(analysis_text) / 500)  # Normalized to 0-1

                contributions[agent_id] = {
                    'quality': quality,
                    'status': 'success',
                    'length': len(analysis_text)
                }

        return contributions

    def _calculate_confidence_metrics(self, refined_analyses: Dict[str, Dict]) -> Dict:
        """Calculate confidence metrics for the analysis"""
        successful_agents = sum(
            1 for analysis in refined_analyses.values()
            if 'refined' in analysis
        )

        total_agents = len(refined_analyses)
        agreement_rate = successful_agents / total_agents if total_agents > 0 else 0

        return {
            'successful_agents': successful_agents,
            'total_agents': total_agents,
            'agreement_rate': agreement_rate,
            'overall_confidence': agreement_rate * 0.8 + 0.2  # Baseline 20% + agreement boost
        }

    def simulate_agent_debate(
        self,
        topic: str,
        event_data: Dict,
        rounds: int = 2
    ) -> List[Dict]:
        """
        Simulate a debate between agents

        Args:
            topic: Debate topic
            event_data: Event context
            rounds: Number of debate rounds

        Returns:
            List of debate exchanges
        """
        debate_log = []

        # Select debating agents (analyst vs predictor, psychologist vs economist)
        debates = [
            ('analyst', 'predictor', 'What will be the market impact?'),
            ('psychologist', 'economist', 'How will people react vs how should they react?')
        ]

        for agent1_id, agent2_id, question in debates:
            agent1 = self.agents[agent1_id]
            agent2 = self.agents[agent2_id]

            debate_log.append({
                'debate': f'{agent1_id} vs {agent2_id}',
                'question': question,
                'rounds': []
            })

            position1 = ""
            position2 = ""

            for round_num in range(rounds):
                # Agent 1's turn
                prompt1 = f"Debate question: {question}\n"
                if round_num > 0:
                    prompt1 += f"\nOpponent's position: {position2}\nRespond and refine your position."
                else:
                    prompt1 += "\nState your position."

                position1 = agent1.generate_response(prompt1, event_data)

                # Agent 2's turn
                prompt2 = f"Debate question: {question}\nOpponent's position: {position1}\n"
                if round_num > 0:
                    prompt2 += "Respond and refine your position."
                else:
                    prompt2 += "State your counter-position."

                position2 = agent2.generate_response(prompt2, event_data)

                debate_log[-1]['rounds'].append({
                    'round': round_num + 1,
                    f'{agent1_id}_position': position1,
                    f'{agent2_id}_position': position2
                })

        return debate_log

    def query_agent(self, agent_id: str, question: str, context: Dict) -> str:
        """
        Query a specific agent

        Args:
            agent_id: Agent to query
            question: Question to ask
            context: Context data

        Returns:
            Agent's response
        """
        if agent_id not in self.agents:
            return f"Error: Agent '{agent_id}' not found"

        agent = self.agents[agent_id]
        return agent.generate_response(question, context)

    def get_specialized_perspective(
        self,
        agent_role: str,
        analysis_focus: str,
        event_data: Dict
    ) -> Dict:
        """
        Get specialized perspective from a specific type of agent

        Args:
            agent_role: Role of agent (analyst, predictor, etc.)
            analysis_focus: What to focus analysis on
            event_data: Event data

        Returns:
            Specialized analysis
        """
        agent_id = agent_role.lower()

        if agent_id not in self.agents:
            return {'error': f'No agent with role {agent_role}'}

        agent = self.agents[agent_id]

        prompt = f"Focus Area: {analysis_focus}\n\nProvide your specialized {agent_role} perspective on this event."

        response = agent.generate_response(prompt, event_data)

        return {
            'agent_role': agent_role,
            'focus': analysis_focus,
            'perspective': response,
            'timestamp': time.time()
        }
