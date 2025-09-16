# Health Coach AI System

A comprehensive AI-powered health coaching system built with Agno v2.0 that provides personalized fitness training, health monitoring, and nutrition guidance through specialized AI agents.

## 🎯 Features

### Core Coaching Capabilities
- **Personalized Training Plans**: AI-generated workout plans based on goals, fitness level, and constraints
- **Health Metrics Analysis**: Comprehensive monitoring of HRV, sleep, stress, and recovery metrics
- **Nutrition Guidance**: Evidence-based dietary recommendations and meal planning
- **Recovery Optimization**: Intelligent rest and recovery protocols for optimal adaptation
- **Goal Management**: SMART goal setting with adaptive progress tracking

### AI Agent System
- **Coordinator Agent**: Main orchestrator for seamless user experience
- **Specialized Agents**: 8 domain-expert agents for comprehensive coaching
- **Team Collaboration**: Multi-agent teams for complex scenarios
- **Workflow Automation**: Automated daily check-ins and onboarding processes

### Data Integration
- **Garmin Integration**: Complete sync with Garmin Connect API
- **Health Monitoring**: Real-time health metrics from wearable devices
- **Performance Analytics**: Detailed workout analysis and insights
- **Trend Analysis**: Long-term health and fitness trend monitoring

## 🏗️ Architecture

### Multi-Agent System
```
Coordinator Agent (Claude Sonnet)
├── Onboarding Agent (GPT-4o)
├── Data Sync Agent (GPT-4o Mini)
├── Training Planner Agent (Claude Haiku)
├── Training Analyzer Agent (GPT-4o)
├── Health Analyzer Agent (Claude Sonnet)
├── Recovery Agent (GPT-4o Mini)
├── Nutrition Agent (GPT-4o)
└── Goal Manager Agent (Claude Haiku)
```

### Team Configurations
- **Main Coaching Team**: Complete health coaching with all agents
- **Analysis Team**: Specialized performance and health analysis

### Workflows
- **Daily Check-in**: Automated health assessment and recommendations
- **Onboarding**: Complete new user setup and profile creation

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Garmin Developer Account (for API access)
- OpenAI API Key
- Anthropic API Key

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd coach
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Environment setup**
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

4. **Initialize database**
```bash
python -c "from config.database_config import db_config; db_config.initialize_database()"
```

### Running the System

#### Interactive Chat Mode
```bash
# Chat with complete coaching team
python main.py --mode chat

# Chat with specific agent
python main.py --mode chat --agent training_planner
```

#### API Server Mode
```bash
# Start AgentOS API server
python main.py --mode api --host 0.0.0.0 --port 8000
```

#### Workflow Execution
```bash
# Run onboarding workflow
python main.py --mode workflow --workflow onboarding --user-name "John Doe"

# Run daily check-in
python main.py --mode workflow --workflow daily_checkin --user-id "user123"
```

## 📁 Project Structure

```
coach/
├── agents/                 # AI agent implementations
│   ├── core/              # Core agents (coordinator)
│   └── specialized/       # Specialized domain agents
├── teams/                 # Agent team configurations
├── workflows/             # Automated workflow definitions
├── tools/                 # Utilities and integrations
│   ├── garmin/           # Garmin API integration
│   └── health/           # Health calculation utilities
├── database/              # Data models and repositories
│   └── models/           # SQLAlchemy models
├── config/                # Configuration and settings
│   ├── models/           # AI model configurations
│   └── prompts/          # Agent prompt templates
├── ui/                    # User interface components
├── tests/                 # Test suites
├── docs/                  # Documentation
├── main.py                # Application entry point
└── requirements.txt       # Python dependencies
```

## 🔧 Configuration

### Model Configuration
The system uses a hybrid approach with different AI models optimized for specific tasks:

- **Claude Sonnet**: Complex reasoning and coordination
- **Claude Haiku**: Fast responses and simple tasks
- **GPT-4o**: Structured data processing and planning
- **GPT-4o Mini**: Lightweight operations

### Database Configuration
Supports multiple database backends:
- **SQLite**: Development and testing
- **PostgreSQL**: Production deployment
- **Memory**: Unit testing

### Garmin Integration
Configure Garmin Connect API integration:
```python
GARMIN_CLIENT_ID = "your_client_id"
GARMIN_CLIENT_SECRET = "your_client_secret"
GARMIN_REDIRECT_URI = "your_redirect_uri"
```

## 🎨 Usage Examples

### Basic Health Coaching
```python
from teams.main_coaching_team import MainCoachingTeam

# Initialize coaching team
team = MainCoachingTeam()

# User interaction
response = await team.handle_user_query(
    "I want to start running but I'm a complete beginner",
    {"user_id": "user123", "fitness_level": "beginner"}
)
```

### Workout Analysis
```python
from teams.analysis_team import AnalysisTeam

# Initialize analysis team
analysis_team = AnalysisTeam()

# Analyze workout
analysis = await analysis_team.analyze_workout_performance(
    workout_data=garmin_activity_data,
    user_context=user_profile
)
```

### Custom Workflows
```python
from workflows.daily_checkin import DailyCheckinWorkflow

# Run daily check-in
workflow = DailyCheckinWorkflow()
result = await workflow.execute_daily_checkin("user123", {})
```

## 🔒 Security & Privacy

- **Data Privacy**: All health data processed locally
- **Secure Storage**: Encrypted database storage
- **API Security**: Authentication and rate limiting
- **GDPR Compliant**: User data control and deletion

## 🧪 Testing

Run the test suite:
```bash
# Run all tests
pytest

# Run specific test categories
pytest tests/agents/
pytest tests/workflows/
pytest tests/integration/

# Run with coverage
pytest --cov=agents --cov=teams --cov=workflows
```

## 📈 Monitoring & Analytics

### Health Metrics
- Heart Rate Variability (HRV) tracking
- Sleep quality analysis
- Stress level monitoring
- Recovery assessment

### Performance Analytics
- Training load quantification
- Progress tracking
- Goal achievement rates
- User engagement metrics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [docs/](docs/)
- **Issues**: GitHub Issues
- **Discord**: Join our Discord community
- **Email**: support@healthcoach-ai.com

## 🗺️ Roadmap

### Phase 1 (Current)
- ✅ Core agent system implementation
- ✅ Garmin data integration
- ✅ Basic coaching workflows
- 🔄 AgentOS integration

### Phase 2 (Q2 2024)
- 📱 Mobile app integration
- 💬 WhatsApp chat interface
- 🎯 Advanced goal tracking
- 📊 Enhanced analytics dashboard

### Phase 3 (Q3 2024)
- 🤖 Predictive health insights
- 👥 Social features and challenges
- 🏥 Healthcare provider integration
- 🌍 Multi-language support

---

Built with ❤️ using [Agno v2.0](https://docs.agno.com) - The fastest framework for building AI agents.