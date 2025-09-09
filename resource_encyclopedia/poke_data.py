"""
Pokémon Data Resource
MCP Resource implementation for Pokémon data access
"""
import httpx
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class PokemonDataResource:
    def __init__(self):
        self.base_url = "https://pokeapi.co/api/v2"
        self.cache = {}
        self.move_cache = {}

    async def get_pokemon_data(self, pokemon_name: str) -> Dict[str, Any]:
        """Get comprehensive Pokémon data"""
        if pokemon_name in self.cache:
            return self.cache[pokemon_name]

        try:
            async with httpx.AsyncClient() as client:
                pokemon_response = await client.get(f"{self.base_url}/pokemon/{pokemon_name}")
                pokemon_response.raise_for_status()
                pokemon_data = pokemon_response.json()

                species_response = await client.get(pokemon_data["species"]["url"])
                species_response.raise_for_status()
                species_data = species_response.json()

                evolution_data = None
                if species_data.get("evolution_chain"):
                    evolution_response = await client.get(species_data["evolution_chain"]["url"])
                    evolution_response.raise_for_status()
                    evolution_data = evolution_response.json()

                processed_data = await self._process_pokemon_data(pokemon_data, species_data, evolution_data)
                self.cache[pokemon_name] = processed_data
                return processed_data

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ValueError(f"Pokémon '{pokemon_name}' not found")
            raise ValueError(f"Error fetching Pokémon data: {e}")
        except Exception as e:
            raise ValueError(f"Error processing Pokémon data: {e}")

    async def _process_pokemon_data(
        self, pokemon_data: Dict, species_data: Dict, evolution_data: Optional[Dict]
    ) -> Dict[str, Any]:
        """Process API data into structured format"""

        # Base stats
        base_stats = {}
        for stat in pokemon_data["stats"]:
            stat_name = stat["stat"]["name"].replace("-", "_")
            base_stats[stat_name] = stat["base_stat"]

        # Types
        types = [type_info["type"]["name"] for type_info in pokemon_data["types"]]

        # Abilities
        abilities = []
        for ability in pokemon_data["abilities"]:
            abilities.append(
                {
                    "name": ability["ability"]["name"],
                    "is_hidden": ability["is_hidden"],
                    "slot": ability["slot"],
                }
            )

        # Moves (limit to first 20 for simplicity)
        moves = []
        for move in pokemon_data["moves"][:20]:
            move_name = move["move"]["name"]
            move_details = await self._get_move_details(move["move"]["url"])
            moves.append(
                {
                    "name": move_name,
                    "details": move_details,
                }
            )

        # Evolution chain
        evolution_chain = []
        if evolution_data:
            evolution_chain = self._process_evolution_chain(evolution_data["chain"])

        return {
            "id": pokemon_data["id"],
            "name": pokemon_data["name"],
            "height": pokemon_data["height"],
            "weight": pokemon_data["weight"],
            "base_stats": base_stats,
            "types": types,
            "abilities": abilities,
            "moves": moves,
            "evolution_chain": evolution_chain,
            "sprites": {
                "front_default": pokemon_data["sprites"]["front_default"],
                "back_default": pokemon_data["sprites"]["back_default"],
                "front_shiny": pokemon_data["sprites"]["front_shiny"],
            },
            "base_experience": pokemon_data["base_experience"],
            "generation": species_data.get("generation", {}).get("name", "unknown"),
        }

    async def _get_move_details(self, move_url: str) -> Dict[str, Any]:
        """Get detailed move information"""
        if move_url in self.move_cache:
            return self.move_cache[move_url]

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(move_url)
                response.raise_for_status()
                move_data = response.json()

                details = {
                    "type": move_data.get("type", {}).get("name", "normal"),
                    "category": move_data.get("damage_class", {}).get("name", "physical"),
                    "power": move_data.get("power"),
                    "accuracy": move_data.get("accuracy"),
                    "pp": move_data.get("pp", 0),
                    "priority": move_data.get("priority", 0),
                    "effect_chance": move_data.get("effect_chance"),
                    "effect_entries": [
                        entry["effect"]
                        for entry in move_data.get("effect_entries", [])
                        if entry["language"]["name"] == "en"
                    ][:1],
                }

                self.move_cache[move_url] = details
                return details
        except Exception:
            return {
                "type": "normal",
                "category": "physical",
                "power": 40,
                "accuracy": 100,
                "pp": 35,
                "priority": 0,
            }

    def _process_evolution_chain(self, chain_data: Dict) -> List[Dict[str, Any]]:
        """Process evolution chain data recursively"""
        evolution_chain = []

        def process_chain(chain):
            pokemon_name = chain["species"]["name"]
            evolution_info = {
                "name": pokemon_name,
                "evolution_details": [],
            }

            for detail in chain.get("evolution_details", []):
                evolution_info["evolution_details"].append(
                    {
                        "min_level": detail.get("min_level"),
                        "trigger": detail.get("trigger", {}).get("name"),
                        "item": detail.get("item", {}).get("name") if detail.get("item") else None,
                        "min_happiness": detail.get("min_happiness"),
                        "time_of_day": detail.get("time_of_day"),
                    }
                )

            evolution_chain.append(evolution_info)

            for evolved_form in chain.get("evolves_to", []):
                process_chain(evolved_form)

        process_chain(chain_data)
        return evolution_chain

    async def list_all_pokemon(self) -> Dict[str, Any]:
        """List of all available Pokémon"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/pokemon?limit=1010")
                response.raise_for_status()
                data = response.json()

                return {
                    "count": data["count"],
                    "pokemon": [pokemon["name"] for pokemon in data["results"]],
                }
        except Exception as e:
            raise ValueError(f"Error fetching Pokémon list: {e}")

    async def get_type_effectiveness(self, attacking_type: str) -> Dict[str, List[str]]:
        """Get effectiveness data for a type"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/type/{attacking_type}")
                response.raise_for_status()
                type_data = response.json()

                return {
                    "double_damage_to": [t["name"] for t in type_data["damage_relations"]["double_damage_to"]],
                    "half_damage_to": [t["name"] for t in type_data["damage_relations"]["half_damage_to"]],
                    "no_damage_to": [t["name"] for t in type_data["damage_relations"]["no_damage_to"]],
                }
        except Exception as e:
            raise ValueError(f"Error fetching type effectiveness: {e}")
