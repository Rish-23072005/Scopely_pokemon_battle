# Pokémon Battle Simulation - MCP Server

A comprehensive Model Context Protocol (MCP) server implementation that bridges AI models with the Pokémon universe, providing rich data access and interactive battle simulations.

## Overview

This project implements a technical MCP server designed to integrate seamlessly with Large Language Models. It exposes two primary capabilities:

- **Pokémon Data Resource**: Comprehensive information retrieval system
- **Battle Simulation Tool**: Complex battle execution engine

The architecture prioritizes modularity, scalability, and seamless integration with any MCP-compliant LLM.

## What's Included

This repository contains everything you need to get started:

- **Complete Server Implementation**: All core logic and supporting scripts
- **Dependency Management**: Comprehensive `requirements.txt` file
- **Documentation**: This detailed README with setup instructions
- **Test Suite**: Robust testing framework using pytest

## Project Structure

```
SCOPELY_POKEMON/
├── resource_encyclopedia/
│   ├── __init__.py
│   └── poke_data.py            # Pokémon Data Resource
├── rule/
│   ├── __init__.py
│   ├── chart.py                # Type effectiveness calculations
│   ├── damage_calcu.py         # Damage calculation engine
│   └── stat_effect.py          # Status effect management
├── testing/
│   ├── __init__.py
│   ├── battle.py               # Battle simulation tests
│   └── resources.py            # Data resource tests
├── tools/
│   ├── __init__.py
│   └── battle_simulate.py      # Battle Simulation Tool
├── dispatcher.py               # Request routing logic
├── main.py                     # FastAPI server entry point
└── requirements.txt            # Project dependencies
```

## Quick Start

### Prerequisites

- **Python 3.9+** installed on your system
- **pip** (Python package installer)

### Installation

1. **Clone and Navigate**
   ```bash
   cd SCOPELY_POKEMON
   ```

2. **Set Up Virtual Environment** (Recommended)
   ```bash
   # Create virtual environment
   python -m venv env
   
   # Activate it
   # Windows:
   .\env\Scripts\activate
   # macOS/Linux:
   source env/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch Server**
   ```bash
   python main.py
   ```

   **Success**: You should see Uvicorn running at `http://localhost:8000`

## Usage Guide

### Pokémon Data Queries

Retrieve comprehensive Pokémon information including stats, types, abilities, and movesets.

**Example: Get Pikachu's Data**

**PowerShell:**
```powershell
$jsonBody = @{
    action = "info"
    pokemon = "pikachu"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/" -Method Post -Headers @{"Content-Type" = "application/json"} -Body $jsonBody
```

**cURL:**
```bash
curl -X POST "http://localhost:8000/" \
     -H "Content-Type: application/json" \
     -d '{"action": "info", "pokemon": "pikachu"}'
```

**Expected Response:**
```json
{
  "name": "pikachu",
  "stats": {...},
  "types": [...],
  "abilities": [...],
  "moves": [...]
}
```

### Battle Simulations

Execute full battles between two Pokémon with detailed turn-by-turn logging.

**Example: Charmander vs. Squirtle**

**PowerShell:**
```powershell
$jsonBody = @{
    action = "battle"
    pokemon1 = "charmander"
    pokemon2 = "squirtle"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/" -Method Post -Headers @{"Content-Type" = "application/json"} -Body $jsonBody
```

**cURL:**
```bash
curl -X POST "http://localhost:8000/" \
     -H "Content-Type: application/json" \
     -d '{"action": "battle", "pokemon1": "charmander", "pokemon2": "squirtle"}'
```

**Expected Response:**
```json
{
  "winner": "squirtle",
  "battle_log": [
    "Turn 1: Charmander used Ember...",
    "Turn 2: Squirtle used Water Gun...",
    ...
  ]
}
```

## Testing

Run the comprehensive test suite to verify all functionality:

```bash
pytest
```

**Test Coverage:**
- Pokémon data resource functionality
- Battle simulation logic
- Type effectiveness calculations
- Damage calculation accuracy
- Status effect handling

### Verbose Testing
```bash
pytest -v
```

### Run Specific Tests
```bash
# Test only battle functionality
pytest testing/battle.py

# Test only data resources
pytest testing/resources.py
```

## API Reference

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | POST | Main endpoint for all requests |

### Request Format

All requests should be sent as JSON with the following structure:

```json
{
  "action": "info|battle",
  "pokemon": "pokemon_name",      // For info requests
  "pokemon1": "pokemon_name",     // For battle requests
  "pokemon2": "pokemon_name"      // For battle requests
}
```

## 🔍 Troubleshooting

### Common Issues

**Server won't start:**
- Ensure Python 3.7+ is installed: `python --version`
- Check if port 8000 is available
- Verify all dependencies are installed: `pip list`

**Import errors:**
- Make sure you're in the correct directory
- Activate your virtual environment if using one
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

**Test failures:**
- Run tests individually to isolate issues
- Check Python path and working directory
- Ensure all required test data is present

