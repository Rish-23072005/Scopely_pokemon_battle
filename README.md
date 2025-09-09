# Pokémon Battle Simulation - MCP Server

A comprehensive Model Context Protocol (MCP) server that provides AI models with access to Pokémon data and battle simulation capabilities.

## Features

### Pokémon Data Resource
- **Comprehensive Pokémon Information**: Access to detailed data for all Pokémon including:
  - Base stats (HP, Attack, Defense, Special Attack, Special Defense, Speed)
  - Types and type effectiveness
  - Abilities and their effects
  - Available moves with detailed information
  - Evolution chains and requirements
  - Sprites and visual data

### Battle Simulation Tool
- **Realistic Battle Mechanics**: 
  - Type effectiveness calculations (Fire beats Grass, Water beats Fire, etc.)
  - Accurate damage calculations using official Pokémon formulas
  - Turn order based on Speed stats
  - Critical hit mechanics
  - STAB (Same Type Attack Bonus)

- **Status Effects System**: 
  - **Paralysis**: 25% chance to be unable to move, speed reduced by 75%
  - **Burn**: Continuous HP damage, physical attack reduced by 50%
  - **Poison**: Continuous HP damage each turn
  - **Badly Poisoned**: Increasing damage each turn
  - **Freeze**: Unable to move with chance to thaw
  - **Sleep**: Unable to move for 1-3 turns

- **Detailed Battle Logs**: Complete turn-by-turn battle reports with outcomes

## Project Structure

```
SCOPELY_POKEMON/
├── resource_encyclopedia/
│   ├── __init__.py
│   └── poke_data.py              # Pokémon Data Resource
├── rule/
│   ├── __init__.py
│   ├── chart.py                  # Type effectiveness calculations
│   ├── damage_calcu.py           # Damage calculation engine
│   └── stat_effect.py            # Status effect management
├── testing/
│   ├── __init__.py
│   ├── battle.py                 # Battle simulation tests
│   └── resources.py              # Data resource tests
├── tools/
│   ├── __init__.py
│   └── battle_simulate.py        # Battle Simulation Tool
├── dispatcher.py                 # MCP request routing logic
├── main.py                       # FastAPI server entry point
├── requirements.txt              # Project dependencies
└── README.md                     # This file
```

## Installation & Setup

### Prerequisites
- Python 3.9 or higher
- Internet connection (for PokéAPI access)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start the Server
```bash
python main.py
```

The server will start on `http://localhost:8000`

### Step 3: Verify Installation
Visit `http://localhost:8000` to see the server information, or check the health endpoint:
```bash
curl http://localhost:8000/health
```

## Usage

### MCP Protocol Endpoints

#### Initialize Connection
```bash
POST /mcp
{
  "jsonrpc": "2.0",
  "method": "initialize",
  "id": "1"
}
```

#### List Available Resources
```bash
POST /mcp
{
  "jsonrpc": "2.0",
  "method": "resources/list",
  "id": "2"
}
```

#### Get Pokémon Data
```bash
POST /mcp
{
  "jsonrpc": "2.0",
  "method": "resources/read",
  "params": {
    "uri": "pokemon://data",
    "pokemon": "pikachu"
  },
  "id": "3"
}
```

#### List Available Tools
```bash
POST /mcp
{
  "jsonrpc": "2.0",
  "method": "tools/list",
  "id": "4"
}
```

#### Simulate Battle
```bash
POST /mcp
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "battle_simulate",
    "arguments": {
      "pokemon1": "pikachu",
      "pokemon2": "charmander",
      "level1": 50,
      "level2": 50
    }
  },
  "id": "5"
}
```

### Direct API Endpoints (for testing)

#### Get Pokémon Data
```bash
GET /pokemon/{pokemon_name}
# Example: GET /pokemon/pikachu
```

#### Simulate Battle
```bash
POST /battle?pokemon1=pikachu&pokemon2=charmander
```

## Testing

### Run Battle Tests
```bash
cd testing
python battle.py
```

### Run Resource Tests
```bash
cd testing
python resources.py
```

### Test Coverage
The testing suite includes:
- Basic battle simulations
- Level difference battles
- Type advantage scenarios
- Invalid input handling
- Pokémon data retrieval
- Caching mechanism verification
- Type effectiveness queries

## API Examples

### Example: Getting Pikachu's Data
```python
import httpx
import asyncio

async def get_pikachu():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/pokemon/pikachu")
        data = response.json()
        print(f"Name: {data['name']}")
        print(f"Types: {data['types']}")
        print(f"Base Stats: {data['base_stats']}")

asyncio.run(get_pikachu())
```

### Example: Simulating a Battle
```python
import httpx
import asyncio

async def simulate_battle():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/battle",
            params={"pokemon1": "pikachu", "pokemon2": "charmander"}
        )
        result = response.json()
        print(f"Winner: {result['winner']}")
        print(f"Battle Log:\n{result['battle_log']}")

asyncio.run(simulate_battle())
```

## Configuration

### Environment Variables
- `PORT`: Server port (default: 8000)
- `HOST`: Server host (default: 0.0.0.0)
- `LOG_LEVEL`: Logging level (default: info)

### Customization
- **Add new status effects**: Modify `rule/stat_effect.py`
- **Adjust damage calculations**: Update `rule/damage_calcu.py`
- **Add new types**: Extend `rule/chart.py`
- **Custom moves**: Enhance the move database in `resource_encyclopedia/poke_data.py`

## Performance Features

### Caching
- Pokémon data is cached in memory after first request
- Move details are cached to reduce API calls
- Type effectiveness data is pre-loaded

### Rate Limiting
- Built-in request handling to avoid overwhelming PokéAPI
- Efficient batch processing for multiple requests

## Error Handling

The server includes comprehensive error handling for:
- Invalid Pokémon names
- Network connectivity issues
- Malformed MCP requests
- Battle simulation errors
- Resource access failures

## Development

### Adding New Features
1. Create feature branch
2. Implement changes following existing patterns
3. Add tests in the `testing/` directory
4. Update documentation
5. Submit pull request

### Code Style
- Follow PEP 8 guidelines
- Use type hints where possible
- Include comprehensive docstrings
- Maintain test coverage

## Troubleshooting

### Common Issues

**Server won't start**
- Check if port 8000 is available
- Verify all dependencies are installed
- Check Python version (3.8+ required)

**Pokémon not found**
- Verify exact spelling (use lowercase)
- Check PokéAPI availability
- Try common Pokémon names first

**Battle simulation fails**
- Ensure both Pokémon names are valid
- Check network connectivity
- Verify level parameters are between 1-100

### Logs
Server logs include detailed information about:
- MCP request processing
- API calls to PokéAPI
- Battle simulation steps
- Error conditions

