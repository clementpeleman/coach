"""
Health Coach AI System - Main Application Entry Point

A comprehensive AI-powered health coaching system built with Agno v2.0
that provides personalized fitness training, health monitoring, and
nutrition guidance through specialized AI agents.

Features:
- Multi-agent AI coaching system
- Garmin device integration
- Personalized training plans
- Health metrics analysis
- Recovery optimization
- Nutrition guidance
- Goal tracking and adaptation

Usage:
    python main.py [--mode chat|api|worker] [--agent AGENT_NAME] [--workflow WORKFLOW_NAME]

Examples:
    # Start AgentOS API server
    python main.py --mode api

    # Interactive chat with main coaching team
    python main.py --mode chat

    # Run specific workflow
    python main.py --mode workflow --workflow onboarding

    # Chat with specific agent
    python main.py --mode chat --agent training_planner
"""

import asyncio
import argparse
import logging
import sys
from typing import Optional, Dict, Any

# Import Agno components
from agno.db.sqlite import SqliteDb
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge

# Import local components
from teams.main_coaching_team import MainCoachingTeam
from teams.analysis_team import AnalysisTeam
from workflows.daily_checkin import DailyCheckinWorkflow
from workflows.onboarding import OnboardingWorkflow
from config.database_config import db_config
from config.models.model_config import ModelConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class HealthCoachSystem:
    """
    Main application class that orchestrates the health coaching system
    """

    def __init__(self):
        self.knowledge_base = None
        self.main_team = None
        self.analysis_team = None
        self.workflows = {}
        self.database = None

    async def initialize(self):
        """
        Initialize all system components
        """
        logger.info("Initializing Health Coach AI System...")

        try:
            # Initialize database
            await self._initialize_database()

            # Initialize knowledge base
            await self._initialize_knowledge_base()

            # Initialize teams
            await self._initialize_teams()

            # Initialize workflows
            await self._initialize_workflows()

            logger.info("System initialization completed successfully")

        except Exception as e:
            logger.error(f"System initialization failed: {e}")
            raise

    async def _initialize_database(self):
        """
        Initialize database connection and schema
        """
        logger.info("Setting up database...")

        # Create database engine and tables
        db_config.initialize_database()

        # Create SQLite database for session management
        self.database = SqliteDb(
            db_file="./data/health_coach.db",
            session_table="coaching_sessions"
        )

        logger.info("Database initialized successfully")

    async def _initialize_knowledge_base(self):
        """
        Initialize knowledge base with training methodologies and health information
        """
        logger.info("Setting up knowledge base...")

        # Create vector database for knowledge storage
        self.knowledge_base = Knowledge(
            vector_db=LanceDb(
                uri="./data/knowledge",
                table_name="health_coaching_knowledge",
                search_type=SearchType.hybrid,
                embedder=OpenAIEmbedder(id="text-embedding-3-small")
            )
        )

        # Load training methodologies and health information
        # This would be populated with actual content in production
        knowledge_sources = [
            {
                "name": "Exercise Physiology Principles",
                "content": "Core principles of exercise physiology, training adaptation, and periodization..."
            },
            {
                "name": "Sports Nutrition Guidelines",
                "content": "Evidence-based sports nutrition recommendations for performance and health..."
            },
            {
                "name": "Recovery Science",
                "content": "Scientific principles of recovery, sleep optimization, and stress management..."
            },
            {
                "name": "Health Monitoring Best Practices",
                "content": "Best practices for health metric interpretation and risk assessment..."
            }
        ]

        # Add content to knowledge base
        for source in knowledge_sources:
            await self.knowledge_base.add_content_async(
                name=source["name"],
                content=source["content"]
            )

        logger.info("Knowledge base initialized with training content")

    async def _initialize_teams(self):
        """
        Initialize AI agent teams
        """
        logger.info("Setting up AI agent teams...")

        # Initialize main coaching team
        self.main_team = MainCoachingTeam(self.knowledge_base)

        # Initialize analysis team
        self.analysis_team = AnalysisTeam(self.knowledge_base)

        logger.info("AI teams initialized successfully")

    async def _initialize_workflows(self):
        """
        Initialize system workflows
        """
        logger.info("Setting up workflows...")

        # Initialize workflows
        self.workflows = {
            "daily_checkin": DailyCheckinWorkflow(self.knowledge_base),
            "onboarding": OnboardingWorkflow(self.knowledge_base)
        }

        logger.info("Workflows initialized successfully")

    async def run_chat_mode(self, agent_name: Optional[str] = None):
        """
        Run interactive chat mode
        """
        logger.info("Starting chat mode...")

        if agent_name:
            # Chat with specific agent
            agent = getattr(self.main_team, agent_name, None)
            if agent:
                print(f"\nChatting with {agent_name.replace('_', ' ').title()} Agent")
                print("Type 'exit' to quit\n")

                while True:
                    user_input = input("You: ").strip()
                    if user_input.lower() == 'exit':
                        break

                    try:
                        response = await agent.agent.arun(user_input)
                        print(f"\n{agent_name.replace('_', ' ').title()}: {response}\n")
                    except Exception as e:
                        print(f"Error: {e}\n")
            else:
                print(f"Agent '{agent_name}' not found")
        else:
            # Chat with main coaching team
            print("\nHealth Coach AI - Interactive Chat")
            print("Type 'exit' to quit\n")

            while True:
                user_input = input("You: ").strip()
                if user_input.lower() == 'exit':
                    break

                try:
                    response = await self.main_team.handle_user_query(
                        user_input,
                        {"user_id": "demo_user", "session_id": "demo_session"}
                    )
                    print(f"\nCoach: {response}\n")
                except Exception as e:
                    print(f"Error: {e}\n")

    async def run_workflow_mode(self, workflow_name: str, **kwargs):
        """
        Run specific workflow
        """
        logger.info(f"Running workflow: {workflow_name}")

        workflow = self.workflows.get(workflow_name)
        if not workflow:
            logger.error(f"Workflow '{workflow_name}' not found")
            return

        try:
            if workflow_name == "onboarding":
                result = await workflow.execute_onboarding({
                    "user_name": kwargs.get("user_name", "Demo User"),
                    "email": kwargs.get("email", "demo@example.com")
                })
            elif workflow_name == "daily_checkin":
                result = await workflow.execute_daily_checkin(
                    kwargs.get("user_id", "demo_user"),
                    {"check_date": "today"}
                )
            else:
                logger.error(f"Unknown workflow execution pattern for '{workflow_name}'")
                return

            logger.info(f"Workflow '{workflow_name}' completed successfully")
            print(f"\nWorkflow Result:\n{result}")

        except Exception as e:
            logger.error(f"Workflow '{workflow_name}' failed: {e}")

    async def run_api_mode(self, host: str = "0.0.0.0", port: int = 8000):
        """
        Run AgentOS API server
        """
        logger.info(f"Starting AgentOS API server on {host}:{port}")

        # This would integrate with AgentOS for production deployment
        # For now, we'll implement a basic FastAPI server placeholder

        try:
            from fastapi import FastAPI
            import uvicorn

            app = FastAPI(title="Health Coach AI API", version="1.0.0")

            @app.get("/health")
            async def health_check():
                return {"status": "healthy", "service": "health-coach-ai"}

            @app.post("/chat")
            async def chat_endpoint(message: dict):
                user_input = message.get("message", "")
                user_context = message.get("context", {})

                response = await self.main_team.handle_user_query(user_input, user_context)
                return {"response": response}

            @app.post("/workflow/{workflow_name}")
            async def workflow_endpoint(workflow_name: str, data: dict):
                await self.run_workflow_mode(workflow_name, **data)
                return {"status": "completed", "workflow": workflow_name}

            uvicorn.run(app, host=host, port=port)

        except ImportError:
            logger.error("FastAPI not installed. Install with: pip install fastapi uvicorn")
        except Exception as e:
            logger.error(f"API server failed: {e}")

async def main():
    """
    Main application entry point
    """
    parser = argparse.ArgumentParser(description="Health Coach AI System")
    parser.add_argument("--mode", choices=["chat", "api", "workflow"], default="chat",
                        help="Application mode")
    parser.add_argument("--agent", help="Specific agent for chat mode")
    parser.add_argument("--workflow", help="Workflow to run")
    parser.add_argument("--host", default="0.0.0.0", help="API server host")
    parser.add_argument("--port", type=int, default=8000, help="API server port")
    parser.add_argument("--user-name", help="User name for workflows")
    parser.add_argument("--user-id", help="User ID for workflows")

    args = parser.parse_args()

    # Initialize system
    system = HealthCoachSystem()
    await system.initialize()

    # Run in specified mode
    try:
        if args.mode == "chat":
            await system.run_chat_mode(args.agent)
        elif args.mode == "api":
            await system.run_api_mode(args.host, args.port)
        elif args.mode == "workflow":
            if not args.workflow:
                logger.error("--workflow parameter required for workflow mode")
                sys.exit(1)
            await system.run_workflow_mode(
                args.workflow,
                user_name=args.user_name,
                user_id=args.user_id
            )
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())