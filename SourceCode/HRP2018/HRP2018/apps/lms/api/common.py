from bson import ObjectId
import models
import datetime

__collectionName = ''
__collection = {}
def get_pagination(args):
    global __collectionName 
    global __collection 

    if('collection' in args['data'].keys()):
        __collectionName = args['data']['collection']
        __collection= getattr(models, __collectionName)()
        pageIndex = args['data'].get('pageIndex', 0)
        pageSize = args['data'].get('pageSize', 20)
        where = args['data'].get('where', '')
        sort = args['data'].get('sort', {})
        return get_data(pageIndex, pageSize, where, sort)
    return {"error":"Not found collection name"}

def get_data(pageIndex, pageSize, where, sort):
    global __collection
    _Sort = (lambda x: x if x != None else {})(sort)
    item = __collection.aggregate()
    if(where != ''):
        item.match(where)
        if _Sort != {}:
            item.sort(_Sort)
    return item.get_page((lambda pIndex: pIndex if pIndex != None else 0)(pageIndex),\
                        (lambda pSize: pSize if pSize != None else 20)(pageSize))