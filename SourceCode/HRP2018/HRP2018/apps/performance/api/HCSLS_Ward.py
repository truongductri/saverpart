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
    ret=AdministrativeSubdivisions.get_ward()

    if where.has_key('district_code') and where['district_code'] != None:\
       #and where['district_code'].strip() != "":
        ret.match("district_code == @dis_code", dis_code = where['district_code'])

    if(searchText != None):
        ret.match("contains(ward_name, @name)",name=searchText)

    if(sort != None):
        ret.sort(sort)
        
    return ret.get_page(pageIndex, pageSize)

def insert(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_insert_data(args)
            ret  =  models.HCSLS_Ward().insert(data)
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
            ret  =  models.HCSLS_Ward().update(
                data, 
                "_id == {0}", 
                ObjectId(args['data']['_id']))
            if ret['data'].raw_result['updatedExisting'] == True:
                ret.update(
                    item = AdministrativeSubdivisions.get_ward().match("_id == {0}", ObjectId(args['data']['_id'])).get_item()
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
            ret  =  models.HCSLS_Ward().delete("_id in {0}",[ObjectId(x["_id"])for x in args['data']])
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
        ward_code            = (lambda x: x['ward_code']            if x.has_key('ward_code')       else None)(args['data']),
        district_code        = (lambda x: x['district_code']        if x.has_key('district_code')   else None)(args['data']),
        ward_name            = (lambda x: x['ward_name']            if x.has_key('ward_name')       else None)(args['data']),
        ward_name2           = (lambda x: x['ward_name2']           if x.has_key('ward_name2')      else None)(args['data']),
        type_code            = (lambda x: x['type_code']            if x.has_key('type_code')       else None)(args['data']),
        ordinal              = (lambda x: x['ordinal']              if x.has_key('ordinal')         else None)(args['data']),
        note                 = (lambda x: x['note']                 if x.has_key('note')            else None)(args['data']),
        lock                 = (lambda x: x['lock']                 if x.has_key('lock')            else None)(args['data']),
        org_ward_code        = (lambda x: x['org_ward_code']        if x.has_key('org_ward_code')   else None)(args['data'])
    )

    return ret_dict

def set_dict_update_data(args):
    ret_dict = set_dict_insert_data(args)
    del ret_dict['ward_code']
    return ret_dict