# Ice Breaker - AI-Powered LinkedIn Networking Assistant

An intelligent application that generates personalized ice breakers for networking by automatically finding and analyzing LinkedIn profiles using AI agents and large language models.

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Input    │───▶│  LinkedIn Agent │───▶│  Profile Data   │
│ (Person's Name) │    │   (AI Search)   │    │   (Scraping)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │                        │
                              ▼                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Ice Breaker   │◀───│  LLM Generator  │◀───│ Structured Data │
│    Output       │    │   (Ollama)      │    │  (Filtering)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🔧 System Components

### 1. **Main Application** (`ice_breaker.py`)
- **Purpose**: Orchestrates the entire workflow
- **Dependencies**: 
  - `langchain_core` (Prompt templates)
  - `langchain_ollama` (Local LLM integration)
  - Custom modules (agents, third_parties)

### 2. **LinkedIn Lookup Agent** (`agents/linkedin_lookup.py`)
- **Purpose**: Finds LinkedIn profile URLs from person names
- **Architecture**:
  ```
  Name Input → LLM Agent → Search Tool → LinkedIn URL
                ↑              ↓
           React Pattern   Tavily Search
  ```
- **Dependencies**:
  - `langchain.agents` (ReAct agent framework)
  - `langchain` (Hub for prompts)
  - `tools.tools` (Search functionality)
  - **Model**: `qwen2.5:7b` (via Ollama)

### 3. **Search Tools** (`tools/tools.py`)
- **Purpose**: Web search functionality for LinkedIn profiles
- **Dependencies**:
  - `langchain_tavily` (Search API integration)
  - **API**: Tavily Search (requires API key)

### 4. **LinkedIn Scraper** (`third_parties/linkedin.py`)
- **Purpose**: Extracts profile data from LinkedIn URLs
- **Architecture**:
  ```
  LinkedIn URL → API Call → Raw Data → Filtered Data
                    ↑           ↓          ↓
              Scrapin.io API  JSON      Clean Dict
  ```
- **Dependencies**:
  - `requests` (HTTP client)
  - **API**: Scrapin.io (requires API key)
  - **Fallback**: Mock data from GitHub Gist

## 🔄 Data Flow

### Complete Workflow:
1. **Input**: User provides person's name
2. **Search**: AI agent searches web for LinkedIn profile
3. **Extraction**: Profile data extracted via scraping API
4. **Processing**: Data cleaned and structured
5. **Generation**: LLM creates personalized ice breakers
6. **Output**: Conversation starters delivered to user

### Detailed Data Pipeline:
```python
"Tatyjana Ankudo" 
    ↓ (linkedin_lookup_agent)
"https://linkedin.com/in/ankudo" 
    ↓ (scrape_linkedin_profile)
{
    "firstName": "Tatyjana",
    "headline": "Data Scientist...",
    "experience": [...],
    "skills": [...]
}
    ↓ (LLM Chain)
"Ice breaker suggestions:
1. I see you have expertise in molecular biology..."
```

## 🧠 AI Components

### **Language Models Used:**
- **Primary LLM**: `mistral` or `qwen2.5:7b` (via Ollama)
- **Agent LLM**: `qwen2.5:7b` (for search reasoning)
- **Local Execution**: All models run locally (no cloud API calls)

### **AI Frameworks:**
- **LangChain**: Orchestrates LLM interactions and chains
- **ReAct Pattern**: Reasoning + Acting for search agents
- **Prompt Templates**: Structured input/output formatting

## 📦 Dependencies

### **Core Dependencies:**
```python
# LLM & AI Framework
langchain-core          # Prompt templates, base classes
langchain-ollama       # Local LLM integration
langchain-community    # Additional tools
langchain              # Main framework
langchain-tavily       # Search integration

# Local LLM Runtime
ollama                 # Local model serving

# Web & API
requests              # HTTP client
python-dotenv         # Environment variables

# Search & Data
tavily-python         # Search API (optional)
```

### **External APIs:**
```bash
TAVILY_API_KEY=xxx     # Web search functionality
SCRAPIN_API_KEY=xxx    # LinkedIn data extraction
LANGSMITH_API_KEY=xxx  # LLM monitoring (optional)
```

## 🏢 Module Structure

```
ice_breaker/
├── ice_breaker.py              # Main orchestrator
├── agents/
│   ├── __init__.py
│   └── linkedin_lookup.py      # AI search agent
├── third_parties/
│   ├── __init__.py
│   └── linkedin.py             # Profile scraping
├── tools/
│   ├── __init__.py
│   └── tools.py                # Search utilities
├── .env                        # API keys (gitignored)
├── .env.example               # Template for setup
└── .gitignore                 # Excludes sensitive files
```

## 🔗 Component Interactions

### **Import Relationships:**
```python
ice_breaker.py
    ├── agents.linkedin_lookup (lookup function)
    ├── third_parties.linkedin (scrape function)
    └── langchain_ollama (LLM interface)

linkedin_lookup.py
    ├── tools.tools (search functionality)
    ├── langchain.agents (ReAct framework)
    └── langchain (hub, prompts)

tools.py
    └── langchain_tavily (search API)

linkedin.py
    ├── requests (HTTP)
    └── os/dotenv (API keys)
```

### **Data Exchange Formats:**
- **Name** → Agent: `str`
- **LinkedIn URL** → Scraper: `str`
- **Profile Data** → LLM: `dict`
- **Ice Breakers** → User: `str` (formatted text)

## 🚀 Setup & Usage

### **Prerequisites:**
1. **Install Ollama**: Download from [ollama.ai](https://ollama.ai)
2. **Pull Models**: `ollama pull mistral` and `ollama pull qwen2.5:7b`
3. **API Keys**: Sign up for Tavily and Scrapin.io APIs

### **Installation:**

# Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/ice-breaker.git
cd ice-breaker
```

# Install dependencies
```bash
pip install -r requirements.txt
```

# Setup environment
```bash
cp .env.example .env
# (edit .env with API keys)
```

# Install Ollama models
```bash
ollama pull mistral
ollama pull qwen2.5:7b

pip install -r requirements.txt
cp .env.example .env  # Add your API keys
```

### **Running:**
```bash
# Start Ollama server
ollama serve
```

# Run the application
```bash
python ice_breaker.py
```

## 🎯 Key Features

- **🤖 AI-Powered Search**: Automatically finds LinkedIn profiles
- **📊 Smart Data Extraction**: Cleans and structures profile data
- **💬 Personalized Output**: Context-aware conversation starters
- **🔒 Privacy-First**: Runs locally, no data sent to cloud LLMs
- **⚡ Modular Design**: Easy to extend and modify components

## 🛠️ Customization Points

- **Models**: Switch between different Ollama models
- **Prompts**: Modify templates for different output styles
- **Data Sources**: Add more profile sources beyond LinkedIn
- **Output Formats**: Change from text to JSON, email templates, etc.

This architecture enables flexible, AI-powered networking assistance while maintaining privacy and customizability.