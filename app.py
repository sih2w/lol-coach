from typing import Any
from dataclasses import dataclass
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.prebuilt import ToolRuntime
from riotapi import GetAccount, GetMatchIds, GetMatch, Continent, SummarizeMatch
import streamlit as st


@dataclass
class UserContext:
    account: Any
    continent: Continent


Search = DuckDuckGoSearchResults()


@tool
def GetRecentMatchTool(runtime: ToolRuntime[UserContext]):
    """Retrieve the user's most recent match data."""
    match_ids = GetMatchIds(runtime.context.continent, runtime.context.account["puuid"])

    if match_ids and len(match_ids) > 0:
        match = GetMatch(runtime.context.continent, match_ids[0])
        return SummarizeMatch(match, runtime.context.account["puuid"])

    return "Match not found"


def Ask(continent: Continent, game_name: str, tag_line: str):
    account = GetAccount(continent, game_name, tag_line)
    if not account:
        return "I wasn't able to find your account. Please check your spelling and try again."

    agent = create_agent(
        model="gpt-4o-mini",
        tools=[
            GetRecentMatchTool,
            Search
        ],
        context_schema=UserContext
    )

    messages: Any = {
        "messages":[
            SystemMessage(content=(
                "You are a professional League of Legends coach."
                "Use your search tool to find information about League of Legends when needed."
                f"You are assisting puuid {account["puuid"]}, but address them as {game_name}. "
            )),
            HumanMessage(content=(
                "I need a detailed review of my last match. Please analyze and provide a section for each of the following:\n"
                "1. Itemization: Based on my opponents' builds and damage types, were my items optimal?\n"
                "2. Map Positioning: Look at my death locations and objective participation. Was I in the right spots?\n"
                "3. Vision: Analyze my ward placement and vision score. Was it efficient?"
            ))
        ]
    }

    response = agent.invoke(
        messages,
        context=UserContext(account, continent),
    )

    print(response)

    return response["messages"][-1].content


if __name__ == "__main__":
    if "output" not in st.session_state:
        st.session_state["output"] = None
    if "error_msg" not in st.session_state:
        st.session_state["error_msg"] = None
    if "is_loading" not in st.session_state:
        st.session_state["is_loading"] = False

    def handle_click():
        if not st.session_state.is_loading:
            st.session_state.is_loading = True
            st.session_state["output"] = None
            st.session_state["error_msg"] = None

    _, middle_column, _ = st.columns([1, 3, 1])
    with middle_column:
        st.title("Coaching Assistant", text_alignment="center")

    with st.form("coach_form"):
        left_column, middle_column, right_column = st.columns([2, 3, 1.50])
        with left_column:
             st.selectbox("Continent", ["Americas", "Asia", "Europe"], key="continent")
        with middle_column:
            st.text_input("Game Name", max_chars=30, key="game_name")
        with right_column:
            st.text_input("Tag Line", max_chars=5, key="tag_input")

        with st.container(horizontal=True, horizontal_alignment="center", vertical_alignment="center"):
            submit_button = st.form_submit_button(
                "Analyze Last Match",
                disabled=st.session_state.is_loading,
                on_click=handle_click,
                use_container_width=False
            )

    if st.session_state.is_loading:
        if not st.session_state.game_name or not st.session_state.tag_input:
            st.session_state["error_msg"] = "Please fill in all fields!"
            st.session_state.is_loading = False
            st.rerun()
        else:
            with st.spinner("Coach is analyzing..."):
                try:
                    response = Ask(
                        st.session_state.continent,
                        st.session_state.game_name,
                        st.session_state.tag_input
                    )
                    st.session_state["output"] = response
                except Exception as e:
                    st.session_state["error_msg"] = f"Analysis failed: {str(e)}"
                finally:
                    st.session_state.is_loading = False
                    st.rerun()

    if st.session_state["error_msg"]:
        st.error(st.session_state["error_msg"])

    if st.session_state["output"]:
        with st.container(border=True):
            st.write(st.session_state["output"])