# -*- coding: utf-8 -*-
from bson import ObjectId
import models
from Query import AdministrativeSubdivisions
import logging
import threading
logger = logging.getLogger(__name__)
global lock
lock = threading.Lock()

def get_list_with_searchtext(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    where = args['data'].get('where', None)
    sort = args['data'].get('sort', 20)

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
    ret=AdministrativeSubdivisions.get_hamlet()

    if where.has_key('ward_code') and where['ward_code'] != None:\
        #and where['ward_code'].strip() != "":
        ret.match("ward_code == @war_code", war_code = where['ward_code'])

    if(searchText != None):
        ret.match("contains(hamlet_name, @name) or " + \
            "contains(hamlet_code, @name) or " + \
            "contains(org_hamlet_code, @name) or " + \
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
            ret  =  models.HCSLS_Hamlet().insert(data)
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
            ret  =  models.HCSLS_Hamlet().update(
                data, 
                "hamlet_code == {0}", 
                args['data']['hamlet_code'])
            if ret['data'].raw_result['updatedExisting'] == True:
                ret.update(
                    item = AdministrativeSubdivisions.get_hamlet().match("hamlet_code == {0}", args['data']['hamlet_code']).get_item()
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
            ret  =  models.HCSLS_Hamlet().delete("hamlet_code in {0}",[x["hamlet_code"]for x in args['data']])
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
        hamlet_code            = (lambda x: x['hamlet_code']            if x.has_key('hamlet_code')       else None)(args['data']),
        ward_code              = (lambda x: x['ward_code']              if x.has_key('ward_code')         else None)(args['data']),
        hamlet_name            = (lambda x: x['hamlet_name']            if x.has_key('hamlet_name')       else None)(args['data']),
        hamlet_name2           = (lambda x: x['hamlet_name2']           if x.has_key('hamlet_name2')      else None)(args['data']),
        type_code              = (lambda x: x['type_code']              if x.has_key('type_code')         else None)(args['data']),
        ordinal                = (lambda x: x['ordinal']                if x.has_key('ordinal')           else None)(args['data']),
        note                   = (lambda x: x['note']                   if x.has_key('note')              else None)(args['data']),
        lock                   = (lambda x: x['lock']                   if x.has_key('lock')              else None)(args['data']),
        org_hamlet_code        = (lambda x: x['org_hamlet_code']        if x.has_key('org_hamlet_code')   else None)(args['data'])
    )

    return ret_dict

def set_dict_update_data(args):
    ret_dict = set_dict_insert_data(args)
    del ret_dict['hamlet_code']
    return ret_dict