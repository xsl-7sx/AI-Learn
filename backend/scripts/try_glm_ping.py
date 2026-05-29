import asyncio

from langchain_core.messages import HumanMessage
from app.chains.llm import get_llm


async def main() -> None:
    llm = get_llm()
    result = await llm.ainvoke([HumanMessage(content="用一句话介绍光合作用")])
    print(result.content)


if __name__ == "__main__":
    asyncio.run(main())
