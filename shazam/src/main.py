import asyncio

from shazam import Recognizer


async def main():
    recognizer = Recognizer("songs.json")
    await recognizer.run()
    print("\nDone!")


if __name__ == '__main__':
    asyncio.run(main())
