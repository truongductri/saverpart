# -*- coding: utf-8 -*-
from config import database, helpers, db_context
_hasCreated=False
def LMSLS_MaterialFolder():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "LMSLS_MaterialFolder",
            "base",
            [["folder_id"]],
            #id=helpers.create_field("numeric",True),
            folder_id=helpers.create_field("text", True),
            folder_name=helpers.create_field("text", True),
            folder_name2=helpers.create_field("text"),
            parent_id=helpers.create_field("text"),
            parent_code=helpers.create_field("text"),
            level=helpers.create_field("numeric"),
            level_code=helpers.create_field("list"),
            ordinal=helpers.create_field("numeric"),
            lock=helpers.create_field("bool"),
            note=helpers.create_field("text"),
            moderator_id=helpers.create_field("text"),
            approver_id=helpers.create_field("text"),
            active=helpers.create_field("bool"),
            approve_type=helpers.create_field("bool"),
            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text")
        )
        _hasCreated=True
    ret = db_context.collection("LMSLS_MaterialFolder")

    return ret