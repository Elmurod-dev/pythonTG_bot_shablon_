import json
from os.path import join
import aiofiles

from confs import BASE_DIR

DB_PATH = join(BASE_DIR, 'db' , 'database')


class DB:
    @property
    async def objects(self):
        file_name = self.__class__.__name__.lower() + "s.json"
        async with aiofiles.open(join(DB_PATH, file_name), 'r') as f:
            data = await f.read()
            data = json.loads(data)
        res = []
        for i in data:
            res.append(self.__class__(**i)) # noqa
        return res

    async def write(self, data: list[objects]):
        file_name = self.__class__.__name__.lower() + "s.json"
        res = []
        for i in data:
            res.append(i.__dict__)
        async with aiofiles.open(join(DB_PATH, file_name), 'w') as f:
            data_json = json.dumps(res, indent=3)
            await f.write(data_json)

class CRUD(DB):
    async def save(self):
        objects : list = await self.objects
        self.id = objects[-1].id + 1 if objects else 1
        objects.append(self)
        await self.write(objects)

    async def update(self, **fields):
        objects: list = await self.objects
        for obj in objects:
            if obj.id == self.id:
                for k, v in fields.items():
                    setattr(obj, k, v)
                await self.write(objects)
                return obj



    async def delete(self):
        objects : list= await self.objects
        for obj in objects:
            if obj.id == self.id:
                objects.remove(obj)
                await self.write(objects)
                break

    async def read(self):
        objects : list= await self.objects
        for obj in objects:
            if obj.id == self.id:
                return obj
