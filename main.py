from typing import Any, Annotated, Union
from dataclasses import dataclass
from langchain_classic.agents import create_openai_tools_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import StructuredTool
from langchain_openai import ChatOpenAI
from langchain.tools import tool, InjectedToolArg
from langchain_core.messages import SystemMessage, HumanMessage
from merakiapi import GetItemById, GetChampionByName, SummarizeItem, SummarizeChampion
from riotapi import GetAccount, GetMatchIds, GetMatch, Continent, Region, SummarizeMatch


@dataclass
class UserContext:
    Account: Any
    Continent: Continent
    Region: Region


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


def Main(continent: Continent, region: Region, game_name: str, tag_line: str):
    account = GetAccount(continent, game_name, tag_line)
    if not account:
        print("No account was found")
        return

    context = UserContext(account, continent, region)

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
                Use your tools.
            """),
            HumanMessage(content="""
                Give me an overview of my last match.
                Did I build the correct items this game, and if not, what items should I have been building?
                How was my map positioning? Did I ward in the correct places? Was I helping my team with objectives?
                What suggestions do you have specifically for my champion? Did I play show good mechanical skill?
            """)
        ]
    }

    agent.invoke(messages)


if __name__ == "__main__":
    Main("AMERICAS", "NA1", "Rocky Raider", "00000")