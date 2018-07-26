# -*- coding: utf-8 -*-
import models
import quicky

_language_code = ""

def get_list(args):
    try:
        global _language_code
        items = models.TMSYS_ConfigChangeObjectPriority().aggregate().project(
            value_list_key = 1,
            change_object = 1,
            change_object_name = 1,
            table_name = 1,
            language = 1,
            priority_no = 1
            )

        if _language_code == "":
            _language_code = quicky.applications.get_settings().LANGUAGE_CODE

        list_name = args["data"].get("name", "")

        if type(list_name) is list:
            ret = []
            for x in list_name:
                items.match("(language == @lan) and (value_list_key == @name)", lan=_language_code, name=x)
                items.sort({"priority_no":1})
                ret.append(items.get_item())
            return {"values":ret}
        elif type(list_name) in [str, unicode]:
            if args["data"].has_key('name'):
                items.match("(language == @lan) and (value_list_key == @name)", lan=_language_code, name=list_name)
                items.sort({"priority_no":1})
                return items.get_list()
        
        return None
    except Exception as ex:
        return None