"""
LLM-Based Agent System
Uses free LLMs (Ollama, Llama.cpp) for intelligent analysis
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import json
import subprocess
import time


@dataclass
class AgentMessage:
    """Message exchanged between agents"""
    sender: str
    recipient: str
    content: str
    message_type: str  # query, response, analysis, recommendation
    timestamp: float
    context: Dict[str, Any]


class LLMAgent:
    """
    Base class for LLM-powered agents
    Uses free, local LLMs via Ollama or similar
    """

    def __init__(
        self,
        agent_id: str,
        role: str,
        model: str = "llama2",  # Default to Llama 2
        temperature: float = 0.5,
        max_tokens: int = 2000
    ):
        """
        Initialize LLM agent

        Args:
            agent_id: Unique agent identifier
            role: Agent role (analyst, predictor, psychologist, etc.)
            model: LLM model to use
            temperature: Sampling temperature
            max_tokens: Maximum response tokens
        """
        self.agent_id = agent_id
        self.role = role
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.conversation_history = []
        self.knowledge_base = {}

    def generate_response(self, prompt: str, context: Optional[Dict] = None) -> str:
        """
        Generate response using LLM

        Args:
            prompt: Input prompt
            context: Additional context

        Returns:
            LLM response text
        """
        # Build full prompt with role and context
        full_prompt = self._build_prompt(prompt, context)

        try:
            # Try to use Ollama (free, local LLM)
            response = self._call_ollama(full_prompt)
        except Exception as e:
            # Fallback to rule-based response if LLM not available
            print(f"Warning: LLM not available ({e}), using fallback logic")
            response = self._fallback_response(prompt, context)

        # Store in conversation history
        self.conversation_history.append({
            'prompt': prompt,
            'response': response,
            'timestamp': time.time()
        })

        return response

    def _build_prompt(self, prompt: str, context: Optional[Dict]) -> str:
        """Build complete prompt with role and context"""
        role_prompts = {
            'analyst': "You are a financial analyst specializing in extreme event analysis. Provide data-driven insights.",
            'predictor': "You are a market prediction specialist. Forecast likely outcomes with probability estimates.",
            'psychologist': "You are a behavioral economist analyzing human responses to crises. Focus on psychological patterns.",
            'economist': "You are an economist evaluating economic impacts. Consider macro and micro effects.",
            'strategist': "You are a strategic advisor. Develop actionable plans and risk mitigation strategies.",
            'coordinator': "You are coordinating multiple expert opinions. Synthesize insights and resolve conflicts."
        }

        system_prompt = role_prompts.get(self.role, "You are an expert analyst.")

        # Add context if provided
        context_str = ""
        if context:
            context_str = f"\n\nContext:\n{json.dumps(context, indent=2)}\n"

        return f"{system_prompt}{context_str}\n\nQuery: {prompt}\n\nResponse:"

    def _call_ollama(self, prompt: str) -> str:
        """
        Call Ollama API for LLM inference

        Args:
            prompt: Full prompt

        Returns:
            LLM response
        """
        # Construct Ollama command
        # This assumes Ollama is installed: https://ollama.ai/
        cmd = [
            'ollama',
            'run',
            self.model,
            prompt
        ]

        # Call Ollama
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            raise RuntimeError(f"Ollama failed: {result.stderr}")

        return result.stdout.strip()

    def _fallback_response(self, prompt: str, context: Optional[Dict]) -> str:
        """
        Fallback response when LLM is not available
        Uses rule-based logic specific to agent role
        """
        if self.role == 'analyst':
            return self._analyst_fallback(prompt, context)
        elif self.role == 'predictor':
            return self._predictor_fallback(prompt, context)
        elif self.role == 'psychologist':
            return self._psychologist_fallback(prompt, context)
        elif self.role == 'economist':
            return self._economist_fallback(prompt, context)
        elif self.role == 'strategist':
            return self._strategist_fallback(prompt, context)
        else:
            return "Analysis complete. LLM service unavailable - using baseline assessment."

    def _analyst_fallback(self, prompt: str, context: Optional[Dict]) -> str:
        """Analyst fallback logic"""
        if not context:
            return "Insufficient data for analysis."

        event_type = context.get('event_type', 'unknown')
        severity = context.get('severity', 3)

        return f"""Analysis of {event_type} event:

Severity Assessment: {severity}/5
Event Type: {event_type}
Geographic Scope: {context.get('geographic_scope', 'unknown')}

Key Observations:
1. This is a {'severe' if severity >= 4 else 'moderate' if severity >= 3 else 'minor'} event
2. Expected market impact: {'High' if severity >= 4 else 'Medium' if severity >= 3 else 'Low'}
3. Data quality: {context.get('data_quality', 'medium')}

Recommendation: {'Immediate action required' if severity >= 4 else 'Monitor closely'}"""

    def _predictor_fallback(self, prompt: str, context: Optional[Dict]) -> str:
        """Predictor fallback logic"""
        if not context:
            return "Insufficient data for prediction."

        severity = context.get('severity', 3)
        impact = -10 * (severity / 3.0)

        return f"""Market Prediction:

Expected Impact: {impact:.1f}%
Confidence: {70 if context.get('data_quality') == 'high' else 60}%
Timeline: {'Rapid (1-7 days)' if severity >= 4 else 'Gradual (1-4 weeks)'}

Probability Distribution:
- Best case: {impact * 0.5:.1f}%
- Base case: {impact:.1f}%
- Worst case: {impact * 1.5:.1f}%

Recovery Timeline: {90 * severity // 3} days"""

    def _psychologist_fallback(self, prompt: str, context: Optional[Dict]) -> str:
        """Psychologist fallback logic"""
        event_type = context.get('event_type', '') if context else ''

        if 'pandemic' in event_type or 'health' in event_type:
            dominant_emotion = 'fear'
        elif 'economic' in event_type or 'crisis' in event_type:
            dominant_emotion = 'anxiety'
        elif 'terror' in event_type or 'cyber' in event_type:
            dominant_emotion = 'fear and anger'
        else:
            dominant_emotion = 'uncertainty'

        return f"""Behavioral Psychology Analysis:

Dominant Emotion: {dominant_emotion}
Expected Behaviors:
- Risk aversion will increase significantly
- Flight to safety assets (gold, bonds)
- Herd behavior likely
- Panic buying of essentials possible

Social Dynamics:
- Information seeking will spike
- Social media amplification high
- Trust in authority {'high' if dominant_emotion == 'fear' else 'declining'}

Economic Behaviors:
- Reduced discretionary spending
- Increased savings rate
- Delayed major purchases"""

    def _economist_fallback(self, prompt: str, context: Optional[Dict]) -> str:
        """Economist fallback logic"""
        return """Economic Impact Assessment:

Primary Channels:
1. Demand Shock - Reduced consumer spending
2. Supply Disruption - Production constraints
3. Financial Stress - Credit tightening
4. Confidence Effects - Investment delays

Sectoral Impact:
- Most Vulnerable: Travel, hospitality, discretionary retail
- Defensive: Utilities, healthcare, consumer staples
- Potential Beneficiaries: Technology, delivery services

Policy Response Required:
- Monetary: Rate cuts, liquidity provision
- Fiscal: Targeted support, stimulus measures"""

    def _strategist_fallback(self, prompt: str, context: Optional[Dict]) -> str:
        """Strategist fallback logic"""
        severity = context.get('severity', 3) if context else 3

        if severity >= 4:
            urgency = "IMMEDIATE"
            actions = [
                "Reduce equity exposure by 30-50%",
                "Increase cash position to 20-30%",
                "Implement hedging strategies",
                "Review all risk exposures"
            ]
        else:
            urgency = "ELEVATED"
            actions = [
                "Increase defensive positioning",
                "Add safe haven assets",
                "Monitor positions daily",
                "Prepare contingency plans"
            ]

        return f"""Strategic Recommendations:

Urgency Level: {urgency}

Immediate Actions:
{chr(10).join(f'{i+1}. {action}' for i, action in enumerate(actions))}

Risk Management:
- Update VaR models
- Stress test portfolio
- Review liquidity

Opportunities:
- Quality assets at discounts
- Counter-cyclical positioning
- Long-term value creation"""

    def analyze(self, task: str, data: Dict) -> Dict:
        """
        Perform analysis task

        Args:
            task: Description of analysis task
            data: Input data

        Returns:
            Analysis results
        """
        prompt = f"Task: {task}\n\nPlease analyze this situation and provide detailed insights."

        response = self.generate_response(prompt, data)

        return {
            'agent_id': self.agent_id,
            'role': self.role,
            'task': task,
            'analysis': response,
            'timestamp': time.time()
        }

    def send_message(self, recipient: str, content: str, message_type: str, context: Dict) -> AgentMessage:
        """
        Send message to another agent

        Args:
            recipient: Recipient agent ID
            content: Message content
            message_type: Type of message
            context: Message context

        Returns:
            AgentMessage object
        """
        return AgentMessage(
            sender=self.agent_id,
            recipient=recipient,
            content=content,
            message_type=message_type,
            timestamp=time.time(),
            context=context
        )

    def receive_message(self, message: AgentMessage) -> str:
        """
        Process received message

        Args:
            message: Received message

        Returns:
            Response text
        """
        # Generate response based on message content and context
        prompt = f"Message from {message.sender}:\n{message.content}\n\nHow should I respond?"

        return self.generate_response(prompt, message.context)
