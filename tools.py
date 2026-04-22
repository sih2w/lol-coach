import json
from typing import List, Optional, Dict, Union, TypedDict
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.tools import tool
from langgraph.prebuilt import ToolRuntime
from pydantic import BaseModel, ConfigDict, AliasGenerator
from pydantic.alias_generators import to_camel
from pydantic.dataclasses import dataclass
from riotapi import Continent, get_account, get_match_ids, get_match


class ParticipantChallenges(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_camel,
        ),
        populate_by_name=True
    )

    baron_buff_gold_advantage_over_threshold: Optional[float] = None
    control_ward_time_coverage_in_river_or_enemy_half: Optional[float] = None
    earliest_baron: Optional[float] = None
    earliest_dragon_takedown: Optional[float] = None
    earliest_elder_dragon: Optional[float] = None
    early_laning_phase_gold_exp_advantage: Optional[float] = None
    faster_support_quest_completion: Optional[int] = None
    fastest_legendary: Optional[float] = None
    had_afk_teammate: Optional[int] = None
    highest_champion_damage: Optional[int] = None
    highest_crowd_control_score: Optional[int] = None
    highest_ward_kills: Optional[int] = None
    jungler_kills_early_jungle: Optional[int] = None
    kills_on_laners_early_jungle_as_jungler: Optional[int] = None
    laning_phase_gold_exp_advantage: Optional[float] = None
    legendary_count: Optional[int] = None
    max_cs_advantage_on_lane_opponent: Optional[float] = None
    max_level_lead_lane_opponent: Optional[int] = None
    most_wards_destroyed_one_sweeper: Optional[int] = None
    mythic_item_used: Optional[int] = None
    played_champ_select_position: Optional[int] = None
    solo_turrets_lategame: Optional[int] = None
    takedowns_first25_minutes: Optional[int] = None
    teleport_takedowns: Optional[int] = None
    third_inhibitor_destroyed_time: Optional[float] = None
    three_wards_one_sweeper_count: Optional[int] = None
    vision_score_advantage_lane_opponent: Optional[float] = None
    infernal_scale_pickup: Optional[int] = None
    fist_bump_participation: Optional[int] = None
    void_monster_kill: Optional[int] = None
    ability_uses: Optional[int] = None
    aces_before15_minutes: Optional[int] = None
    allied_jungle_monster_kills: Optional[float] = None
    baron_takedowns: Optional[int] = None
    blast_cone_opposite_opponent_count: Optional[int] = None
    bounty_gold: Optional[float] = None
    buffs_stolen: Optional[int] = None
    complete_support_quest_in_time: Optional[int] = None
    control_wards_placed: Optional[int] = None
    damage_per_minute: Optional[float] = None
    damage_taken_on_team_percentage: Optional[float] = None
    danced_with_rift_herald: Optional[int] = None
    deaths_by_enemy_champs: Optional[int] = None
    dodge_skill_shots_small_window: Optional[int] = None
    double_aces: Optional[int] = None
    dragon_takedowns: Optional[int] = None
    legendary_item_used_list: List[int] = []
    effective_heal_and_shielding: Optional[float] = None
    elder_dragon_kills_with_opposing_soul: Optional[int] = None
    elder_dragon_multikills: Optional[int] = None
    enemy_champion_immobilizations: Optional[int] = None
    enemy_jungle_monster_kills: Optional[float] = None
    epic_monster_kills_near_enemy_jungler: Optional[int] = None
    epic_monster_kills_within30_seconds_of_spawn: Optional[int] = None
    epic_monster_steals: Optional[int] = None
    epic_monster_stolen_without_smite: Optional[int] = None
    first_turret_killed: Optional[int] = None
    first_turret_killed_time: Optional[float] = None
    flawless_aces: Optional[int] = None
    full_team_takedown: Optional[int] = None
    game_length: Optional[float] = None
    get_takedowns_in_all_lanes_early_jungle_as_laner: Optional[int] = None
    gold_per_minute: Optional[float] = None
    had_open_nexus: Optional[int] = None
    immobilize_and_kill_with_ally: Optional[int] = None
    initial_buff_count: Optional[int] = None
    initial_crab_count: Optional[int] = None
    jungle_cs_before10_minutes: Optional[float] = None
    jungler_takedowns_near_damaged_epic_monster: Optional[int] = None
    kda: Optional[float] = None
    kill_after_hidden_with_ally: Optional[int] = None
    killed_champ_took_full_team_damage_survived: Optional[int] = None
    killing_sprees: Optional[int] = None
    kill_participation: Optional[float] = None
    kills_near_enemy_turret: Optional[int] = None
    kills_on_other_lanes_early_jungle_as_laner: Optional[int] = None
    kills_on_recently_healed_by_aram_pack: Optional[int] = None
    kills_under_own_turret: Optional[int] = None
    kills_with_help_from_epic_monster: Optional[int] = None
    knock_enemy_into_team_and_kill: Optional[int] = None
    k_turrets_destroyed_before_plates_fall: Optional[int] = None
    land_skill_shots_early_game: Optional[int] = None
    lane_minions_first10_minutes: Optional[int] = None
    lost_an_inhibitor: Optional[int] = None
    max_kill_deficit: Optional[int] = None
    mejais_full_stack_in_time: Optional[int] = None
    more_enemy_jungle_than_opponent: Optional[float] = None
    multi_kill_one_spell: Optional[int] = None
    multikills: Optional[int] = None
    multikills_after_aggressive_flash: Optional[int] = None
    multi_turret_rift_herald_count: Optional[int] = None
    outer_turret_executes_before10_minutes: Optional[int] = None
    outnumbered_kills: Optional[int] = None
    outnumbered_nexus_kill: Optional[int] = None
    perfect_dragon_souls_taken: Optional[int] = None
    perfect_game: Optional[int] = None
    pick_kill_with_ally: Optional[int] = None
    poro_explosions: Optional[int] = None
    quick_cleanse: Optional[int] = None
    quick_first_turret: Optional[int] = None
    quick_solo_kills: Optional[int] = None
    rift_herald_takedowns: Optional[int] = None
    save_ally_from_death: Optional[int] = None
    scuttle_crab_kills: Optional[int] = None
    shortest_time_to_ace_from_first_takedown: Optional[float] = None
    skillshots_dodged: Optional[int] = None
    skillshots_hit: Optional[int] = None
    snowballs_hit: Optional[int] = None
    solo_baron_kills: Optional[int] = None
    solo_kills: Optional[int] = None
    stealth_wards_placed: Optional[int] = None
    survived_single_digit_hp_count: Optional[int] = None
    survived_three_immobilizes_in_fight: Optional[int] = None
    takedown_on_first_turret: Optional[int] = None
    takedowns: Optional[int] = None
    takedowns_after_gaining_level_advantage: Optional[int] = None
    takedowns_before_jungle_minion_spawn: Optional[int] = None
    takedowns_first_x_minutes: Optional[int] = None
    takedowns_in_alcove: Optional[int] = None
    takedowns_in_enemy_fountain: Optional[int] = None
    team_baron_kills: Optional[int] = None
    team_damage_percentage: Optional[float] = None
    team_elder_dragon_kills: Optional[int] = None
    team_rift_herald_kills: Optional[int] = None
    took_large_damage_survived: Optional[int] = None
    turret_plates_taken: Optional[int] = None
    turrets_taken_with_rift_herald: Optional[int] = None
    turret_takedowns: Optional[int] = None
    twenty_minions_in3_seconds_count: Optional[int] = None
    two_wards_one_sweeper_count: Optional[int] = None
    unseen_recalls: Optional[int] = None
    vision_score_per_minute: Optional[float] = None
    wards_guarded: Optional[int] = None
    ward_takedowns: Optional[int] = None
    ward_takedowns_before20_min: Optional[int] = None


class User(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_camel,
        ),
        populate_by_name=True
    )

    riot_id_game_name: Optional[str] = None
    riot_id_tagline: Optional[str] = None
    champion_name: Optional[str] = None
    team_position: Optional[str] = None
    team_id: Optional[int] = None
    puuid: Optional[str] = None
    kills: Optional[int] = None
    deaths: Optional[int] = None
    assists: Optional[int] = None
    bounty_level: Optional[int] = None
    champ_experience: Optional[int] = None
    champ_level: Optional[int] = None
    largest_killing_spree: Optional[int] = None
    largest_multi_kill: Optional[int] = None
    double_kills: Optional[int] = None
    quadra_kills: Optional[int] = None
    penta_kills: Optional[int] = None
    damage_dealt_to_buildings: Optional[int] = None
    damage_dealt_to_objectives: Optional[int] = None
    damage_dealt_to_turrets: Optional[int] = None
    damage_self_mitigated: Optional[int] = None
    magic_damage_dealt: Optional[int] = None
    magic_damage_dealt_to_champions: Optional[int] = None
    magic_damage_taken: Optional[int] = None
    physical_damage_dealt: Optional[int] = None
    physical_damage_dealt_to_champions: Optional[int] = None
    physical_damage_taken: Optional[int] = None
    baron_kills: Optional[int] = None
    dragon_kills: Optional[int] = None
    inhibitor_kills: Optional[int] = None
    inhibitor_takedowns: Optional[int] = None
    inhibitors_lost: Optional[int] = None
    objectives_stolen: Optional[int] = None
    objectives_stolen_assists: Optional[int] = None
    detector_wards_placed: Optional[int] = None
    sight_wards_bought_in_game: Optional[int] = None
    first_blood_assist: Optional[bool] = None
    first_blood_kill: Optional[bool] = None
    first_tower_assist: Optional[bool] = None
    first_tower_kill: Optional[bool] = None
    game_ended_in_surrender: Optional[bool] = None
    team_early_surrendered: Optional[bool] = None
    longest_time_spent_living: Optional[int] = None
    gold_earned: Optional[int] = None
    gold_spent: Optional[int] = None
    neutral_minions_killed: Optional[int] = None
    item0: Optional[int] = None
    item1: Optional[int] = None
    item2: Optional[int] = None
    item3: Optional[int] = None
    item4: Optional[int] = None
    item5: Optional[int] = None
    item6: Optional[int] = None
    spell1_casts: Optional[int] = None
    spell2_casts: Optional[int] = None
    spell3_casts: Optional[int] = None
    spell4_casts: Optional[int] = None
    summoner1_casts: Optional[int] = None
    summoner2_casts: Optional[int] = None
    challenges: Optional[ParticipantChallenges] = None


class Participant(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_camel
        ),
        populate_by_name=True
    )

    riot_id_game_name: Optional[str] = None
    riot_id_tagline: Optional[str] = None
    champion_name: Optional[str] = None
    team_position: Optional[str] = None
    team_id: Optional[int] = None
    puuid: Optional[str] = None
    kills: Optional[int] = None
    deaths: Optional[int] = None
    assists: Optional[int] = None
    gold_earned: Optional[int] = None
    gold_spent: Optional[int] = None


class Spell(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_camel
        ),
        populate_by_name=True
    )

    name: Optional[str] = None
    description: Optional[str] = None
    cooldown: Optional[List[Union[int, float]]] = None
    cost: Optional[List[Union[int, float]]] = None
    range: Optional[List[Union[int, float]]] = None


class Passive(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_camel
        ),
        populate_by_name=True
    )

    name: Optional[str] = None
    description: Optional[str] = None


class Champion(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_camel
        ),
        populate_by_name=True
    )

    title: Optional[str] = None
    tags: Optional[List[str]] = None
    stats: Optional[Dict[str, Union[int, float]]] = None
    spells: Optional[List[Spell]] = None
    passive: Optional[Passive] = None


class Item(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_camel
        ),
        populate_by_name=True
    )

    name: Optional[str] = None
    description: Optional[str] = None
    plaintext: Optional[str] = None
    tags: Optional[List[str]] = None
    stats: Optional[Dict[str, Union[int, float]]] = None


class Objective(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_camel
        ),
        populate_by_name=True
    )

    first: Optional[bool] = None
    kills: Optional[int] = None


class Objectives(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_camel
        ),
        populate_by_name=True
    )

    baron: Optional[Objective] = None
    champion: Optional[Objective] = None
    dragon: Optional[Objective] = None
    horde: Optional[Objective] = None
    inhibitor: Optional[Objective] = None
    rift_herald: Optional[Objective] = None
    tower: Optional[Objective] = None


class Team(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_camel
        ),
        populate_by_name=True
    )

    team_id: Optional[int] = None
    win: Optional[bool] = None
    objectives: Optional[Objectives] = None


@dataclass
class UserContext:
    continent: Continent
    game_name: str
    tag_line: str


class MatchData(TypedDict):
    user: User
    others: List[Participant]
    teams: List[Team]


search = DuckDuckGoSearchResults()


@tool
def get_recent_match_data(runtime: ToolRuntime[UserContext]) -> Optional[MatchData]:
    """
    Fetches comprehensive telemetry and performance data for the most recent
    League of Legends match played by the user defined in the UserContext.

    Returns:
        MatchData: A dictionary containing 'others' (List[Participant])
        and 'teams' (List[Team]) amd 'user' (User). Returns None if no recent match is found
        or the API request fails.
    """
    continent = runtime.context.continent
    game_name = runtime.context.game_name
    tag_line = runtime.context.tag_line

    account = get_account(continent, game_name, tag_line)
    if not account:
        return None

    match_ids = get_match_ids(continent, account["puuid"])
    if not match_ids:
        return None

    match = get_match(continent, match_ids[0])
    if not match:
        return None

    participants: List[Participant] = []
    user = None

    for participant in match["info"]["participants"]:
        if participant["puuid"] == account["puuid"]:
            user = User(**participant)
        else:
            participant = Participant(**participant)
            participants.append(participant)

    if not user:
        return None

    return {
        "user": user,
        "others": participants,
        "teams": [Team(**team) for team in match["info"]["teams"]],
    }


@tool
def get_item_data(item_id: int) -> Optional[Item]:
    """
    Retrieves detailed metadata, statistics, and descriptions for a specific
    League of Legends item based on its unique numeric ID.

    This tool is essential for interpreting the 'item0' through 'item6' fields
    found in ParticipantStats. It provides the human-readable context
    necessary to analyze a player's build.

    Args:
        item_id (int): The unique integer identifier for the item (e.g., 3089 for Rabadon's Deathcap).

    Returns:
        Optional[Item]: An Item model containing game data, or None if the ID is invalid
        or represents an empty inventory slot (ID 0).
    """
    try:
        item_id = str(item_id)
        with open("item.json", "r") as file:
            data = json.load(file)
            items = data["data"]
            for key, item in items.items():
                if key == item_id:
                    return Item(**item)
    except FileNotFoundError:
        return None


@tool
def get_champion_data(champion_name: str) -> Optional[Champion]:
    """
    Retrieves comprehensive game data for a specific League of Legends champion,
    including their kit, base stats, and lore title.

    This tool provides the mechanical context for a champion's performance
    in a match. Use it to understand the specific abilities (spells) and
    scaling factors that influenced the MatchData results.

    The returned 'Champion' object includes:
    - **Identity**: The champion's official title and thematic tags (e.g., 'Mage', 'Assassin').
    - **Stats**: Base attributes such as Health, Armor, Attack Damage, and
      scaling values per level.
    - **Spells**: A list of the four active abilities (Q, W, E, R), including
      their names, descriptions, cooldowns, and resource costs.
    - **Passive**: Details on the champion's innate ability that doesn't
      require a keypress but often defines their playstyle

    Args:
        champion_name (str): The exact name of the champion (e.g., "Aatrox", "KaiSa", "LeeSin").
                             Note: Names should generally follow the Riot API naming
                             convention (case-sensitive, usually removing spaces/apostrophes).

    Returns:
        Optional[Champion]: A Champion model containing the full data profile,
        or None if the champion name is not found.
    """
    try:
        with open(f"champion/{champion_name}.json", "r") as file:
            data = json.load(file)
            champion = data["data"][champion_name]
            champion = Champion(**champion)
            return champion
    except FileNotFoundError:
        return None

