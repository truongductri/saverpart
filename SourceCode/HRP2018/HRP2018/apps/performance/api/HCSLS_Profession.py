# -*- coding: utf-8 -*-
from bson import ObjectId
import models
from Query import Profession
import logging
import threading
logger = logging.getLogger(__name__)
global lock
lock = threading.Lock()

def get_list_with_searchtext(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
    ret=Profession.display_list_profession()
    
    if(searchText != None):
        ret.match("contains(profession_name, @name) or " + \
            "contains(profession_code, @name) or " + \
            "contains(note, @name) or " + \
            "contains(ordinal, @name)",name=searchText.strip())

    if(sort != None):
        ret.sort(sort)
        
    return ret.get_page(pageIndex, pageSize)

def insert(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_insert_data(args)
            ret  =  models.HCSLS_Profession().insert(data)
            lock.release()
            return ret

        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)

def update(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_update_data(args)
            ret  =  models.HCSLS_Profession().update(
                data, 
                "profession_code == {0}", 
                args['data']['profession_code'])
            if ret['data'].raw_result['updatedExisting'] == True:
                ret.update(
                    item = Profession.display_list_profession().match("profession_code == {0}", args['data']['profession_code']).get_item()
                    )
            lock.release()
            return ret

        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)

def delete(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            ret  =  models.HCSLS_Profession().delete("profession_code in {0}",[x["profession_code"]for x in args['data']])
            lock.release()
            return ret

        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)

def set_dict_insert_data(args):
    ret_dict = dict()

    ret_dict.update(
        profession_code    = (lambda x: x['profession_code']   if x.has_key('profession_code')    else None)(args['data']),
        profession_name    = (lambda x: x['profession_name']   if x.has_key('profession_name')    else None)(args['data']),
        ordinal            = (lambda x: x['ordinal']           if x.has_key('ordinal')            else None)(args['data']),
        note               = (lambda x: x['note']              if x.has_key('note')               else None)(args['data']),
        lock               = (lambda x: x['lock']              if x.has_key('lock')               else None)(args['data']),
        profession_name2   = (lambda x: x['profession_name2']  if x.has_key('profession_name2')   else None)(args['data'])
    )

    return ret_dict

def set_dict_update_data(args):
    ret_dict = set_dict_insert_data(args)
    del ret_dict['profession_code']
    return ret_dict