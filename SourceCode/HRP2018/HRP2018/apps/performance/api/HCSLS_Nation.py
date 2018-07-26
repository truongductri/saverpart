# -*- coding: utf-8 -*-
from bson import ObjectId
import models
from Query import Nation
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
    ret=Nation.display_list_nation()
    
    if(searchText != None):
        ret.match("contains(nation_code, @name) or " + \
            "contains(nation_name, @name) or " + \
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
            ret  =  models.HCSLS_Nation().insert(data)
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
            ret  =  models.HCSLS_Nation().update(
                data, 
                "nation_code == {0}", 
                args['data']['nation_code'])
            if ret['data'].raw_result['updatedExisting'] == True:
                ret.update(
                    item = Nation.display_list_nation().match("nation_code == {0}", args['data']['nation_code']).get_item()
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
            ret  =  models.HCSLS_Nation().delete("nation_code in {0}",[x["nation_code"]for x in args['data']])
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
        nation_code          = (lambda x: x['nation_code']        if x.has_key('nation_code')          else None)(args['data']),
        nation_name          = (lambda x: x['nation_name']        if x.has_key('nation_name')          else None)(args['data']),
        ordinal              = (lambda x: x['ordinal']            if x.has_key('ordinal')              else None)(args['data']),
        note                 = (lambda x: x['note']               if x.has_key('note')                 else None)(args['data']),
        lock                 = (lambda x: x['lock']               if x.has_key('lock')                 else None)(args['data']),
        #eat_amount           = (lambda x: x['eat_amount']         if x.has_key('eat_amount')           else None)(args['data']),
        continents           = (lambda x: x['continents']         if x.has_key('continents')           else None)(args['data']),
        #home_amount          = (lambda x: x['home_amount']        if x.has_key('home_amount')          else None)(args['data']),
        #taxi_amount          = (lambda x: x['taxi_amount']        if x.has_key('taxi_amount')          else None)(args['data']),
        #sub_days_amount      = (lambda x: x['sub_days_amount']    if x.has_key('sub_days_amount')      else None)(args['data']),
        nation_name2         = (lambda x: x['nation_name2']       if x.has_key('nation_name2')         else None)(args['data']),
        #department_code      = (lambda x: x['department_code']    if x.has_key('department_code')      else None)(args['data']),
        org_nation_code      = (lambda x: x['org_nation_code']    if x.has_key('org_nation_code')      else None)(args['data'])
    )

    return ret_dict

def set_dict_update_data(args):
    ret_dict = set_dict_insert_data(args)
    del ret_dict['nation_code']
    return ret_dict