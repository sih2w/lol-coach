from typing import Any, Annotated, Union
from dataclasses import dataclass
from langchain_classic.agents import create_openai_tools_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import StructuredTool
from langchain_openai import ChatOpenAI
from langchain.tools import tool, InjectedToolArg
from langchain_core.messages import SystemMessage, HumanMessage
from merakiapi import GetItemById, GetChampionByName, SummarizeItem, SummarizeChampion
from riotapi import GetAccount, GetMatchIds, GetMatch, Continent, SummarizeMatch
import streamlit as st


@dataclass
class UserContext:
    Account: Any
    Continent: Continent


@tool
def GetItemByIdTool(item_id: Union[str, int]) -> Any:
    """
    Returns information about an item given its ID.
    Use this tool to get an item's name and description.
    """
    item = GetItemById(item_id)
    if item:
        return SummarizeItem(item)


@tool
def GetChampionByNameTool(champion_name: str) -> Any:
    """
    Returns information about a champion given its name.
    Pass champion name to get information about that champion.
    """
    champion = GetChampionByName(champion_name)
    if champion:
        return SummarizeChampion(champion)


@tool
def GetRecentMatchTool(context: Annotated[UserContext, InjectedToolArg]):
    """
    Returns information about the user's most recent match.
    """
    match_ids = GetMatchIds(context.Continent, context.Account)
    if match_ids and len(match_ids) > 0:
        match = GetMatch(context.Continent, match_ids[0])
        return SummarizeMatch(match, context.Account["puuid"])

    return "Match not found"


def CreateAgent(tools):
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.8,
        max_tokens=1000,
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a professional League of Legends coach."),
        MessagesPlaceholder(variable_name="messages"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_openai_tools_agent(llm, tools, prompt)

    return AgentExecutor(agent=agent, tools=tools, verbose=True)


def Ask(continent: Continent, game_name: str, tag_line: str):
    account = GetAccount(continent, game_name, tag_line)
    if not account:
        return "I wasn't able to find your account. Please check your spelling and try again."

    context = UserContext(account, continent)

    tools = [
        StructuredTool.from_function(
            name="GetRecentMatchTool",
            func=lambda: GetRecentMatchTool.invoke({"context": context}),
            description="Returns information about the user's most recent match."
        ),
        GetItemByIdTool,
        GetChampionByNameTool,
    ]

    agent = CreateAgent(tools)

    messages: Any = {
        "messages": [
            SystemMessage(f"""
                You are assisting {account["puuid"]}.
                Address them by their game name.
                Use GetRecentMatchTool to retrieve the most recent match.
                Use GetItemByIdTool to map item IDs to item names.
                Use GetChampionByNameTool to map champion names to champion abilities. 
            """),
            HumanMessage(content="""
                Give me an overview of my last match.
                Who was my lane opponent? How did I do against them early?
                What items did I build? Should I have built different items?
                How was my map positioning? Did I rotate for objectives?
                What suggestions do you have specifically for my champion? Was I using my abilities efficiently?
            """)
        ]
    }

    return agent.invoke(messages)["output"]


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