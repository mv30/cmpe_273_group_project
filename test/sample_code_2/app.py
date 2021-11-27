

import pymongo
import json

from pymongo import collection

client = pymongo.MongoClient("mongodb+srv://root:root@group-project-team-9.pxttw.mongodb.net/sample_geospatial?retryWrites=true&w=majority")
db = client['sample_geospatial']
collection = db['shipwrecks']
res = collection.find_one({  })
del res['_id']
print(json.dumps(res))