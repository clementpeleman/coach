from agno.team import Team
from agno.models.openai import OpenAIChat
from agno.models.anthropic import Claude

from agents.core.coordinator import CoordinatorAgent
from agents.specialized.onboarding import OnboardingAgent
from agents.specialized.data_sync import DataSyncAgent
from agents.specialized.training_planner import TrainingPlannerAgent
from agents.specialized.training_analyzer import TrainingAnalyzerAgent
from agents.specialized.health_analyzer import HealthAnalyzerAgent
from agents.specialized.recovery import RecoveryAgent
from agents.specialized.nutrition import NutritionAgent
from agents.specialized.goal_manager import GoalManagerAgent

class MainCoachingTeam:
    """
    Complete coaching team with all specialized agents working together.

    This team provides comprehensive health and fitness coaching by combining:
    - Coordinator for query routing and response integration
    - All specialized agents for domain expertise
    - Collaborative decision making for complex scenarios
    - Holistic approach to user health and fitness

    Team workflow:
    1. Coordinator receives user input and determines relevant agents
    2. Specialized agents contribute domain-specific insights
    3. Coordinator synthesizes responses into coherent guidance
    4. Continuous learning from agent interactions and user feedback

    Use cases:
    - Complete health and fitness coaching
    - Complex multi-domain questions
    - Long-term user relationship management
    - Comprehensive progress tracking and adaptation
    """

    def __init__(self, knowledge_base=None):

        # Initialize all specialized agents
        self.coordinator = CoordinatorAgent()
        self.onboarding = OnboardingAgent()
        self.data_sync = DataSyncAgent()
        self.training_planner = TrainingPlannerAgent(knowledge_base)
        self.training_analyzer = TrainingAnalyzerAgent(knowledge_base)
        self.health_analyzer = HealthAnalyzerAgent()
        self.recovery = RecoveryAgent()
        self.nutrition = NutritionAgent()
        self.goal_manager = GoalManagerAgent()

        # Create the main coaching team
        team_members = [
            self.coordinator.agent,
            self.onboarding.agent,
            self.data_sync.agent,
            self.training_planner.agent,
            self.training_analyzer.agent,
            self.health_analyzer.agent,
            self.recovery.agent,
            self.nutrition.agent,
            self.goal_manager.agent
        ]

        self.team = Team(
            name="Complete Health Coaching Team",
            members=team_members,
            description="Comprehensive health and fitness coaching with all specialized agents",
        )

        # Set team instructions
        self.team.instructions = """
            This is the main coaching team providing comprehensive health and fitness guidance.

            Team coordination:
            - The Coordinator agent leads and routes queries appropriately
            - Each specialist contributes domain expertise when relevant
            - Responses are integrated for coherent, holistic guidance
            - All agents collaborate to ensure consistent messaging

            Team priorities:
            1. User safety and health as primary concern
            2. Evidence-based recommendations and guidance
            3. Personalized approach based on individual data
            4. Sustainable lifestyle and training practices
            5. Continuous adaptation based on progress and feedback

            Communication style:
            - Supportive and encouraging tone
            - Clear, actionable guidance
            - Educational context when helpful
            - Professional yet approachable
            """

    async def handle_user_query(self, user_input: str, user_context: dict):
        """
        Process user query through the complete coaching team
        """
        pass

    async def daily_check_in(self, user_id: str):
        """
        Perform daily health and training check-in
        """
        pass