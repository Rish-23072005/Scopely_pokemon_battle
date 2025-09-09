"""
Pokémon Battle Simulation MCP Server
Main FastAPI server entry point
"""
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging

from dispatcher import MCPDispatcher
from resource_encyclopedia.poke_data import PokemonDataResource
from tools.battle_simulate import BattleSimulationTool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Pokémon Battle Simulation MCP Server",
    description="MCP Server providing Pokémon data resources and battle simulation tools",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize MCP components
pokemon_data = PokemonDataResource()
battle_tool = BattleSimulationTool()
dispatcher = MCPDispatcher(pokemon_data, battle_tool)

# MCP Protocol Models
class MCPRequest(BaseModel):
    jsonrpc: str = "2.0"
    method: str
    params: Optional[Dict[str, Any]] = None
    id: Optional[str] = None

class MCPResponse(BaseModel):
    jsonrpc: str = "2.0"
    result: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None
    id: Optional[str] = None

@app.get("/")
async def root():
    """Root endpoint with server information"""
    return {
        "name": "Pokémon Battle Simulation MCP Server",
        "version": "1.0.0",
        "description": "MCP Server for Pokémon data and battle simulations",
        "capabilities": {
            "resources": ["pokemon_data"],
            "tools": ["battle_simulate"]
        }
    }

@app.post("/mcp")
async def mcp_endpoint(request: MCPRequest):
    """Main MCP protocol endpoint"""
    try:
        logger.info(f"Received MCP request: {request.method}")
        response_data = await dispatcher.handle_request(request.method, request.params or {})
        
        return MCPResponse(
            result=response_data,
            id=request.id
        )
    except Exception as e:
        logger.error(f"Error handling MCP request: {str(e)}")
        return MCPResponse(
            error={
                "code": -32603,
                "message": "Internal error",
                "data": str(e)
            },
            id=request.id
        )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "server": "pokemon-mcp"}

@app.get("/capabilities")
async def get_capabilities():
    """Get server capabilities"""
    return await dispatcher.handle_request("initialize", {})

# Development endpoints for testing
@app.get("/pokemon/{pokemon_name}")
async def get_pokemon_direct(pokemon_name: str):
    """Direct endpoint to get Pokémon data (for testing)"""
    try:
        result = await pokemon_data.get_pokemon_data(pokemon_name.lower())
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/battle")
async def simulate_battle_direct(pokemon1: str, pokemon2: str):
    """Direct endpoint to simulate battle (for testing)"""
    try:
        result = await battle_tool.simulate_battle(pokemon1.lower(), pokemon2.lower())
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )