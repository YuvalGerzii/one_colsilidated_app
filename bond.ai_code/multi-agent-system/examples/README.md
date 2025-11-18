# Multi-Agent System Examples

This directory contains examples demonstrating various features of the Multi-Agent System.

## Examples

### 1. Basic Usage (`basic_usage.py`)

Demonstrates fundamental system operations:
- Initializing the system
- Executing simple and complex tasks
- Retrieving results
- Viewing system metrics

**Run:**
```bash
python examples/basic_usage.py
```

### 2. Reinforcement Learning (`reinforcement_learning.py`)

Shows the RL capabilities:
- Training agents through multiple episodes
- Policy improvement over time
- Saving and loading learned policies
- Performance improvement tracking

**Run:**
```bash
python examples/reinforcement_learning.py
```

### 3. Custom Agents (`custom_agent.py`)

Demonstrates creating and using custom agents:
- Implementing specialized agent types
- Adding custom agents to the system
- Task delegation to custom agents

**Run:**
```bash
python examples/custom_agent.py
```

## Expected Output

Each example will:
1. Initialize the multi-agent system
2. Execute various tasks
3. Display results and metrics
4. Show agent states
5. Demonstrate learning (if applicable)

## Customization

You can modify these examples to:
- Create different task types
- Adjust system configuration
- Implement new agent types
- Test different scenarios

## Troubleshooting

If you encounter import errors:
```bash
# Make sure you're in the repository root
cd /path/to/multi-agent-system

# Install dependencies
pip install -r requirements.txt

# Run examples
python examples/basic_usage.py
```

## Next Steps

After running these examples, try:
1. Creating your own custom agents
2. Designing complex multi-step workflows
3. Training the system on domain-specific tasks
4. Integrating with external systems
