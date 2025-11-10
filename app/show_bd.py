from university.dao import UniversityDAO
import asyncio


async def main():
    print(1)
    print(await UniversityDAO.get_all())

if __name__ == '__main__':
    asyncio.run(main())