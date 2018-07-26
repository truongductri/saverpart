from .. import models


def check_exits_factCode_within_factGroup(fact_grCode):
    list_factCode = models.TMLS_FactorAppraisal().aggregate().match("factor_group_code == {0}", fact_grCode).get_list()
    if list_factCode != None and len(list_factCode) > 0:
        return True
    return False
   
def get_factor_appraisal_group():
    ret=models.TMLS_FactorAppraisalGroup().aggregate()
    ret.project(
        factor_group_code = 1,
        factor_group_name = 1,
        factor_group_name2 = 1,
        parent_code = 1,
        level = 1,
        level_code = 1,
        ordinal = 1,
        note = 1,
        lock = 1
        )
    ret.sort(dict(
        factor_group_code = 1,
        ordinal = 1
    )) 
    return ret



