import aiohttp_jinja2
import jinja2
import aioredis
import motor.motor_asyncio



def initJinja(app):
  aiohttp_jinja2.setup(app, loader = jinja2.FileSystemLoader('app/templates'))
  app.aiohttp_jinja2 = aiohttp_jinja2



async def initRedis(app):
  app.redisPool = await aioredis.create_pool(
    (app["config"]["redis"]["host"], int(app["config"]["redis"]["port"])),
    minsize = int(app["config"]["redis"]["poolMinSize"]),
    maxsize = int(app["config"]["redis"]["poolMaxSize"]),
    loop = app.loop,
    encoding = "utf-8",
    db = int(app["config"]["redis"]["db"])
  )



def initMongo(app):
  client = motor.motor_asyncio.AsyncIOMotorClient(app["config"]["mongo"]["dsn"])
  app.mongoHandler = client[app["config"]["mongo"]["db"]]