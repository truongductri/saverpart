from pymongo import MongoClient
from . import dict_utils
import threading
import logging
logger = logging.getLogger(__name__)
global lock
lock = threading.Lock()
_view_cache={}
_coll_of_views = None
_coll_of_roles = None
_coll_of_user_role= None
_privileges_cache={}
import datetime
_db=None
def set_config(*args,**kwargs):

    """
    Set database config for authorization
    Example: set_config(
                        host=...,
                        port=...,
                        name=..database name,
                        user=....
                        password=...)
    :param args:
    :param kwargs:
    :return:
    """
    try:
        global _db
        global _coll_of_views
        global _coll_of_roles
        if type(args) is tuple and args.__len__() > 0:
            args = args[0]
        else:
            args = kwargs
        if not dict_utils.has_key(args,"host"):
            raise Exception("'host' was not found")
        if not dict_utils.has_key(args,"port"):
            raise Exception("'port' was not found")
        if not dict_utils.has_key(args,"name"):
            raise Exception("'name' was not found")
        if not dict_utils.has_key(args,"schema"):
            raise Exception("'schema' was not found")
        if _db == None:
            cnn = MongoClient(host=args["host"], port=args["port"])
            _db = cnn.get_database(args["name"])
            if dict_utils.has_key(args,"user") and (args["user"] != "" or args["user"] != None):
                _db.authenticate(args["user"], args["password"])
        _coll_of_views = _db.get_collection( "{0}.views".format(args["schema"]))
        _coll_of_roles = _db.get_collection("{0}.roles".format(args["schema"]))
    except Exception as ex:
        logger.debug(ex)
        raise ex


def register_view(*args,**kwargs):
    # type: (dict) -> dict
    """
    Regist a new view example register_view(
                        view=...view name,
                        app= ... appname)
    :param args:
    :param kwargs:
    :return:
    """
    try:
        if type(args) is tuple and args.__len__() > 0:
            args = args[0]
        else:
            args = kwargs
        if not dict_utils.has_key(args,"app"):
            raise Exception("'app' was not found")
        if not dict_utils.has_key(args,"view"):
            raise Exception("'view' was not found")
        key = "{0}/{1}".format(args["app"], args["view"]).lower()
        if not dict_utils.has_key(_view_cache,key):
            lock.acquire()
            try:
                item = _coll_of_views.find_one({
                    "View": args["view"],
                    "App": args["app"]
                })
                ret_id = None
                if item == None:
                    ret = _coll_of_views.insert_one({
                        "View": args["view"],
                        "App": args["app"],
                        "CreatedOn": datetime.datetime.now(),
                        "CreatedOnUTC": datetime.datetime.utcnow()
                    })
                    _view_cache.update({
                        key: ret.inserted_id.__str__()
                    })
                else:
                    _view_cache.update({
                        key: item["_id"].__str__()
                    })
                lock.release()
                return _view_cache[key]
            except Exception as ex:
                lock.release()
                logger.debug(ex)
                raise (ex)
    except Exception as ex:
        logger.debug(ex)
        raise ex

def get_privileges_of_user(*args,**kwargs):
    global _privileges_cache
    import re
    from django.contrib.auth.models import User
    import django.core.exceptions
    if args.__len__() == 0:
        args =kwargs
    if not dict_utils.has_key(args,"username"):
        raise ("'username' was not found")
    if not dict_utils.has_key(args,"app"):
        raise ("'app' was not found")
    if not dict_utils.has_key(args,"view"):
        raise ("'view' was not found")
    if not dict_utils.has_key(args,"schema"):
        raise ("'schema' was not found")
    key="username={0};app={1};view={2};schema={3}".format(
        args["username"],
        args["app"],
        args["view"],
        args["schema"],
    ).lower()
    if dict_utils.has_key(_privileges_cache,key):
        return _privileges_cache[key]
    else:

        try:
            try:
                user=User.objects.get(username=args["username"], schema=args["schema"])
            except django.core.exceptions.ObjectDoesNotExist as ex:

                return None
            if user.is_superuser:
                return dict(
                    isFull=True
                )
            else:
                lock.acquire()
                try:
                    roles =list(_coll_of_roles\
                        .aggregate([
                        {
                            "$match":{
                                "schema": re.compile(r"^" + args["schema"] + "$", re.IGNORECASE)
                            }
                        },{
                            "$match": {
                                "app": re.compile(r"^" + args["app"] + "$", re.IGNORECASE)
                            }
                        },{
                            "$unwind": "$views"
                        },{
                            "$match": {
                                "views.name": re.compile(r"^" + args["view"] + "$", re.IGNORECASE)
                            }
                        },{
                            "$unwind":"$views.users"
                        },{
                            "$match": {
                                "views.users.username":re.compile(r"^"+args["username"]+"$",re.IGNORECASE)
                            }
                        }
                    ]))
                    if roles.__len__() == 0:
                        lock.release()
                        return None
                    else:
                        if roles[0].get("privileges",None) == None:
                            lock.release()
                            return None
                        else:
                            _privileges_cache[key]=roles[0]["privileges"]
                            lock.release()
                            return _privileges_cache[key]
                except Exception as ex:
                    lock.release()
                    raise (ex)
        except Exception as ex:
            raise (ex)

def create_role(*args,**kwargs):
    import re
    if args.__len__() == 0:
        args =kwargs
    if not dict_utils.has_key(args,"role"):
        raise ("'role' was not found")
    if not dict_utils.has_key(args,"app"):
        raise ("'app' was not found")
    if not dict_utils.has_key(args,"schema"):
        raise ("'schema' was not found")
    role=_coll_of_roles.find_one({
        "schema": re.compile(r"^" + args["schema"] + "$", re.IGNORECASE),
        "role": re.compile(r"^" + args["role"] + "$", re.IGNORECASE),
        "app": re.compile(r"^" + args["app"] + "$", re.IGNORECASE),
    })
    if role == None:
        _coll_of_roles.insert_one({
            "schema":args["schema"],
            "role":args["role"],
            "app":args["app"],
            "createdOn":datetime.datetime.now(),
            "createdBy":"application"
        })

def add_view_to_role(*args,**kwargs):
    import re
    if args.__len__() == 0:
        args = kwargs
    if not dict_utils.has_key(args, "role"):
        raise ("'role' was not found")
    if not dict_utils.has_key(args, "app"):
        raise ("'app' was not found")
    if not dict_utils.has_key(args, "schema"):
        raise ("'schema' was not found")
    if not dict_utils.has_key(args, "view"):
        raise ("'view' was not found")
    role = _coll_of_roles.find_one({
        "schema": re.compile(r"^" + args["schema"] + "$", re.IGNORECASE),
        "role": re.compile(r"^" + args["role"] + "$", re.IGNORECASE),
        "app": re.compile(r"^" + args["app"] + "$", re.IGNORECASE),
    })
    if role == None:
        raise ("'{0}' was not found".format(args["role"]))
    else:

        _coll_of_roles.update_one({
            "schema": re.compile(r"^" + args["schema"] + "$", re.IGNORECASE),
            "role": re.compile(r"^" + args["role"] + "$", re.IGNORECASE),
            "app": re.compile(r"^" + args["app"] + "$", re.IGNORECASE)
        },{
            "$push":{
                "views":{
                    "name":args["view"].lower(),
                    "createdOn":datetime.datetime.now(),
                    "createdBy":"application",
                    "users":[]
                }
            }
        })
def add_user_to_view(*args,**kwargs):
    import re
    if args.__len__() == 0:
        args = kwargs
    if not dict_utils.has_key(args, "role"):
        raise ("'role' was not found")
    if not dict_utils.has_key(args, "app"):
        raise ("'app' was not found")
    if not dict_utils.has_key(args, "schema"):
        raise ("'schema' was not found")
    if not dict_utils.has_key(args, "view"):
        raise ("'view' was not found")
    if not dict_utils.has_key(args, "username"):
        raise ("'username' was not found")
    if not dict_utils.has_key(args, "privileges"):
        raise ("'privileges' was not found")
    if not dict_utils.has_key(args["privileges"], "isFull"):
        raise ("'privileges.isFull' was not found")
    if not dict_utils.has_key(args["privileges"], "allowInsert"):
        raise ("'privileges.allowInsert' was not found")
    if not dict_utils.has_key(args["privileges"], "allowUpdate"):
        raise ("'privileges.allowUpdate' was not found")
    if not dict_utils.has_key(args["privileges"], "allowDelete"):
        raise ("'privileges.allowDelete' was not found")
    role = _coll_of_roles.find_one({
        "schema": re.compile(r"^" + args["schema"] + "$", re.IGNORECASE),
        "role": re.compile(r"^" + args["role"] + "$", re.IGNORECASE),
        "app": re.compile(r"^" + args["app"] + "$", re.IGNORECASE),
        "views.name": re.compile(r"^" + args["view"] + "$", re.IGNORECASE)
    })
    if role == None:
        raise ("'{0}' not found in '{1}'".format(args["view"],args["role"]))
    else:
        role_user = _coll_of_roles.find_one({
            "schema": re.compile(r"^" + args["schema"] + "$", re.IGNORECASE),
            "role": re.compile(r"^" + args["role"] + "$", re.IGNORECASE),
            "app": re.compile(r"^" + args["app"] + "$", re.IGNORECASE),
            "views.name": re.compile(r"^" + args["view"] + "$", re.IGNORECASE),
            "views.users.username": re.compile(r"^" + args["view"] + "$", re.IGNORECASE),
        })
        if role_user == None:
            ret_indexs =list( _coll_of_roles.aggregate([
                {
                    "$match": {
                        "schema": re.compile(r"^" + args["schema"] + "$", re.IGNORECASE),
                        "role": re.compile(r"^" + args["role"] + "$", re.IGNORECASE),
                        "app": re.compile(r"^" + args["app"] + "$", re.IGNORECASE),
                        "views.name": re.compile(r"^" + args["view"] + "$", re.IGNORECASE)
                    }
                }, {
                    "$project": {
                        "index": { "$indexOfArray": [ "$views.name", args["view"].lower() ] }
                    }
                }
            ]))
            if ret_indexs[0]["index"] == -1:
                raise (Exception("'{0}' was not found in '{1}'".format(args["view"],args["role"])))

            _coll_of_roles.update_one({
                "schema": re.compile(r"^" + args["schema"] + "$", re.IGNORECASE),
                "role": re.compile(r"^" + args["role"] + "$", re.IGNORECASE),
                "app": re.compile(r"^" + args["app"] + "$", re.IGNORECASE),
                "views.name": re.compile(r"^" + args["view"] + "$", re.IGNORECASE)
            },{
                "$push":{
                    "views["+ret_indexs[0]["index"]+"].users":{
                        "username":args["username"],
                        "createdOn":datetime.datetime.now(),
                        "createdBy":"application",
                        "privileges":args["privileges"]
                    }
                }
            })




