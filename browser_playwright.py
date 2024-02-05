from langchain_community.agent_toolkits import PlayWrightBrowserToolkit

import nest_asyncio

nest_asyncio.apply()

from langchain_community.tools.playwright.utils import (
    create_async_playwright_browser,  # A synchronous browser is available, though it isn't compatible with jupyter.\n",      },
)


async_browser = create_async_playwright_browser()
toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=async_browser)
tools = toolkit.get_tools()
print(tools)

tools_by_name = {tool.name: tool for tool in tools}
navigate_tool = tools_by_name["navigate_browser"]
get_elements_tool = tools_by_name["get_elements"]


await navigate_tool.arun(
    {"url": "https://web.archive.org/web/20230428131116/https://www.cnn.com/world"}
)


# The browser is shared across tools, so the agent can interact in a stateful manner
await get_elements_tool.arun(
    {"selector": ".container__headline", "attributes": ["innerText"]}
)


# If the agent wants to remember the current webpage, it can use the `current_webpage` tool
await tools_by_name["current_webpage"].arun({})