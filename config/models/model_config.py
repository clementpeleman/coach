from typing import Dict, List, Optional
from agno.models.openai import OpenAIChat
from agno.models.anthropic import Claude

class ModelConfig:
    """
    Centralized model configuration for different agents and use cases.

    This configuration optimizes model selection based on:
    - Task complexity and requirements
    - Response time needs
    - Cost considerations
    - Agent specialization

    Model selection strategy:
    - Claude Sonnet: Complex reasoning, analysis, and coordination
    - Claude Haiku: Fast responses, simple tasks, real-time interactions
    - GPT-4o: Structured data processing, JSON outputs, planning
    - GPT-4o-mini: Lightweight tasks, high-frequency operations
    """

    # Model instances for different use cases
    MODELS = {
        # Primary models for complex reasoning
        "claude_sonnet": Claude(
            id="claude-3-5-sonnet-20241022",
            name="Claude Sonnet",
            provider="Anthropic"
        ),

        # Fast response models
        "claude_haiku": Claude(
            id="claude-3-5-haiku-20241022",
            name="Claude Haiku",
            provider="Anthropic"
        ),

        # Structured output and planning
        "gpt4o": OpenAIChat(
            id="gpt-4o",
            name="GPT-4o",
            provider="OpenAI"
        ),

        # Lightweight and frequent operations
        "gpt4o_mini": OpenAIChat(
            id="gpt-4o-mini",
            name="GPT-4o Mini",
            provider="OpenAI"
        ),

        # Specialized for analysis tasks
        "gpt5_mini": OpenAIChat(
            id="gpt-5-mini",
            name="GPT-5 Mini",
            provider="OpenAI"
        )
    }

    # Agent-specific model assignments
    AGENT_MODELS = {
        # Core coordination - needs complex reasoning
        "coordinator": "claude_sonnet",

        # Onboarding - needs empathy and complex conversation
        "onboarding": "gpt4o",

        # Data sync - lightweight operations
        "data_sync": "gpt4o_mini",

        # Training planning - complex reasoning and creativity
        "training_planner": "claude_haiku",

        # Analysis - deep analytical capabilities
        "training_analyzer": "gpt4o",

        # Health analysis - medical expertise and reasoning
        "health_analyzer": "claude_sonnet",

        # Recovery - specialized knowledge application
        "recovery": "gpt4o_mini",

        # Nutrition - structured recommendations
        "nutrition": "gpt4o",

        # Goal management - tracking and motivation
        "goal_manager": "claude_haiku"
    }

    # Team-specific model configurations
    TEAM_MODELS = {
        "main_coaching_team": {
            "lead_model": "claude_sonnet",
            "fallback_model": "gpt4o"
        },
        "analysis_team": {
            "lead_model": "gpt4o",
            "fallback_model": "claude_sonnet"
        }
    }

    # Workflow-specific model configurations
    WORKFLOW_MODELS = {
        "daily_checkin": {
            "primary": "gpt4o_mini",  # Fast daily operations
            "analysis": "claude_sonnet"  # Deep analysis when needed
        },
        "onboarding": {
            "primary": "gpt4o",  # Structured conversation flow
            "assessment": "claude_sonnet"  # Complex evaluation
        }
    }

    @classmethod
    def get_model_for_agent(cls, agent_name: str):
        """
        Get the configured model for a specific agent
        """
        model_key = cls.AGENT_MODELS.get(agent_name, "claude_sonnet")
        return cls.MODELS.get(model_key)

    @classmethod
    def get_model_for_team(cls, team_name: str, role: str = "lead_model"):
        """
        Get the configured model for a team role
        """
        team_config = cls.TEAM_MODELS.get(team_name, {})
        model_key = team_config.get(role, "claude_sonnet")
        return cls.MODELS.get(model_key)

    @classmethod
    def get_model_for_workflow(cls, workflow_name: str, stage: str = "primary"):
        """
        Get the configured model for a workflow stage
        """
        workflow_config = cls.WORKFLOW_MODELS.get(workflow_name, {})
        model_key = workflow_config.get(stage, "claude_sonnet")
        return cls.MODELS.get(model_key)

    @classmethod
    def get_cost_optimized_model(cls, task_complexity: str):
        """
        Get model based on task complexity for cost optimization

        task_complexity: "simple", "moderate", "complex", "analytical"
        """
        complexity_mapping = {
            "simple": "gpt4o_mini",
            "moderate": "claude_haiku",
            "complex": "claude_sonnet",
            "analytical": "gpt4o"
        }

        model_key = complexity_mapping.get(task_complexity, "claude_sonnet")
        return cls.MODELS.get(model_key)

    @classmethod
    def get_response_time_optimized_model(cls, priority: str):
        """
        Get model optimized for response time requirements

        priority: "real_time", "fast", "standard", "deep_analysis"
        """
        priority_mapping = {
            "real_time": "gpt4o_mini",
            "fast": "claude_haiku",
            "standard": "gpt4o",
            "deep_analysis": "claude_sonnet"
        }

        model_key = priority_mapping.get(priority, "claude_sonnet")
        return cls.MODELS.get(model_key)