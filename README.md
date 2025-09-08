Pokémon Battle Simulation - MCP ServerThis project is a technical implementation of a Model Context Protocol (MCP) server. Its primary function is to serve as a bridge between an AI model and the world of Pokémon, exposing two core capabilities: a Pokémon Data Resource for information retrieval and a Battle Simulation Tool for executing complex actions. This architecture is built to be modular, scalable, and easy to integrate with any LLM that follows the MCP standard.DeliverablesThe deliverables for this project are packaged as a single repository containing:All Code and Supporting Files: The complete server implementation, including all scripts for the core logic and supporting files like this README.Dependencies: A requirements.txt file that lists all necessary Python packages.This README File: Comprehensive documentation explaining how to install, run, and use the server, ensuring a clear and straightforward setup process for anyone unfamiliar with the project.Project StructureThe project is organized into logical directories to separate concerns and improve maintainability. The core server logic is located at the root, while resources, rules, and tests are stored in dedicated folders.SCOPELY_POKEMON/
├── resource_encyclopedia/
│   ├── __init__.py
│   └── poke_data.py            # The Pokémon Data Resource
├── rule/
│   ├── __init__.py
│   ├── chart.py                # Type effectiveness rules
│   ├── damage_calcu.py         # Damage calculation logic
│   └── stat_effect.py          # Status effect rules
├── testing/
│   ├── __init__.py
│   ├── battle.py               # Tests for battle simulation
│   └── resources.py            # Tests for the data resource
├── tools/
│   ├── __init__.py
│   └── battle_simulate.py      # The Battle Simulation Tool
├── dispatcher.py               # Routes incoming requests
├── main.py                     # FastAPI server entry point
└── requirements.txt            # Project dependencies
How to Install and Run the ServerFollow these simple steps to get the server up and running.1. PrerequisitesYou'll need Python 3.7+ and pip (the Python package installer) installed on your system.2. Install DependenciesIt is highly recommended to use a virtual environment to manage dependencies. Open your terminal, navigate to the project's root directory, and run the following commands:# Optional: Create and activate a virtual environment
python -m venv env

# On Windows, use:
# .\env\Scripts\activate
# On macOS/Linux, use:
# source env/bin/activate

# Install the dependencies from the requirements.txt file
pip install -r requirements.txt
3. Start the ServerWith the dependencies installed, you can start the FastAPI server. From the project's root directory, execute the following command:python main.py
If successful, you will see a message indicating that Uvicorn is running, typically at http://localhost:8000. This means your server is live and ready to accept requests.How to Use the ServerThe server is now live and can be queried. You can use a tool like PowerShell's Invoke-RestMethod to send requests and interact with both the data resource and the simulation tool.Task 1: Query the Pokémon Data ResourceThis action exposes comprehensive data for any given Pokémon, allowing an LLM to "read" information from the Pokémon world.Example Request: Get data for Pikachu.$jsonBody = @{
    action = "info"
    pokemon = "pikachu"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/" -Method Post -Headers @{"Content-Type" = "application/json"} -Body $jsonBody
Expected Response: A JSON object with Pikachu's stats, types, abilities, and a list of moves.Task 2: Use the Battle Simulation ToolThis action simulates a full battle between two Pokémon, allowing an LLM to "perform" an action within the Pokémon world.Example Request: Simulate a battle between Charmander and Squirtle.$jsonBody = @{
    action = "battle"
    pokemon1 = "charmander"
    pokemon2 = "squirtle"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/" -Method Post -Headers @{"Content-Type" = "application/json"} -Body $jsonBody
Expected Response: A JSON object with the battle's winner and a detailed battle_log of the fight, turn by turn.How to Test the ProjectA robust test suite using the pytest framework is included to verify the functionality of the core components. This is the best way to confirm that all functions are working as intended.From the project's root directory, run the tests with the following command:pytest
This command will automatically discover and run all the tests in the testing/ folder, ensuring that the data resource and battle simulation logic are fully functional.
