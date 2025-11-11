import json
import asyncio
from university.dao import UniversityDAO
from spec.dao import SpecDAO


def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


async def load_university_to_db(json_data):
    for university in json_data['university']:
        await UniversityDAO.add(**university)


async def load_spec_to_db(json_data):
    for spec in json_data['spec']:
        university = await UniversityDAO.find_by_fil(name=spec.pop('university'))
        await SpecDAO.add(**spec, university_id=university.id)


async def main():
    university_data = load_json('university.json')
    spec_data = load_json('spec.json')
    await load_university_to_db(university_data)
    await load_spec_to_db(spec_data)
    
if __name__ == '__main__':
    asyncio.run(main())