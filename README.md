## 🤖 SUTURE_CI: Autonomous Self-Healing Agent

Suture_CI is an intelligent, local-first CI agent that monitors Docker containers and automatically repairs codebases when a crash is detected. It analyzes real-time logs to provide validated code fixes directly through GitHub Pull Requests.

<hr>

### Prerequisites

Before running the agent, ensure you have the following installed:
+ Python 3.9+
+ Docker Desktop
+ Ollama (Local LLM Server)

<hr>

### Installation

Clone the repository and install the required Python libraries:

```
# Clone the repository
git clone https://github.com/KSrikzz/Suture_CI.git
cd Suture_CI

# Install dependencies
pip install -r requirements.txt
```

<hr>

### Setup LLM
Pull the coding model required for the local engine:
```
ollama pull qwen2.5-coder:7b
```

<hr>

### Configuration
Create a .env file in the root directory using the provided .env.example as a template:
```
cp .env.example .env
```

<hr>

### Initialize
Start the Suture_CI engine to begin monitoring all active Docker containers:
```
python main.py --watch
```
