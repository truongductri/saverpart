"""
This package is the core package support for multi purpose in project
"""
from . import dict_utils
from . dic_has_key import dic_has_key
from . import view
from . import applications
from . import authorize
from . import language
import sys
from . import caller
from . import sql_db
import os
from . import layout_view #use for boostrap layout definition
from . import url
import datetime
import threading
system_settings=None
_db_multi_tenancy=None
_cache_multi_tenancy={}
global lock
lock=threading.Lock()
def get_tenancy_code_regex():
    """
    get Regex for tenancyCode tenancy code must be star with alphabet and including number, "-","_":
    :return:
    """
    return r"[A-Za-z0-9](?:[A-Za-z0-9\-\_]{0,61}[A-Za-z0-9])"
    # return "\(w{0,24})"
def validate_tenancy_code(code):
    """
    Validate tenancy code 
    :param code:
    :return:
    """
    import re
    return re.compile(get_tenancy_code_regex()).match(code)


def get_static_server_path(file,path):
    # type: (str,str) -> str
    """
    create full phisical static path from relative path
    :param file:
    :param path:
    :return:
    """
    return os.getcwd() + os.sep + os.path.dirname(file) + os.sep +path
def get_django_settings_module():
    """
    Get django setting module in project

    :return:
    """
    global system_settings
    if system_settings!=None:
        return system_settings
    "get all settings of current project"
    setting_name=os.environ.get("DJANGO_SETTINGS_MODULE",None)
    ret=None
    if setting_name==None:
        return None
    else:
        if not dic_has_key(sys.modules,setting_name):
            return None
        else:
            system_settings=sys.modules[setting_name]
            if hasattr(system_settings,"USE_MULTI_TENANCY") and system_settings.USE_MULTI_TENANCY:
                if not hasattr(system_settings,"MULTI_TENANCY_DEFAULT_SCHEMA"):
                    raise (Exception("It look like you have used 'USE_MULTI_TENANCY'.\n"
                                     "But you forgot set 'MULTI_TENANCY_DEFAULT_SCHEMA' in '{0}'.\n"
                                     "What is default schema?\n"
                                     "Serving multiple tenants under same database,\n"
                                     "where each tenant has its own sets of tables grouped with schema as required by tenant.\n"
                                     "default schema will be used, if the system can not determine schema of user transaction".format(
                        system_settings.__file__
                    )))
                if not hasattr(system_settings,"MULTI_TENANCY_CONFIGURATION"):
                    raise (Exception("It look like you have used 'USE_MULTI_TENANCY'.\n"
                                     "But you forgot set 'MULTI_TENANCY_CONFIGURATION' in '{0}'.\n"
                                     "What is 'MULTI_TENANCY_CONFIGURATION'?\n"
                                     "'MULTI_TENANCY_CONFIGURATION' is include bellow information:\n"
                                     "host=[host data base name]\n"
                                     "port=[mongodb port]\n"
                                     "user=[user name]\n"
                                     "password=[password]\n"
                                     "name=[database name]\n"
                                     "collection=[manage muti tenant collection name]".format(
                        system_settings.__file__
                    )))
    return system_settings
def to_server_local_time(val):
    # type: (datetime) -> datetime
    """
    convert datetime val into datetime with server local time zone
    :param val:
    :return:
    """
    return val+(datetime.datetime.utcnow() - datetime.datetime.now())
def to_client_time(val):
    # type: (datetime) -> datetime
    """
    convert datetime value into datetime with client time zone
    Caution: this method need to be call in thread with http request
    :param val:
    :return:
    """
    return val - datetime.timedelta(minutes=threading.current_thread().client_offset_minutes)
def get_client_offset_minutes():
    # type: () -> int
    """
    get client offset minutes from UTC
    :return:
    """
    return threading.current_thread().client_offset_minutes
def get_tenancy_collection():
    # type: () -> pymongo.MongoClient.Collection
    """
    Get tenancy collection refer 'MULTI_TENANCY_CONFIGURATION' in settings.py
    :return:
    """
    global _db_multi_tenancy
    if _db_multi_tenancy==None:
        import pymongo

        config=get_django_settings_module().MULTI_TENANCY_CONFIGURATION
        cnn=pymongo.MongoClient(
            host=config["host"],
            port=config["port"]
        )
        db=cnn.get_database(config["name"])
        if config.get("user","")!="":
            db.authenticate(config["user"],config["password"])
        _db_multi_tenancy=db.get_collection(config["collection"])
    return _db_multi_tenancy
def get_tenancy_schema(code):
    # type: (str) -> str
    """
    get schema from tenancy code
    :param code:
    :return:
    """
    from . import get_django_settings_module
    import re
    # cmp=re.compile(r"[a-zA-Z_0-9-]+\z",re.IGNORECASE)
    if get_django_settings_module().MULTI_TENANCY_DEFAULT_SCHEMA==code:
        return code

    global _cache_multi_tenancy

    if not dict_utils.has_key(_cache_multi_tenancy,code):
        lock.acquire()
        try:
            item=get_tenancy_collection().find_one(
                {
                    "code":{
                        "$regex":re.compile("^"+code+"$",)
                    }
                }
            )
            if item==None:
                lock.release()
                return None
            lock.release()
            _cache_multi_tenancy.update({
                code: item["schema"]
            })
            return _cache_multi_tenancy[code]
        except Exception as ex:
            lock.release()
            raise (ex)
    return _cache_multi_tenancy[code]
def register_tenancy_schema(code,schema=None):

    """
    Register new tenancy
    :param code:
    :param schema:
    :return:
    """
    if schema==None:
        schema=code
    import re
    item=get_tenancy_collection().find_one(
        {
            "code":{"$regex": re.compile("^"+code+"$",re.IGNORECASE)}
        }
    )
    if item==None:
        get_tenancy_collection().insert_one({
            "code":code,
            "schema":schema

        })
    _cache_multi_tenancy.update({
        code: schema
    })