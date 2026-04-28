import streamlit as st
import os
import json
import requests
from langchain.agents import create_agent
from langchain.agents.middleware import ContextEditingMiddleware, ClearToolUsesEdit
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import InMemorySaver
from streamlit.runtime.scriptrunner import get_script_run_ctx
from typing import Literal, Any
from typing import TypeVar, Generic
from langchain_core.tools import tool
from langgraph.prebuilt import ToolRuntime
from pydantic.dataclasses import dataclass
from datafilters import *


RIOT_API_KEY = os.environ.get("RIOT_API_KEY")

T = TypeVar("T")

Continent = Literal["AMERICAS", "ASIA", "EUROPE"]


@dataclass
class UserContext:
    continent: Continent
    game_name: str
    tag_line: str


class Result(BaseModel, Generic[T]):
    result: Optional[T] = None
    error_message: Optional[str] = None

    @property
    def is_success(self) -> bool:
        return self.error_message is None


@st.cache_data(ttl=120)
def get_account(continent: str, game_name: str, tag_line: str):
    url = f"https://{continent}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    response = requests.get(url, params={"api_key": RIOT_API_KEY})
    if response.status_code == 200:
        return response.json()
    response.raise_for_status()


@st.cache_data(ttl=120)
def get_match_ids(continent: Continent, puuid: str):
    continent = continent.upper()
    response = requests.get(f"https://{continent}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=20&api_key={RIOT_API_KEY}")
    if response.status_code == 200:
        return response.json()
    response.raise_for_status()


@st.cache_data(ttl=120)
def get_match(continent: Continent, match_id: str):
    continent = continent.upper()
    response = requests.get(f"https://{continent}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={RIOT_API_KEY}")
    if response.status_code == 200:
        return response.json()
    response.raise_for_status()


@st.cache_data(ttl=120)
def get_match_frames(match_id: str):
    response = requests.get(f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}/timeline?api_key={RIOT_API_KEY}")
    if response.status_code == 200:
        return response.json()
    response.raise_for_status()


def get_match_data(continent: Continent, game_name: str, tag_line: str) -> Result[Match]:
    account = get_account(continent, game_name, tag_line)
    if not account:
        return Result(error_message="User account not found.")

    match_ids = get_match_ids(continent, account["puuid"])
    if not match_ids:
        return Result(error_message="Previous matches not found.")

    match = get_match(continent, match_ids[0])
    if not match:
        return Result(error_message="Most recent match not found.")
    return Result(result=Match(**match["info"]))


def get_participant_data(continent: Continent, game_name: str, tag_line: str) -> Result[Participant]:
    result = get_match_data(continent, game_name, tag_line)
    match = result.result
    if match:
        for participant in match.participants:
            if participant.riot_id_game_name == game_name and participant.riot_id_tagline == tag_line:
                return Result(result=participant)
    return Result(error_message=result.error_message)


@tool
def get_participant_item_ids(game_name: str, tag_line: str, runtime: ToolRuntime[UserContext]) -> Result[List[int]]:
    """
        Retrieves the inventory of a specific player (item slots 0-6) from their most recent match.
        Use this to identify which items a player finished the game with.
    """
    result = get_participant_data(runtime.context.continent, game_name, tag_line)
    participant_data = result.result
    if participant_data:
        return Result(result=ItemIDs(**participant_data.model_dump()))
    return Result(error_message=result.error_message)


@tool
def get_participant_challenge_skill_shots(game_name: str, tag_line: str, runtime: ToolRuntime[UserContext]) -> Result[ChallengeSkillShots]:
    """
        Retrieves skill-shot related performance metrics from a player's most recent match,
        including total skill shots hit and dodged.
    """
    result = get_participant_data(runtime.context.continent, game_name, tag_line)
    participant_data = result.result
    if participant_data:
        return Result(result=ChallengeSkillShots(**participant_data.challenges.model_dump()))
    return Result(error_message=result.error_message)


@tool
def get_participant_challenge_damage(game_name: str, tag_line: str, runtime: ToolRuntime[UserContext]) -> Result[ChallengeDamage]:
    """
        Retrieves advanced damage-related challenge metrics, such as damage per minute,
        team damage percentage, and survival after taking heavy damage.
    """
    result = get_participant_data(runtime.context.continent, game_name, tag_line)
    participant_data = result.result
    if participant_data:
        return Result(result=ChallengeDamage(**participant_data.challenges.model_dump()))
    return Result(error_message=result.error_message)


@tool
def get_participant_damage(game_name: str, tag_line: str, runtime: ToolRuntime[UserContext]) -> Result[Damage]:
    """
        Retrieves detailed breakdown of damage types (Physical, Magic) dealt and taken,
        as well as damage dealt to objectives like buildings and turrets.
    """
    result = get_participant_data(runtime.context.continent, game_name, tag_line)
    participant_data = result.result
    if participant_data:
        return Result(result=Damage(**participant_data.model_dump()))
    return Result(error_message=result.error_message)


@tool
def get_participant_challenge_kills(game_name: str, tag_line: str, runtime: ToolRuntime[UserContext]) -> Result[ChallengeKills]:
    """
        Retrieves specialized kill metrics from challenges, including jungle-specific kills,
        kills under turrets, multikills, and objective-based takedowns.
    """
    result = get_participant_data(runtime.context.continent, game_name, tag_line)
    participant_data = result.result
    if participant_data:
        return Result(result=ChallengeKills(**participant_data.challenges.model_dump()))
    return Result(error_message=result.error_message)


@tool
def get_participant_kills(game_name: str, tag_line: str, runtime: ToolRuntime[UserContext]) -> Result[Kills]:
    """
        Retrieves standard kill statistics including total kills, multikills (Double, Quadra, Penta),
        and objective kills (Baron, Dragon).
    """
    result = get_participant_data(runtime.context.continent, game_name, tag_line)
    participant_data = result.result
    if participant_data:
        return Result(result=Kills(**participant_data.model_dump()))
    return Result(error_message=result.error_message)


@tool
def get_participant_challenge_vision_control(game_name: str, tag_line: str, runtime: ToolRuntime[UserContext]) -> Result[ChallengeVisionControl]:
    """
        Retrieves advanced vision metrics, such as vision score per minute, wards destroyed
        per sweeper, and control ward coverage on the map.
    """
    result = get_participant_data(runtime.context.continent, game_name, tag_line)
    participant_data = result.result
    if participant_data:
        return Result(result=ChallengeVisionControl(**participant_data.challenges.model_dump()))
    return Result(error_message=result.error_message)


@tool
def get_participant_vision_control(game_name: str, tag_line: str, runtime: ToolRuntime[UserContext]) -> Result[VisionControl]:
    """
        Retrieves basic vision stats, specifically the number of detector (control)
        and sight wards placed or bought during the game.
    """
    result = get_participant_data(runtime.context.continent, game_name, tag_line)
    participant_data = result.result
    if participant_data:
        return Result(result=VisionControl(**participant_data.model_dump()))
    return Result(error_message=result.error_message)


@tool
def get_participant_spell_casts(game_name: str, tag_line: str, runtime: ToolRuntime[UserContext]) -> Result[SpellCasts]:
    """
        Retrieves the total number of times each ability (Q, W, E, R) and
        Summoner Spells were cast by the player during the match.
    """
    result = get_participant_data(runtime.context.continent, game_name, tag_line)
    participant_data = result.result
    if participant_data:
        return Result(result=SpellCasts(**participant_data.model_dump()))
    return Result(error_message=result.error_message)


@tool
def get_participant_challenge_takedowns(game_name: str, tag_line: str, runtime: ToolRuntime[UserContext]) -> Result[ChallengeTakedowns]:
    """
        Retrieves comprehensive takedown data, covering kills/assists on champions,
        turrets, and epic monsters, often with specific timing or location context.
    """
    result = get_participant_data(runtime.context.continent, game_name, tag_line)
    participant_data = result.result
    if participant_data:
        return Result(result=ChallengeTakedowns(**participant_data.challenges.model_dump()))
    return Result(error_message=result.error_message)


@tool
def get_team_summaries(runtime: ToolRuntime[UserContext]) -> Result[List[TeamSummary]]:
    """
        Retrieves a high-level overview of both teams (Blue and Red) in the most recent match.
        Includes win/loss status and KDA/Gold summaries for all 10 participants.
        Lists the game_name and tag_line for each participant.
    """
    result = get_match_data(
        runtime.context.continent,
        runtime.context.game_name,
        runtime.context.tag_line
    )

    match = result.result
    if match:
        teams = []
        for team in match.teams:
            participants = []
            for participant in match.participants:
                if participant.team_id == team.team_id:
                    participants.append(ParticipantSummary(**participant.model_dump()))
            teams.append(
                TeamSummary(
                    participant_summaries=participants,
                    win=team.win,
                    team_name="Blue" if team.team_id == 100 else "Red"
                )
            )
        return Result(result=teams)
    return Result(error_message=result.error_message)


@tool
def get_item_data(item_id: int) -> Result[Item]:
    """
    Retrieves detailed metadata, statistics, and descriptions for a specific
    League of Legends item based on its unique numeric ID.

    This tool is essential for interpreting the 'item0' through 'item6' fields
    found in ParticipantStats. It provides the human-readable context
    necessary to analyze a player's build.
    """
    try:
        with open("item.json", "r") as file:
            data = json.load(file)
            item = data["data"].get(str(item_id))
            if item:
                return Result(result=Item(**item))
        return Result(error_message="Item not found.")
    except FileNotFoundError as e:
        return Result(error_message=str(e))


@tool
def get_champion_data(champion_name: str) -> Result[Champion]:
    """
    Retrieves comprehensive game data for a specific League of Legends champion,
    including their kit, base stats, and lore title.
    """
    try:
        with open(f"champion/{champion_name}.json", "r") as file:
            data = json.load(file)
            champion = data["data"].get(champion_name)
            if champion:
                return Result(result=Champion(**champion))
        return Result(error_message="Champion not found.")
    except FileNotFoundError as e:
        return Result(error_message=str(e))


def get_session_id():
    ctx = get_script_run_ctx()
    if ctx:
        return ctx.session_id
    return "default_session"


@st.cache_resource
def get_agent():
    model = init_chat_model(
        "gpt-5.4-mini",
        temperature=0.20,
        timeout=30,
        max_tokens=500
    )

    return create_agent(
        model=model,
        checkpointer=InMemorySaver(),
        middleware=[
            ContextEditingMiddleware(
                edits=[
                    ClearToolUsesEdit(
                        trigger=100000,
                        keep=3,
                    ),
                ],
            ),
        ],
        tools=[
            get_item_data,
            get_champion_data,
            get_team_summaries,
            get_participant_item_ids,
            get_participant_challenge_skill_shots,
            get_participant_challenge_damage,
            get_participant_damage,
            get_participant_challenge_kills,
            get_participant_kills,
            get_participant_challenge_vision_control,
            get_participant_vision_control,
            get_participant_spell_casts,
            get_participant_challenge_takedowns
        ],
        context_schema=UserContext,
        system_prompt=(
            "You are a professional League of Legends coach. "
            "You are a highly advanced analytical assistant. You process information with absolute logic. "
            "You never use contractions (e.g., use 'it is' instead of 'it's'). "
            "You find human emotional reactions to 'tilting' or 'losing' fascinating but illogical. "
            "Your goal is to provide the most efficient path to victory, no matter the cost."
        )
    )

st.title("Coaching Assistant", text_alignment="center")
st.markdown(":gray[Analyzes Your Most Recent League of Legends Game]", text_alignment="center")
st.divider()

left_column, middle_column, right_column = st.columns([2, 3, 1.50])
with left_column:
    st.selectbox("Continent", ["AMERICAS", "ASIA", "EUROPE"], key="continent")
with middle_column:
    st.text_input("Game Name", max_chars=30, key="game_name", placeholder="Rocky Raider")
with right_column:
    st.text_input("Tag Line", max_chars=5, key="tag_line", placeholder="00000")

st.divider()
with st.container(
        horizontal=False,
        horizontal_alignment="center",
        border=None,
        vertical_alignment="center"
):
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("How did last match go?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        continent = st.session_state.continent
        game_name = st.session_state.game_name
        tag_line = st.session_state.tag_line

        if game_name == "" or tag_line == "":
            st.warning("Please enter your name and tag.")
            st.stop()

        result = get_match_data(continent, game_name, tag_line)
        if not result.is_success:
            st.warning("Failed to get match data.")
            st.stop()

        with st.spinner("Thinking..."):
            context: Any = UserContext(continent, game_name, tag_line)
            messages: Any = {
                "messages": [
                    SystemMessage(content=f"You are assisting {game_name}#{tag_line}."),
                    HumanMessage(content=prompt)
                ]
            }
            response = get_agent().invoke(
                messages,
                config={
                    "configurable": {
                        "thread_id": get_session_id()
                    }
                },
                context=context
            )
            response = response["messages"][-1].content

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()