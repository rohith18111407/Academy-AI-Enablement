from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

from llm.bedrock_llm import get_bedrock_llm
from tools.web_search_tool import get_web_search_tool
from tools.hr_policy_rag_tool import get_hr_policy_rag_tool
from prompts.system_prompt import SYSTEM_PROMPT
from tools.mcp_google_docs_tool import get_mcp_google_docs_tool


def create_presidio_research_agent():

    llm = get_bedrock_llm()

    tools = [
        get_hr_policy_rag_tool(),
        get_mcp_google_docs_tool(),
        get_web_search_tool()
    ]

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    agent = create_tool_calling_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )

    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True
    )
