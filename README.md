# BhimLaw AI - Intelligent Legal Agent

🏛️ **Revolutionary AI-Powered Legal Solutions - Prototype VI**

## Overview

BhimLaw AI is an advanced multi-agent legal AI system that provides comprehensive legal analysis, case research, and professional guidance across all areas of Indian law. The system features 10 specialized legal agents, each designed to handle specific domains of municipal and administrative law.

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** installed on your system
2. **pip** package manager

### Installation

1. **Clone or download** this repository
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

**Main Entry Point**: `run_bhimlaw_ai.py`

```bash
python run_bhimlaw_ai.py
```

The application will start on **http://localhost:5001**

### Access Points

- **Main Application**: http://localhost:5001
- **API Documentation**: http://localhost:5001/docs
- **Interactive API**: http://localhost:5001/redoc
- **Frontend Interface**: Open `bhimlaw_frontend.html` in your browser

## 🏛️ Core Features

### AI Methodologies
- **Natural Language Processing Engine** for legal text analysis
- **Machine Learning & Pattern Recognition** for case outcome prediction
- **Knowledge Graph Technology** for legal concept mapping
- **Retrieval-Augmented Generation (RAG)** for real-time legal research
- **Legal Reasoning Engine** for formal logic application

### Professional Solutions
- **For Advocates & Lawyers**: Case strategy development, document preparation
- **For Judges & Officers**: Decision support framework, case review
- **For Legal Institutions**: Practice management, knowledge systems

### Legal Coverage
- Constitutional Law, Criminal Law, Civil Law, Corporate Law
- Family Law, Labor Law, Tax Law, Environmental Law, IP Law
- Multi-jurisdictional Support (India Focus)

## 🤖 Specialized Agents

1. **Property & Building Violations Agent** - Building regulations, unauthorized constructions
2. **Environmental & Public Health Agent** - Environmental law, pollution control
3. **Employee & Service Matters Agent** - Government service rules, employment law
4. **RTI & Transparency Agent** - Right to Information, transparency issues
5. **Infrastructure & Public Works Agent** - Public infrastructure, works contracts
6. **Encroachment & Land Agent** - Land disputes, encroachment issues
7. **Licensing & Trade Regulation Agent** - Business licenses, trade regulations
8. **Slum Clearance & Resettlement Agent** - Urban development, resettlement
9. **Water & Drainage Agent** - Water supply, drainage systems
10. **Public Nuisance Agent** - Public nuisance, civic issues

## 📁 File Structure

```
Bhimlaw-Ai/
├── run_bhimlaw_ai.py           # Main entry point (START HERE)
├── app.py                      # FastAPI application core
├── specialized_agents.py       # 10 specialized legal agents
├── agent_router.py            # Intelligent agent routing system
├── pdf_generator.py           # Professional PDF report generation
├── bhimlaw_frontend.html      # Frontend interface
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── README_SPECIALIZED_AGENTS.md # Detailed agent documentation
```

## 🔧 Configuration

### Environment Variables (Optional)

Create a `.env` file in the root directory:

```env
NVIDIA_API_KEY=your_nvidia_api_key_here
API_SECRET_KEY=your_secret_key_here
```

### Default Configuration

The application runs with default settings if no environment variables are provided.

## 📖 Usage

1. **Start the server**: `python run_bhimlaw_ai.py`
2. **Open your browser** to http://localhost:5001
3. **Use the web interface** or access the API directly
4. **Generate PDF reports** of legal analyses
5. **Access specialized agents** for domain-specific legal guidance

## 🛠️ Troubleshooting

### Common Issues

1. **Port 5001 already in use**: Change the port in `run_bhimlaw_ai.py`
2. **Missing dependencies**: Run `pip install -r requirements.txt`
3. **Import errors**: Ensure all Python files are in the same directory

### Support

For technical support or questions:
- Check the detailed documentation in `README_SPECIALIZED_AGENTS.md`
- Review the API documentation at http://localhost:5001/docs

## 📄 License

© 2024 BhimLaw AI - Revolutionary Legal Technology Solutions

---

**Start the application with**: `python run_bhimlaw_ai.py`
