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
from agno.os import AgentOS

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

def initialize_system():
    """
    Initialize Health Coach AI System components and return AgentOS instance
    """
    logger.info("Initializing Health Coach AI System...")

    # Initialize database
    logger.info("Setting up database...")
    db_config.initialize_database()

    from agno.db.sqlite import SqliteDb
    database = SqliteDb(
        db_file="./data/health_coach.db",
        session_table="coaching_sessions"
    )
    logger.info("Database initialized successfully")

    # Initialize knowledge base
    logger.info("Setting up knowledge base...")
    from agno.vectordb.lancedb import LanceDb, SearchType
    from agno.knowledge.embedder.openai import OpenAIEmbedder
    from agno.knowledge.knowledge import Knowledge

    knowledge_base = Knowledge(
        vector_db=LanceDb(
            uri="./data/knowledge",
            table_name="health_coaching_knowledge",
            search_type=SearchType.hybrid,
            embedder=OpenAIEmbedder(id="text-embedding-3-small")
        )
    )
    logger.info("Knowledge base initialized (content loading skipped for now)")

    # Initialize teams
    logger.info("Setting up AI agent teams...")
    main_team = MainCoachingTeam(knowledge_base)
    analysis_team = AnalysisTeam(knowledge_base)
    logger.info("AI teams initialized successfully")

    # Create individual agents list for AgentOS
    agents = []

    # Add agents from main coaching team
    agents.extend([
        main_team.coordinator.agent,
        main_team.onboarding.agent,
        main_team.data_sync.agent,
        main_team.training_planner.agent,
        main_team.training_analyzer.agent,
        main_team.health_analyzer.agent,
        main_team.recovery.agent,
        main_team.nutrition.agent,
        main_team.goal_manager.agent
    ])

    # Create teams list for AgentOS
    teams = [
        main_team.team,
        analysis_team.team
    ]

    # Create AgentOS instance
    agent_os = AgentOS(
        os_id="health-coach-ai",
        description="Comprehensive AI-powered health coaching system with specialized agents",
        agents=agents,
        teams=teams,
        # workflows=[]  # Will be added later when API is stable
    )

    logger.info("System initialization completed successfully")
    return agent_os

# Initialize AgentOS system at module level
agent_os = initialize_system()

# Create FastAPI app at module level for AgentOS serve method
app = agent_os.get_app()

def main():
    """
    Main application entry point
    """
    parser = argparse.ArgumentParser(description="Health Coach AI System")
    parser.add_argument("--mode", choices=["api"], default="api",
                        help="Application mode (only API mode supported with AgentOS)")
    parser.add_argument("--host", default="0.0.0.0", help="API server host")
    parser.add_argument("--port", type=int, default=8000, help="API server port")

    args = parser.parse_args()

    # Serve using AgentOS built-in serve method
    try:
        logger.info(f"Starting AgentOS API server on {args.host}:{args.port}")

        agent_os.serve(
            app=f"{__name__}:app",
            host=args.host,
            port=args.port,
            reload=False  # Don't use reload with MCP tools
        )

    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()