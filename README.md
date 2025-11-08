# Oxford Debate Agent

An agentic application that generates content for Oxford-style debates using AI.

## Overview

This project creates a complete Oxford-style debate with multiple speakers arguing for and against a motion. The output is 6 separate audio files in MP3 format representing different debate roles.

## Oxford Debate Format

An Oxford debate typically includes:

1. **Opening Statement - Proposition** (For the motion)
2. **Opening Statement - Opposition** (Against the motion)
3. **Rebuttal - Proposition** (Counter-arguments from the "for" side)
4. **Rebuttal - Opposition** (Counter-arguments from the "against" side)
5. **Closing Statement - Proposition** (Final arguments for the motion)
6. **Closing Statement - Opposition** (Final arguments against the motion)

## Project Structure

```
oxford-debate-agent/
├── src/                    # Main source code
│   ├── main.py            # Entry point
│   ├── debate_orchestrator.py  # Coordinates the debate flow
│   └── audio_generator.py # Text-to-speech generation
├── agents/                # AI agent definitions
│   ├── proposition_agent.py
│   ├── opposition_agent.py
│   └── moderator_agent.py
├── config/                # Configuration files
│   ├── config.yaml        # Main configuration
│   └── prompts.yaml       # Agent prompts/templates
├── output/                # Generated debate audio files
│   └── .gitkeep
├── tests/                 # Unit tests
├── docs/                  # Documentation
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore
└── README.md
```

## Output

The application generates 6 MP3 files:
- `01_proposition_opening.mp3`
- `02_opposition_opening.mp3`
- `03_proposition_rebuttal.mp3`
- `04_opposition_rebuttal.mp3`
- `05_proposition_closing.mp3`
- `06_opposition_closing.mp3`

## Installation

### Quick Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/pranavjh/oxford-debate-agent.git
cd oxford-debate-agent

# Run setup script (creates virtual environment and installs dependencies)
./setup.sh

# Copy your OpenAI config
cp /path/to/your/config.json config/secrets/config.json
```

### Manual Setup

```bash
# Clone the repository
git clone https://github.com/pranavjh/oxford-debate-agent.git
cd oxford-debate-agent

# Create and activate virtual environment (recommended to avoid dependency conflicts)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp /path/to/your/config.json config/secrets/config.json
```

### Configuration

The `config/secrets/config.json` file should contain:
```json
{
  "OPENAI_API_KEY": "sk-...",
  "OPENAI_API_BASE": "https://api.openai.com/v1/"
}
```

**Important Notes:**
- ⚠️ **Use a virtual environment** to avoid dependency conflicts with other Python packages
- 🔒 The `config/secrets/` directory is gitignored to protect your API keys
- ✅ The setup script automatically creates the virtual environment for you

## Usage

**Important:** Always activate the virtual environment first:
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Then run the debate generator:
```bash
# Run with default motion
python src/main.py

# Run with custom motion
python src/main.py --motion "AI will replace human creativity"

# See example motions
python src/main.py list-motions
```

## Features

- 🎭 Multi-agent debate system with proposition and opposition agents
- 🧠 Context-aware arguments and rebuttals
- 🎙️ High-quality text-to-speech audio generation
- ⚙️ Configurable debate parameters (length, style, complexity)
- 📊 Structured output format

## Technology Stack

- **LLM Framework**: LangChain for agent orchestration
- **LLM**: OpenAI GPT-4o (latest model)
- **TTS**: OpenAI TTS-1-HD (high quality audio)
- **Audio**: pydub for audio processing
- **CLI**: Typer with Rich for beautiful terminal interface

## Roadmap

- [ ] Basic debate generation
- [ ] Audio synthesis
- [ ] Custom voice selection
- [ ] Debate topics library
- [ ] Web interface
- [ ] Multi-language support

## License

MIT

## Author

Pranav JH (@pranavjh)
