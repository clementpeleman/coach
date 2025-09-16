from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.models.anthropic import Claude

class CoordinatorAgent:
    """
    Main orchestrator agent that:
    - Routes user queries to appropriate specialized agents
    - Provides unified user experience
    - Manages conversation flow and context
    - Coordinates responses from multiple agents
    - Handles fallback scenarios when agents can't help

    Core responsibilities:
    - Query classification and routing
    - Response aggregation and formatting
    - Session management and context preservation
    - Error handling and graceful degradation
    """

    def __init__(self):
        self.agent = Agent(
            name="Health Coach Coordinator",
            model=Claude(id="claude-3-5-sonnet-20241022"),
            description="Main orchestrator for health coaching system",
            instructions="""
            You are the main coordinator for a comprehensive health coaching system.
            Your role is to:
            1. Understand user intent and route to appropriate specialized agents
            2. Provide cohesive responses that integrate multiple agent outputs
            3. Maintain conversation context and user state
            4. Ensure smooth user experience across all interactions

            Available specialized agents:
            - Onboarding: New user setup and profile creation
            - Data Sync: Garmin data integration and synchronization
            - Training Planner: Personalized workout plan creation
            - Training Analyzer: Post-workout analysis and insights
            - Health Analyzer: Health metrics monitoring (HRV, sleep, stress)
            - Recovery: Rest and recovery management
            - Nutrition: Dietary advice and meal planning
            - Goal Manager: Progress tracking and goal adjustment
            """,
            add_history_to_context=True,
            add_datetime_to_context=True,
            markdown=True
        )

    async def route_query(self, user_input: str, user_context: dict):
        """
        Analyze user input and determine which agents to engage
        Returns routing decisions and coordination strategy
        """
        pass

    async def coordinate_response(self, agent_responses: dict):
        """
        Aggregate and format responses from multiple agents
        Ensure coherent and helpful final response
        """
        pass