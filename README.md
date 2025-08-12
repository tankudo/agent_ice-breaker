# Ice Breaker - AI-Powered LinkedIn Networking Web Application

An intelligent web application that generates personalized ice breakers for networking by automatically finding and analyzing LinkedIn profiles using AI agents and large language models. Features a modern Flask web interface for easy interaction.

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Browser   │───▶│   Flask App     │───▶│  LinkedIn Agent │
│ (User Interface)│    │   (app.py)      │    │   (AI Search)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │                        │
                              ▼                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   JSON Response │◀───│  Ice Breaker    │◀───│ LinkedIn Profile│
│  (Web Results)  │    │  Engine (LLM)   │    │    Scraper      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🌐 Web Application Components

### 1. **Flask Web Server** (`app.py`)
- **Purpose**: Web interface and API endpoints
- **Routes**:
  - `GET /` → Serves the main interface
  - `POST /process` → Handles name processing requests
- **Features**:
  - Form-based input for person names
  - JSON API responses
  - Error handling and debugging
  - CORS-enabled for web requests

### 2. **Frontend Interface** (`templates/index.html`)
- **Purpose**: User-friendly web interface
- **Features**:
  - Name input form
  - Real-time processing feedback
  - Results display with profile photos
  - Responsive design
  - AJAX-powered interactions

### 3. **Main Processing Engine** (`ice_breaker.py`)
- **Purpose**: Orchestrates the AI workflow
- **Multi-Model Support**:
  - **Ollama** (Local models - default)
  - **Claude** (Anthropic API - premium)
  - **OpenAI** (GPT models)
- **Parameters**:
  - `temperature=0` for precise name matching
  - Dynamic model selection
  - Error handling and fallbacks

## 🔧 System Components

### 4. **LinkedIn Lookup Agent** (`agents/linkedin_lookup.py`)
- **Purpose**: Finds exact LinkedIn profile URLs from person names
- **Enhanced Precision**:
  ```
  Name Input → Precise LLM Agent → Search Tool → Exact LinkedIn URL
                ↑                    ↓
           React Pattern        Validated Results
  ```
- **Features**:
  - Exact name matching (prevents "AAA DDD" when searching "BBB DDD")
  - First/last name validation
  - Fallback mechanisms
  - **Model**: Configurable (Ollama/Claude/OpenAI)

### 5. **Search Tools** (`tools/tools.py`)
- **Purpose**: Web search functionality for LinkedIn profiles
- **Dependencies**:
  - `langchain_tavily` (Search API integration)
  - **API**: Tavily Search (requires API key)

### 6. **LinkedIn Scraper** (`third_parties/linkedin.py`)
- **Purpose**: Extracts profile data from LinkedIn URLs
- **Architecture**:
  ```
  LinkedIn URL → API Call → Raw Data → Structured Data
                    ↑           ↓          ↓
              Scrapin.io API  JSON    Clean Profile Dict
  ```
- **Output**: Profile data including photos, experience, skills
- **Fallback**: Mock data for development

### 7. **Output Parser** (`output_parser.py`)
- **Purpose**: Structures LLM output into consistent format
- **Features**:
  - Pydantic models for validation
  - JSON serialization for web responses
  - Type safety and error handling

## 🔄 Complete Web Workflow

### User Journey:
1. **Access**: User opens web browser to `http://localhost:5000`
2. **Input**: User enters person's name in web form
3. **Submit**: Form data sent via AJAX POST to `/process`
4. **Search**: AI agent searches for exact LinkedIn profile
5. **Scrape**: Profile data extracted via API
6. **Analyze**: LLM generates personalized ice breakers
7. **Display**: Results shown on web page with profile photo

### Detailed Data Pipeline:
```python
Web Form: "BBB DDD"
    ↓ (Flask POST /process)
request.form.get('name') = "BBB DDD"
    ↓ (ice_breake_with)
precise_linkedin_lookup("BBB DDD")
    ↓ (AI Agent with temperature=0)
"https://linkedin.com/in/BBB-DDD-12345"
    ↓ (scrape_linkedin_profile)
{
    "firstName": "BBB",
    "lastName": "DDD", 
    "headline": "Software Engineer...",
    "photoUrl": "https://...",
    "experience": [...],
    "skills": [...]
}
    ↓ (LLM Chain with verification)
Summary{
    "summary": "Professional software engineer...",
    "facts": ["Expert in Python", "Works at Tech Corp"],
    "ice_breakers": ["I noticed your Python expertise...", ...],
    "interests": ["Machine Learning", "Open Source"]
}
    ↓ (summary.to_dict())
    ↓ (Flask jsonify)
JSON Response to browser
    ↓ (JavaScript)
Web page updates with results
```

## 🧠 AI Components & Model Options

### **Multi-Model Architecture:**
The application supports three LLM providers:

#### **Option 1: Ollama (Default - Free)**
```python
llm = ChatOllama(
    model='llama3:latest',
    temperature=0  # For precise matching
)
```
- **Pros**: Free, private, runs locally
- **Cons**: Requires local setup, slower
- **Models**: `llama3:latest`, `qwen2.5:7b`, `mistral`

#### **Option 2: Claude (Premium)**
```python
llm = ChatAnthropic(
    model="claude-sonnet-4-20250514",
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    temperature=0
)
```
- **Pros**: Highest quality, excellent reasoning
- **Cons**: Requires API credits
- **Usage**: For premium users with API access

#### **Option 3: OpenAI**
```python
llm = ChatOpenAI(
    model="gpt-4",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0
)
```
- **Pros**: Well-established, reliable
- **Cons**: Requires API credits
- **Usage**: Alternative premium option

### **Temperature Settings:**
- **Lookup Agent**: `temperature=0` (precise name matching)
- **Analysis Agent**: `temperature=0` (consistent, accurate summaries)

## 📦 Dependencies

### **Web Framework:**
```python
flask                  # Web server and routing
```

### **AI & LLM Framework:**
```python
langchain-core         # Prompt templates, base classes
langchain-ollama      # Local LLM integration (default)
langchain-anthropic   # Claude integration (premium)
langchain-openai      # OpenAI integration (premium)
langchain-community   # Additional tools
langchain             # Main framework
langchain-tavily      # Search integration
```

### **Data Processing:**
```python
pydantic              # Output parsing and validation
requests              # HTTP client for APIs
python-dotenv         # Environment variables
```

### **External APIs & Services:**
```bash
# Required APIs
TAVILY_API_KEY=xxx           # Web search functionality
SCRAPIN_API_KEY=xxx          # LinkedIn data extraction

# Optional Premium APIs
ANTHROPIC_API_KEY=xxx        # Claude access (premium users)
OPENAI_API_KEY=xxx           # OpenAI access (alternative)

# Optional Monitoring
LANGSMITH_API_KEY=xxx        # LLM monitoring (optional)
```

## 🏢 Project Structure

```
ice_breaker/
├── app.py                      # Flask web server (main entry point)
├── ice_breaker.py              # AI processing engine
├── output_parser.py            # Response formatting
├── templates/
│   └── index.html             # Web interface
├── static/                    # CSS/JS assets (if any)
├── agents/
│   ├── __init__.py
│   └── linkedin_lookup.py     # Precise AI search agent
├── third_parties/
│   ├── __init__.py
│   └── linkedin.py            # Profile scraping
├── tools/
│   ├── __init__.py
│   └── tools.py               # Search utilities
├── .env                       # API keys (gitignored)
├── .env.example              # Template for setup
├── requirements.txt          # Python dependencies
└── .gitignore               # Excludes sensitive files
```

## 🔗 Component Interactions

### **Web Request Flow:**
```python
Browser
    ├── GET / → app.py (render index.html)
    └── POST /process → app.py
                         ├── ice_breaker.py
                         │   ├── agents.linkedin_lookup
                         │   ├── third_parties.linkedin
                         │   └── langchain_ollama/anthropic/openai
                         └── JSON response

app.py
    ├── flask (web framework)
    ├── ice_breaker.ice_breake_with()
    └── jsonify (JSON responses)

ice_breaker.py
    ├── agents.linkedin_lookup (search)
    ├── third_parties.linkedin (scraping)
    ├── output_parser (formatting)
    └── LLM provider (ollama/claude/openai)
```

### **Data Exchange Formats:**
- **Web Form** → Flask: `form data`
- **Flask** → Engine: `str` (name)
- **Agent** → Scraper: `str` (LinkedIn URL)
- **Scraper** → LLM: `dict` (profile data)
- **LLM** → Parser: `str` (raw response)
- **Parser** → Flask: `Summary` object
- **Flask** → Browser: `JSON` response

## 🚀 Setup & Usage

### **Prerequisites:**
1. **Python 3.8+**: Ensure Python is installed
2. **Ollama** (for free local models): Download from [ollama.ai](https://ollama.ai)
3. **API Keys**: Sign up for required services

### **Installation:**

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/ice-breaker.git
cd ice-breaker

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your API keys
```

### **For Ollama Users (Free Option):**
```bash
# Install and start Ollama
ollama pull llama3:latest
ollama serve  # Keep this running
```

### **For Premium Users (Claude/OpenAI):**
```bash
# Add API keys to .env file
echo "ANTHROPIC_API_KEY=your_key_here" >> .env
# or
echo "OPENAI_API_KEY=your_key_here" >> .env
```

### **Running the Application:**
```bash
# Start the web server
python app.py

# Open browser to:
# http://localhost:5000
```

### **Using Different Models:**
```python
# In ice_breaker.py, change the model_type:
summary, photo = ice_breake_with(name, model_type="ollama")    # Free
summary, photo = ice_breake_with(name, model_type="claude")    # Premium
summary, photo = ice_breake_with(name, model_type="openai")    # Premium
```

## 🎯 Key Features

- **🌐 Web Interface**: Modern browser-based application
- **🤖 Multi-Model AI**: Support for Ollama, Claude, and OpenAI
- **🎯 Precise Matching**: Finds exact persons (BBB ≠ Philip)
- **📊 Smart Extraction**: Structured profile analysis
- **💬 Personalized Output**: Context-aware conversation starters
- **🔒 Flexible Privacy**: Local models or cloud APIs
- **⚡ Real-time Processing**: AJAX-powered interface
- **📱 Responsive Design**: Works on desktop and mobile

## 🛠️ Customization & Development

### **Model Switching:**
```python
# Easy model configuration
def ice_breake_with(name: str, model_type: str = "ollama"):
    # Supports: "ollama", "claude", "openai"
```

### **Template Customization:**
- Modify prompts in `ice_breaker.py`
- Adjust output format in `output_parser.py`
- Customize web interface in `templates/index.html`

### **API Integration:**
- Add new LLM providers in `ice_breaker.py`
- Extend search tools in `tools/tools.py`
- Add new data sources in `third_parties/`

### **Deployment Options:**
- **Local**: `python app.py`
- **Docker**: Create Dockerfile for containerization
- **Cloud**: Deploy to Heroku, AWS, or similar platforms

## 🔧 Troubleshooting

### **Common Issues:**
1. **Wrong person found**: Ensure `temperature=0` in lookup agent
2. **API errors**: Check `.env` file has correct API keys
3. **Ollama connection**: Verify `ollama serve` is running
4. **Flask errors**: Check console logs in browser developer tools

### **Model Performance:**
- **Best Quality**: Claude (requires API credits)
- **Good Balance**: OpenAI GPT-4 (requires API credits)  
- **Free Option**: Ollama Llama3 (local, private)

This web application provides an intuitive interface for AI-powered networking assistance while supporting multiple AI providers and maintaining flexibility for different user needs.
