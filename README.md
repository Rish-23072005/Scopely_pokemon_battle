Pokémon Battle Simulation - MCP ServerThis project is an implementation of a Model Context Protocol (MCP) server that provides AI models with two core capabilities: a Pokémon Data Resource and a Battle Simulation Tool. The server acts as a bridge, allowing an AI to query a public dataset for Pokémon information and to perform a battle simulation between two Pokémon.The architecture is designed to be modular and easy to extend, following the principles of the MCP.DeliverablesThis submission includes:All Code and Supporting Files: The entire project structure with code for the server, resources, tools, and tests.Dependencies: A requirements.txt file to manage all necessary Python packages.This README File: Clear instructions for setup and usage.Project StructureThe project is organized into logical directories to separate concerns:SCOPELY_POKEMON/
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

How to Install and Run the ServerFollow these simple steps to get the server running.1. PrerequisitesMake sure you have Python 3.7+ and a package manager like pip installed.2. Install DependenciesOpen your terminal, navigate to the project's root directory, and install the required packages. It's recommended to use a virtual environment.# Optional: Create a virtual environment
python -m venv env

# On Windows, activate with: .\env\Scripts\activate

# On macOS/Linux, activate with: source env/bin/activate

# Install the dependencies

pip install -r requirements.txt

3. Start the ServerWith the dependencies installed, you can start the FastAPI server.python main.py

If successful, you will see a message indicating that Uvicorn is running, typically on <http://localhost:8000.How> to Use the ServerThe server is now live and can be queried. You can use a tool like curl or PowerShell's Invoke-RestMethod to interact with it.Task 1: Query the Pokémon Data ResourceThis action exposes comprehensive data for any given Pokémon.Example Request: Get data for Pikachu.$jsonBody = @{
    action = "info"
    pokemon = "pikachu"
} | ConvertTo-Json

Invoke-RestMethod -Uri "<http://localhost:8000/>" -Method Post -Headers @{"Content-Type" = "application/json"} -Body $jsonBody

Expected Response: A JSON object with Pikachu's stats, types, abilities, and moves.Task 2: Use the Battle Simulation ToolThis action simulates a full battle between two Pokémon.Example Request: Simulate a battle between Charmander and Squirtle.$jsonBody = @{
    action = "battle"
    pokemon1 = "charmander"
    pokemon2 = "squirtle"
} | ConvertTo-Json

Invoke-RestMethod -Uri "<http://localhost:8000/>" -Method Post -Headers @{"Content-Type" = "application/json"} -Body $jsonBody

Expected Response: A JSON object with the winner and a detailed battle_log of the fight.How to Test the ProjectThe project includes a robust test suite using pytest. This is the best way to confirm that all functions are working correctly.Make sure you are in the project's root directory.Run the tests with the following command:pytest

This command will automatically discover and run all the tests in the testing/ folder, verifying that the data resource and battle simulation logic are working as intended.
