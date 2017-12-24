from aiohttp import web
from json import dumps



redisUserKey = "user:{userId}"



async def showDefaultPage(request):
  return request.template("defaultPage.tpl")



async def getUser(request):
  userId = int(request.match_info.get("userId"))
  user = await request.redis.get(redisUserKey.format(userId = userId))
  if user:
    return web.Response(text = user)
  else:
    user = await request.mongo.user.find_one({"id": 1}, {"_id": 0})
    request.redis.set(redisUserKey.format(userId = userId), dumps(user))
    return web.json_response(user)



async def createUser(request):
  json = await request.json()
  user = await request.mongo.user.find_one({"id": json["id"]})
  if not user:
    await request.mongo.user.insert_one(json)
  return web.json_response(json)



async def updateUser(request):
  json = await request.json()
  userId = int(request.match_info.get("userId"))
  user = await request.mongo.user.find_one({"id": userId}, {"_id": 0})
  if user:
    await request.mongo.user.update_one({"id": userId}, {"$set": {
      "name": json["name"],
      "age": json["age"]
    }})
    await request.redis.delete(redisUserKey.format(userId = userId))
    return web.json_response(user)
  else:
    return web.HTTPNotFound()



async def deleteUser(request):
  userId = int(request.match_info.get("userId"))
  user = await request.mongo.user.find_one({"id": userId}, {"_id": 0})
  if user:
    await request.mongo.user.delete_one({"id": userId})
    await request.redis.delete(redisUserKey.format(userId = userId))
    return web.json_response(user)
  else:
    return web.HTTPNotFound()