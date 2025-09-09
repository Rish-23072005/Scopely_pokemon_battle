"""
MCP Request Dispatcher
Routes MCP protocol requests to appropriate handlers
"""
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class MCPDispatcher:
    def __init__(self, pokemon_resource, battle_tool):
        self.pokemon_resource = pokemon_resource
        self.battle_tool = battle_tool
        
        # MCP method handlers
        self.handlers = {
            "initialize": self._handle_initialize,
            "resources/list": self._handle_list_resources,
            "resources/read": self._handle_read_resource,
            "tools/list": self._handle_list_tools,
            "tools/call": self._handle_call_tool,
        }
    
    async def handle_request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Route MCP requests to appropriate handlers"""
        logger.info(f"Dispatching method: {method}")
        
        if method not in self.handlers:
            raise ValueError(f"Unknown method: {method}")
        
        return await self.handlers[method](params)
    
    async def _handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP initialize request"""
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "resources": {
                    "subscribe": True,
                    "listChanged": True
                },
                "tools": {
                    "listChanged": True
                }
            },
            "serverInfo": {
                "name": "pokemon-battle-mcp-server",
                "version": "1.0.0"
            }
        }
    
    async def _handle_list_resources(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """List available MCP resources"""
        return {
            "resources": [
                {
                    "uri": "pokemon://data",
                    "name": "Pokémon Data",
                    "description": "Comprehensive Pokémon information including stats, types, abilities, and moves",
                    "mimeType": "application/json"
                }
            ]
        }
    
    async def _handle_read_resource(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Read a specific MCP resource"""
        uri = params.get("uri", "")
        
        if uri == "pokemon://data":
            # Get query parameters
            pokemon_name = params.get("pokemon", "")
            if pokemon_name:
                data = await self.pokemon_resource.get_pokemon_data(pokemon_name.lower())
                return {
                    "contents": [
                        {
                            "uri": uri,
                            "mimeType": "application/json",
                            "text": str(data)
                        }
                    ]
                }
            else:
                # Return list of all available Pokémon
                data = await self.pokemon_resource.list_all_pokemon()
                return {
                    "contents": [
                        {
                            "uri": uri,
                            "mimeType": "application/json",
                            "text": str(data)
                        }
                    ]
                }
        
        raise ValueError(f"Unknown resource URI: {uri}")
    
    async def _handle_list_tools(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """List available MCP tools"""
        return {
            "tools": [
                {
                    "name": "battle_simulate",
                    "description": "Simulate a battle between two Pokémon with detailed combat mechanics",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "pokemon1": {
                                "type": "string",
                                "description": "Name of the first Pokémon"
                            },
                            "pokemon2": {
                                "type": "string", 
                                "description": "Name of the second Pokémon"
                            },
                            "level1": {
                                "type": "integer",
                                "description": "Level of first Pokémon (default: 50)",
                                "minimum": 1,
                                "maximum": 100,
                                "default": 50
                            },
                            "level2": {
                                "type": "integer",
                                "description": "Level of second Pokémon (default: 50)",
                                "minimum": 1,
                                "maximum": 100,
                                "default": 50
                            }
                        },
                        "required": ["pokemon1", "pokemon2"]
                    }
                }
            ]
        }
    
    async def _handle_call_tool(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Call a specific MCP tool"""
        tool_name = params.get("name", "")
        arguments = params.get("arguments", {})
        
        if tool_name == "battle_simulate":
            pokemon1 = arguments.get("pokemon1", "").lower()
            pokemon2 = arguments.get("pokemon2", "").lower()
            level1 = arguments.get("level1", 50)
            level2 = arguments.get("level2", 50)
            
            if not pokemon1 or not pokemon2:
                raise ValueError("Both pokemon1 and pokemon2 must be specified")
            
            result = await self.battle_tool.simulate_battle(pokemon1, pokemon2, level1, level2)
            
            return {
                "content": [
                    {
                        "type": "text",
                        "text": result.get("summary", "Battle completed")
                    },
                    {
                        "type": "text",
                        "text": f"Detailed log:\n{result.get('battle_log', '')}"
                    }
                ],
                "isError": False
            }
        
        raise ValueError(f"Unknown tool: {tool_name}")