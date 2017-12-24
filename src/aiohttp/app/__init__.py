from aiohttp import web
import asyncio
from .middleware import jinjaMiddleware, redisMiddleware, mongoMiddleware
from .ext import initJinja, initRedis, initMongo
import app.handlers as handlers
from configparser import ConfigParser
import os


loop = asyncio.get_event_loop()



def readConfig(prodConfigFile):
  config = ConfigParser()
  with open(os.path.join(os.path.dirname(__file__), 'default.config')) as defaultJsonConfig:
    config.read_file(defaultJsonConfig)
  if prodConfigFile:
    config.read_file(prodConfigFile)
  return config



def createMainApp(prodConfigFile = None):
  app = web.Application(loop = loop, middlewares = [jinjaMiddleware, redisMiddleware, mongoMiddleware])
  app["config"] = readConfig(prodConfigFile)
  app.on_startup.append(initJinja)
  app.on_startup.append(initRedis)
  app.on_startup.append(initMongo)

  app.router.add_get("/", handlers.showDefaultPage)
  app.router.add_post("/user/", handlers.createUser)
  app.router.add_get("/user/{userId}", handlers.getUser)
  app.router.add_route("PUT", "/user/{userId}", handlers.updateUser)
  app.router.add_route("DELETE", "/user/{userId}", handlers.deleteUser)
  return app