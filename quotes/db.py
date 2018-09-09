import aiohttp
import json
import motor.motor_asyncio
import pymongo

from quotes.config import MONGO_URI


async def mongo_connection(app):
    mongo = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
    async def _cleanup(app):
        mongo.close()
    app.on_cleanup.append(_cleanup)
    app['db'] = mongo['test']


async def load_db(app, path):
    await app['db'].quotes.drop()
    with open(path) as f:
        data = json.load(f)
    await app['db'].quotes.insert_many(data)
    await app['db'].quotes.create_index([('author', pymongo.TEXT)])


async def setup_db(app):
    await mongo_connection(app)
    await load_db(app, 'data.json')


async def get_random_element(collection, pipeline=[]):
    random_element = {'$sample': {'size': 1}}
    pipeline.append(random_element)
    cursor = collection.aggregate(pipeline)
    while (await cursor.fetch_next):
        return cursor.next_object()
    raise aiohttp.web.HTTPNotFound()
