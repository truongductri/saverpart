# -*- coding: utf-8 -*-
from bson import ObjectId
import models
from Query import Discipline
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
    ret=Discipline.display_list_discipline()
    
    if(searchText != None):
        ret.match("contains(disc_name, @name)",name=searchText)

    if(sort != None):
        ret.sort(sort)
        
    return ret.get_page(pageIndex, pageSize)

def insert(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_insert_data(args)
            ret  =  models.HCSLS_Discipline().insert(data)
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
            ret  =  models.HCSLS_Discipline().update(
                data, 
                "_id == {0}", 
                ObjectId(args['data']['_id']))
            if ret['data'].raw_result['updatedExisting'] == True:
                ret.update(
                    item = Discipline.display_list_discipline().match("_id == {0}", ObjectId(args['data']['_id'])).get_item()
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
            ret  =  models.HCSLS_Discipline().delete("_id in {0}",[ObjectId(x["_id"])for x in args['data']])
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
        disc_code           = (lambda x : x['disc_code']         if x.has_key('disc_code')     else None )(args['data']),
        disc_name           = (lambda x : x['disc_name']         if x.has_key('disc_name')     else None )(args['data']),
        disc_name2          = (lambda x : x['disc_name2']        if x.has_key('disc_name2')    else None )(args['data']),
        is_due_salary       = (lambda x : x['is_due_salary']     if x.has_key('is_due_salary') else None )(args['data']),
        ordinal             = (lambda x : x['ordinal']           if x.has_key('ordinal')       else None )(args['data']),
        note                = (lambda x : x['note']              if x.has_key('note')          else None )(args['data']),
        lock                = (lambda x : x['lock']              if x.has_key('lock')          else None )(args['data'])
    )

    return ret_dict

def set_dict_update_data(args):
    ret_dict = set_dict_insert_data(args)
    del ret_dict['disc_code']
    return ret_dict