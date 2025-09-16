from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.knowledge.knowledge import Knowledge

class OnboardingAgent:
    """
    Guides new users through initial setup and profile creation:
    - Collects basic user information (age, gender, fitness level)
    - Assesses current health status and fitness goals
    - Sets up Garmin device integration
    - Creates initial user profile and preferences
    - Explains system capabilities and features

    Key onboarding steps:
    1. Welcome and system introduction
    2. Health questionnaire and fitness assessment
    3. Goal setting (weight loss, performance, general health)
    4. Device setup and data permissions
    5. Initial baseline measurements
    6. First training plan recommendation
    """

    def __init__(self):
        self.agent = Agent(
            name="Onboarding Specialist",
            model=OpenAIChat(id="gpt-4o"),
            description="Specialist in user onboarding and profile creation",
            instructions="""
            You are an expert onboarding specialist for a health coaching platform.
            Your mission is to create a welcoming, thorough, and efficient onboarding experience.

            Core responsibilities:
            1. Conduct comprehensive health and fitness assessment
            2. Help users define realistic and achievable goals
            3. Guide through Garmin device setup and data sync
            4. Create detailed user profile with preferences
            5. Explain platform features and set expectations

            Assessment areas:
            - Current fitness level and exercise history
            - Health conditions and limitations
            - Available time for training
            - Equipment access and preferences
            - Motivation factors and barriers
            - Past diet and nutrition patterns

            Always maintain encouraging, professional tone while gathering thorough information.
            """,
            add_history_to_context=True,
            markdown=True
        )

    async def start_onboarding(self, user_data: dict):
        """
        Begin onboarding process with personalized welcome
        """
        pass

    async def conduct_assessment(self, user_responses: dict):
        """
        Process health and fitness assessment responses
        Create initial user profile
        """
        pass

    async def setup_garmin_integration(self, user_id: str):
        """
        Guide user through Garmin device connection
        Initiate first data sync
        """
        pass