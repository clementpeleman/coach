from agno.workflow import Workflow, Step, Condition, Loop
from agno.models.openai import OpenAIChat

from agents.specialized.onboarding import OnboardingAgent
from agents.specialized.data_sync import DataSyncAgent
from agents.specialized.training_planner import TrainingPlannerAgent
from agents.specialized.goal_manager import GoalManagerAgent

class OnboardingWorkflow:
    """
    Complete user onboarding workflow that:
    - Welcomes new users and explains system capabilities
    - Conducts comprehensive health and fitness assessment
    - Sets up Garmin device integration and data sync
    - Establishes SMART goals and timelines
    - Creates initial personalized training plan
    - Schedules first check-in and follow-up

    Workflow phases:
    1. Welcome and Introduction
    2. Health & Fitness Assessment
    3. Goal Setting and Prioritization
    4. Device Setup and Data Integration
    5. Initial Plan Creation
    6. System Orientation and Next Steps

    Assessment areas:
    - Current fitness level and exercise history
    - Health conditions and limitations
    - Available time and equipment
    - Motivation factors and preferences
    - Goals and timeline expectations
    - Support system and accountability

    Outputs:
    - Complete user profile with preferences
    - Established baseline metrics
    - SMART goal framework
    - Personalized training plan
    - Nutrition guidance framework
    - Follow-up schedule
    """

    def __init__(self, knowledge_base=None):
        self.onboarding = OnboardingAgent()
        self.data_sync = DataSyncAgent()
        self.training_planner = TrainingPlannerAgent(knowledge_base)
        self.goal_manager = GoalManagerAgent()

        # Define workflow steps
        self.welcome_step = Step(
            name="welcome_user",
            description="Welcome new user and explain system capabilities",
            executor=self.onboarding.agent,
            input_schema={
                "user_name": "string",
                "referral_source": "string",
                "initial_interest": "string"
            }
        )

        def conduct_assessment_loop():
            """
            Iterative assessment process until complete
            """
            return Loop(
                name="assessment_loop",
                description="Iterative health and fitness assessment",
                steps=[
                    Step(
                        name="ask_assessment_questions",
                        description="Ask assessment questions based on current progress",
                        executor=self.onboarding.agent
                    ),
                    Step(
                        name="process_responses",
                        description="Process and validate user responses",
                        executor=self.onboarding.agent
                    )
                ],
                condition=Condition(
                    name="assessment_complete",
                    description="Check if assessment is complete",
                    condition_function=lambda x: x.get("assessment_complete", False)
                )
            )

        self.assessment_loop = conduct_assessment_loop()

        self.goal_setting_step = Step(
            name="set_goals",
            description="Establish SMART goals with user",
            executor=self.goal_manager.agent,
            input_schema={
                "user_profile": "object",
                "user_aspirations": "array",
                "constraints": "object"
            }
        )

        self.device_setup_step = Step(
            name="setup_garmin",
            description="Guide through Garmin device setup and first sync",
            executor=self.data_sync.agent,
            input_schema={
                "user_id": "string",
                "device_type": "string",
                "user_preferences": "object"
            }
        )

        self.create_plan_step = Step(
            name="create_initial_plan",
            description="Create first personalized training plan",
            executor=self.training_planner.agent,
            input_schema={
                "user_profile": "object",
                "goals": "array",
                "constraints": "object"
            }
        )

        def setup_follow_up(input_data):
            """
            Schedule follow-up sessions and set expectations
            """
            # Schedule first check-in
            # Set up notification preferences
            # Provide system orientation
            # Create support resources list
            pass

        self.follow_up_step = Step(
            name="setup_follow_up",
            description="Schedule follow-up and provide orientation",
            executor=setup_follow_up,
            input_schema={
                "user_profile": "object",
                "training_plan": "object",
                "preferences": "object"
            }
        )

        # Create the workflow
        self.workflow = Workflow(
            name="User Onboarding",
            description="Complete new user onboarding and setup process",
            steps=[
                self.welcome_step,
                self.assessment_loop,
                self.goal_setting_step,
                self.device_setup_step,
                self.create_plan_step,
                self.follow_up_step
            ],
            add_datetime_to_context=True
        )

    async def execute_onboarding(self, user_data: dict):
        """
        Execute complete onboarding workflow for new user
        """
        workflow_input = {
            "user_data": user_data,
            "onboarding_date": "today",
            "system_version": "2.0"
        }

        result = await self.workflow.run(workflow_input)
        return result

    async def resume_onboarding(self, user_id: str, step_name: str):
        """
        Resume interrupted onboarding from specific step
        """
        pass