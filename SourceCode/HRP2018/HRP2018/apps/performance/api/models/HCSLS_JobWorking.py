# -*- coding: utf-8 -*-
from config import database, helpers, db_context
import datetime
import base
import threading
_hasCreated=False
def HCSLS_JobWorking():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "HCSLS_JobWorking",
            "base",
            [["job_w_code"]],
            job_w_code = helpers.create_field("text", True),
            job_w_name = helpers.create_field("text", True),
            job_w_name2 = helpers.create_field("text"),
            job_w_duty = helpers.create_field("text"),
            gjw_code = helpers.create_field("text", True),
            ordinal = helpers.create_field("numeric"),
            lock = helpers.create_field("bool"),
            is_job_w_main_staff = helpers.create_field("bool"),
            report_to_job_w=helpers.create_field("text"),
            internal_process = helpers.create_field("text"),
            combine_process = helpers.create_field("text"),
            description = helpers.create_field("text"),
            effect_date = helpers.create_field("date"),
            job_pos_code = helpers.create_field("text"),
            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text")
        )
        _hasCreated=True

    ret = db_context.collection("HCSLS_JobWorking")

    return ret