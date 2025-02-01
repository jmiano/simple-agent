# Simple Agent

A ReAct-based LLM agent with tool integration, built using OpenAI's GPT-4 and function calling.

## Features

- 🤖 Interactive chat interface built with Streamlit
- 🔄 ReAct framework for reasoning and action
- 🛠️ Integrated tools:
  - Google Search for real-time information
  - Calculator for mathematical operations
  - DateTime for date calculations
  - Wikipedia for article search and reading

## Prerequisites

- Python 3.10 or higher
- Conda package manager
- OpenAI API key
- SerpAPI key (for Google Search)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/jmiano/simple-agent.git
   cd simple-agent
   ```

2. Create and activate the conda environment:
   ```bash
   conda env create -f environment.yml
   conda activate simple-agent
   ```

3. Create a `.env` file in the root directory with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   SERPAPI_API_KEY=your_serpapi_api_key
   ```

## Running the Application

```bash
streamlit run src/app.py
```

## Project Structure

```
simple-agent/
├── src/
│   ├── app.py              # Streamlit application
│   ├── agent.py            # ReAct agent implementation
│   └── tools/              # Custom tools
│       ├── __init__.py
│       ├── calculator.py    # Calculator tool
│       ├── datetime_tool.py # DateTime tool
│       ├── search.py       # Google search tool
│       └── wikipedia_tool.py# Wikipedia tool
├── tests/                  # Test files
├── environment.yml         # Conda environment file
├── .env.example           # Example environment variables
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## How It Works

The agent uses a ReAct (Reasoning + Action) framework to:
1. Plan the steps needed to answer a query
2. Execute those steps using available tools
3. Present the results in a clear format

Example interactions:
- "What is quantum computing according to Wikipedia?"
- "Calculate 2 + 2 * 5"
- "What day was it 8 days ago?"

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for GPT-4 and function calling
- Streamlit for the web interface
- Various open-source packages used in this project 