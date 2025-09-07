import os
import operator
from typing import TypedDict, Annotated

from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage, BaseMessage
from langchain_groq import ChatGroq

import sib_api_v3_sdk
from sib_api_v3_sdk.models import SendSmtpEmail

# --- Load environment variables ---
load_dotenv()

CURRENT_YEAR = 2025

# -----------------------------
# Define State Schema
# -----------------------------
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]

# -----------------------------
# Prompts
# -----------------------------
TOOLS_SYSTEM_PROMPT = f"""You are a travel assistant.
- Use tools to find flights, hotels, and attractions.
- Current year: {CURRENT_YEAR}.
- Return structured, helpful results.
"""

EMAILS_SYSTEM_PROMPT = """Convert structured text into clean HTML for email content."""

# -----------------------------
# Tools
# -----------------------------
from agents.tools.flights_finder import flights_finder
from agents.tools.hotels_finder import hotels_finder
from agents.tools.attractions_finder import attractions_finder  # ✅ now a proper tool

TOOLS = [flights_finder, hotels_finder, attractions_finder]

# -----------------------------
# Agent Class
# -----------------------------
class Agent:
    def __init__(self):
        # Groq LLM
        self.llm = ChatGroq(model="llama-3.3-70b-versatile")

        # Tool dictionary
        self.tools = {t.name: t for t in TOOLS}

        # Build graph
        builder = StateGraph(AgentState)

        # Add nodes
        builder.add_node("call_tools_llm", self.call_tools_llm)
        builder.add_node("invoke_tools", self.invoke_tools)
        builder.add_node("email_sender", self.email_sender)

        # Entry point
        builder.set_entry_point("call_tools_llm")

        # Conditional routing
        builder.add_conditional_edges(
            "call_tools_llm",
            Agent.exists_action,
            {"more_tools": "invoke_tools", "email_sender": "email_sender"},
        )

        # Tool cycle back
        builder.add_edge("invoke_tools", "call_tools_llm")
        builder.add_edge("email_sender", END)

        # Compile with memory
        memory = MemorySaver()
        self.app = builder.compile(
            checkpointer=memory,
            interrupt_before=["email_sender"]
        )

    # -------------------------
    # Condition: Does LLM want tools?
    # -------------------------
    @staticmethod
    def exists_action(state: AgentState):
        result = state["messages"][-1]
        if hasattr(result, "tool_calls") and result.tool_calls:
            return "more_tools"
        return "email_sender"

    # -------------------------
    def call_tools_llm(self, state: AgentState):
        messages = [SystemMessage(content=TOOLS_SYSTEM_PROMPT)] + state["messages"]
        response = self.llm.invoke(messages)
        return {"messages": [response]}

    # -------------------------
    def invoke_tools(self, state: AgentState):
        tool_calls = getattr(state["messages"][-1], "tool_calls", []) or []
        results = []

        for t in tool_calls:
            tool_name = t.get("name")
            print(f"🔧 Calling tool: {tool_name}")

            if tool_name in self.tools:
                try:
                    result = self.tools[tool_name].invoke(t.get("args", {}))
                except Exception as e:
                    result = f"Error invoking {tool_name}: {e}"
            else:
                result = f"Unknown tool: {tool_name}"

            results.append(
                ToolMessage(
                    tool_call_id=t.get("id", "unknown"),
                    name=tool_name,
                    content=str(result),
                )
            )

        return {"messages": results}

    # -------------------------
    def email_sender(self, state: AgentState):
        email_llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.1)
        email_input = [
            SystemMessage(content=EMAILS_SYSTEM_PROMPT),
            HumanMessage(content=state["messages"][-1].content),
        ]
        email_response = email_llm.invoke(email_input)

        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key["api-key"] = os.environ.get("BREVO_API_KEY")
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )

        send_smtp_email = SendSmtpEmail(
            to=[{"email": os.environ["TO_EMAIL"]}],
            sender={"email": os.environ["FROM_EMAIL"]},
            subject=os.environ["EMAIL_SUBJECT"],
            html_content=email_response.content,
        )

        try:
            response = api_instance.send_transac_email(send_smtp_email)
            print("✅ Email sent successfully:", response)
        except Exception as e:
            print("❌ Email sending failed:", str(e))

    # -------------------------
    # Run wrapper (exposed for app.py)
    # -------------------------
    def run(self, query: str, thread_id: str):
        config = {"configurable": {"thread_id": thread_id}}
        result = self.app.invoke({"messages": [HumanMessage(content=query)]}, config=config)
        return result


# -----------------------------
# Manual testing
# -----------------------------
if __name__ == "__main__":
    agent = Agent()

    # Quick test for attractions
    result = agent.run("Find top attractions in Paris", thread_id="test1")
    print(result)
