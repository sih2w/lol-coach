import streamlit as st
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import after_model
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, RemoveMessage, SystemMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.runtime import Runtime
from riotapi import Continent
from tools import get_item_data, get_champion_data, UserContext, search, get_recent_match_data
from streamlit.runtime.scriptrunner import get_script_run_ctx


def get_session_id():
    ctx = get_script_run_ctx()
    if ctx:
        return ctx.session_id
    return "default_session"

@after_model
def delete_old_messages(state: AgentState, runtime: Runtime) -> dict:
    messages = state["messages"]
    if len(messages) > 15:
        return {"messages": [RemoveMessage(id=m.id) for m in messages[:2]]}
    return {}

if "agent" not in st.session_state:
    model = init_chat_model(
        "gpt-5.4-nano",
        temperature=0.20,
        timeout=30,
        max_tokens=1000,
    )

    st.session_state.agent = create_agent(
        model=model,
        checkpointer=InMemorySaver(),
        middleware=[delete_old_messages],
        tools=[
            get_recent_match_data,
            get_item_data,
            get_champion_data,
            search
        ],
        context_schema=UserContext,
        system_prompt=(
            "You are a professional League of Legends coach. "
            "Be informative and funny. Limit your conversations to League of Legends. "
            "Keep it simple. Do not tell the user's the IDs items or teams. Use words. "
        )
    )

def ask(continent: Continent, game_name: str, tag_line: str, prompt: str) -> str:
    session_id = get_session_id()
    config = {"configurable": {"thread_id": session_id}}
    context = UserContext(continent, game_name, tag_line)
    response = st.session_state.agent.invoke(
        {
            "messages": [
                SystemMessage(f"You are assisting {game_name}#{tag_line}."),
                HumanMessage(prompt)
            ]
        },
        config=config,
        context=context,
    )
    return response["messages"][-1].content

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
        st.selectbox("Continent", ["AMERICAS", "ASIA", "EUROPE"], key="continent")
    with middle_column:
        st.text_input("Game Name", max_chars=30, key="game_name", placeholder="Rocky Raider")
    with right_column:
        st.text_input("Tag Line", max_chars=5, key="tag_input", placeholder="00000")

    st.text_area("Prompt", max_chars=200, key="prompt", placeholder="What items did I build last game?")

    with st.container(horizontal=True, horizontal_alignment="center", vertical_alignment="center"):
        submit_button = st.form_submit_button(
            "Analyze Last Match",
            disabled=st.session_state.is_loading,
            on_click=handle_click,
            use_container_width=False
        )

if st.session_state.is_loading:
    if not st.session_state.game_name or not st.session_state.tag_input or not st.session_state.prompt:
        st.session_state["error_msg"] = "Please fill in all fields!"
        st.session_state.is_loading = False
        st.rerun()
    else:
        with st.spinner("Coach is analyzing..."):
            try:
                response = ask(
                    st.session_state.continent,
                    st.session_state.game_name,
                    st.session_state.tag_input,
                    st.session_state.prompt
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