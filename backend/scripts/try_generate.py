import asyncio

from app.chains.quiz_generation import generate_quiz


async def main() -> None:
    result = await generate_quiz("光合作用")
    types = {question.type for question in result.questions}
    print("quiz_id:", result.quiz_id)
    print("questions:", len(result.questions))
    print("types:", types)


if __name__ == "__main__":
    asyncio.run(main())
