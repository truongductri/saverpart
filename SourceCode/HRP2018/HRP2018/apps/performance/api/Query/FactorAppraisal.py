from .. import models
from .. import common
def display_list_factor_appraisal(group_code):
    list_group_code = models.TMLS_FactorAppraisalGroup().aggregate().match("level_code == {0}", group_code).project(level_code = 1).get_list()
    list_filter = []
    if list_group_code != None and len(list_group_code) > 0:
        for el in list_group_code:
            if el['level_code'] != None and len(el['level_code']):
                list_filter += el['level_code'][el['level_code'].index(group_code) : len(el['level_code'])]
    ret=models.TMLS_FactorAppraisal().aggregate()
    ret.left_join(models.auth_user_info(), "created_by", "username", "uc")
    ret.left_join(models.auth_user_info(), "modified_by", "username", "um")
    if list_filter != None and len(list_filter) > 0:
        ret.match('factor_group_code in {0}', list_filter)
    ret.project(
        factor_code="factor_code",
        factor_name="factor_name",
        factor_name2="factor_name2",
        factor_group_code="factor_group_code",
        weight="weight",
        is_apply_all="is_apply_all",
        note="note",
        ordinal="ordinal",
        lock="lock",
        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')",
        )
    ret.sort(dict(
        ordinal = 1
        ))

    return ret

def update_job_working(args):
    try:
        collection  =  common.get_collection('HCSLS_Acadame')
        ret = collection.update(
            {
                "factor_code": args['data']['factor_code'],
            },
            {
                "$set": {
                    'job_working': args['data']['job_working']
                    }
            })
    except Exception as ex:
        raise ex
