# -*- coding: utf-8 -*-
from bson import ObjectId
import models
from Query import FactorAppraisal
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

    ret=FactorAppraisal.display_list_factor_appraisal(args['data']['factor_group_code'])
    
    if(searchText != None):
        ret.match("contains(factor_code, @name) or contains(factor_name, @name)" + \
            " or contains(weight, @name) or contains(ordinal, @name)",name=searchText.strip())

    if(sort != None):
        ret.sort(sort)
        
    return ret.get_page(pageIndex, pageSize)

def insert(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_insert_data(args)
            ret  =  models.TMLS_FactorAppraisal().insert(data)
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
            ret  =  models.TMLS_FactorAppraisal().update(
                data, 
                "factor_code == {0}", 
                args['data']['factor_code'])
            if ret['data'].raw_result['updatedExisting'] == True:
                ret.update(
                    item = FactorAppraisal.display_list_factor_appraisal(args['data']['factor_group_code']).match("factor_code == {0}", args['data']['factor_code']).get_item()
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
            ret  =  models.TMLS_FactorAppraisal().delete("factor_code in {0}",[x["factor_code"]for x in args['data']])
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
        factor_code         = (lambda x: x['factor_code']        if x.has_key('factor_code')       else None)(args['data']),
        factor_name         = (lambda x: x['factor_name']        if x.has_key('factor_name')       else None)(args['data']),
        factor_name2        = (lambda x: x['factor_name2']       if x.has_key('factor_name2')      else None)(args['data']),
        factor_group_code   = (lambda x: x['factor_group_code']  if x.has_key('factor_group_code') else None)(args['data']),
        weight              = (lambda x: x['weight']             if x.has_key('weight')            else None)(args['data']),
        is_apply_all        = (lambda x: x['is_apply_all']       if x.has_key('is_apply_all')      else None)(args['data']),
        job_working         = (lambda x: x['job_working']        if x.has_key('job_working')       else None)(args['data']),
        note                = (lambda x: x['note']               if x.has_key('note')              else None)(args['data']),
        ordinal             = (lambda x: x['ordinal']            if x.has_key('ordinal')           else None)(args['data']),
        lock                = (lambda x: x['lock']               if x.has_key('lock')              else None)(args['data'])
    )

    return ret_dict

def set_dict_update_data(args):
    ret_dict = set_dict_insert_data(args)
    del ret_dict['factor_code']
    return ret_dict