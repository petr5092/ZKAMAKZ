from university.dao import UniversityDAO
from spec.dao import SpecDAO
import asyncio


async def main():
    print(1)
    print(await UniversityDAO.get_all())
    print(await SpecDAO.get_all())

if __name__ == '__main__':
    asyncio.run(main())