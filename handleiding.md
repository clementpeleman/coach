# Health Coach AI System - Handleiding

## 📋 Overzicht
Dit is een uitgebreid AI-gedreven health coaching systeem gebouwd met Agno v2.0 dat gepersonaliseerde fitness training, gezondheidsmonitoring en voedingsadvies biedt via gespecialiseerde AI-agenten.

## 🏗️ Architectuur
Het systeem is gebaseerd op een **multi-agent architectuur** met:
- **Coordinator Agent** (Claude Sonnet) - hoofdorchestrator
- **8 gespecialiseerde agenten** voor verschillende domeinen
- **Teams** - samenwerking tussen agents voor complexe scenario's
- **Workflows** - geautomatiseerde processen

### AI Agent Structuur
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

## 📁 Project Structuur

| Directory | Beschrijving |
|-----------|-------------|
| `agents/` | AI agent implementaties |
| `├── core/` | Kern agents (coordinator) |
| `└── specialized/` | Gespecialiseerde domain agents |
| `teams/` | Agent team configuraties |
| `workflows/` | Geautomatiseerde workflow definities |
| `tools/` | Utilities en integraties |
| `├── garmin/` | Garmin API integratie |
| `└── health/` | Gezondheidsberekeningen |
| `database/` | Data modellen en repositories |
| `config/` | Configuratie en instellingen |
| `ui/` | User interface componenten |
| `main.py` | Applicatie startpunt |

## 🚀 Installatie & Setup

### Vereisten
- Python 3.9+
- Garmin Developer Account
- OpenAI API Key
- Anthropic API Key

### Stappen
1. **Dependencies installeren:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment configureren:**
   ```bash
   cp .env.example .env
   # Bewerk .env met je API keys
   ```

3. **Database initialiseren:**
   ```bash
   python -c "from config.database_config import db_config; db_config.initialize_database()"
   ```

## 🎯 Gebruik

### Modi
| Mode | Commando | Beschrijving |
|------|----------|-------------|
| Chat | `python main.py --mode chat` | Interactieve chat met coaching team |
| API | `python main.py --mode api` | Start AgentOS API server |
| Workflow | `python main.py --mode workflow --workflow onboarding` | Voer specifieke workflow uit |

### Voorbeelden
```bash
# Chat met specifieke agent
python main.py --mode chat --agent training_planner

# API server starten
python main.py --mode api --host 0.0.0.0 --port 8000

# Dagelijkse check-in workflow
python main.py --mode workflow --workflow daily_checkin --user-id "user123"
```

## 🔧 Configuratie

### AI Modellen
- **Claude Sonnet**: Complexe redenering en coördinatie
- **Claude Haiku**: Snelle responses en eenvoudige taken
- **GPT-4o**: Gestructureerde dataverwerking
- **GPT-4o Mini**: Lichtgewicht operaties

### Database
- **SQLite**: Development/testing
- **PostgreSQL**: Productie
- **Memory**: Unit testing

### Belangrijke Environment Variables
```env
# AI API Keys
OPENAI_API_KEY=your_key
ANTHROPIC_API_KEY=your_key

# Database
DEV_DATABASE_URL=sqlite:///./data/coach_dev.db

# Garmin Integration
GARMIN_CLIENT_ID=your_id
GARMIN_CLIENT_SECRET=your_secret
```

## 🧪 Testing
```bash
# Alle tests
pytest

# Specifieke tests
pytest tests/agents/
pytest tests/workflows/

# Met coverage
pytest --cov=agents --cov=teams --cov=workflows
```

## 🔍 Key Features

### Core Functionaliteit
- **Gepersonaliseerde trainingsplannen**
- **Gezondheidsmetrieken analyse** (HRV, slaap, stress)
- **Voedingsadvies**
- **Recovery optimalisatie**
- **SMART goal management**

### Integraties
- **Garmin Connect API** - volledige sync
- **Real-time gezondheidsmetrieken**
- **Performance analytics**
- **Trend analyse**

### Workflows
- **Onboarding**: Nieuwe gebruiker setup
- **Daily Check-in**: Geautomatiseerde dagelijkse assessment

## 🔒 Beveiliging & Privacy
- **Data Privacy**: Alle gezondheidsdata lokaal verwerkt
- **Secure Storage**: Versleutelde database opslag
- **API Security**: Authenticatie en rate limiting
- **GDPR Compliant**: Gebruikerscontrole over data

## 🤝 Development

### Code Conventie
- Volg bestaande code style en patterns
- Gebruik bestaande libraries en utilities
- Implementeer security best practices
- Geen secrets in code committen

### Team Configuraties
- **Main Coaching Team**: Complete health coaching met alle agents
- **Analysis Team**: Gespecialiseerde performance en health analyse

### Custom Workflows
Het systeem ondersteunt aangepaste workflows voor specifieke use cases zoals onboarding nieuwe gebruikers en dagelijkse health check-ins.

---

Deze codebase implementeert een geavanceerd AI coaching systeem met modulaire architectuur, uitgebreide configuratieopties en robuuste integraties voor gezondheids- en fitnessdata.