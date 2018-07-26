from .. import models
from .. import common
def display_list_job_working(group_code):
    list_group_code = models.HCSLS_JobWorkingGroup().aggregate().match("level_code == {0}", group_code).project(level_code = 1).get_list()
    list_filter = []
    if list_group_code != None and len(list_group_code) > 0:
        for el in list_group_code:
            if el['level_code'] != None and len(el['level_code']) > 0:
                list_filter += el['level_code'][el['level_code'].index(group_code) : len(el['level_code'])]
    ret=models.HCSLS_JobWorking().aggregate()
    ret.left_join(models.HCSEM_Employees(), "report_to_job_w", "employee_code", "emp")
    if list_filter != None and len(list_filter) > 0:
        ret.match('gjw_code in {0}', list_filter)
    ret.project(
        job_w_code="job_w_code",
        job_w_name="job_w_name",
        report_to_job_w="emp.last_name + emp.first_name",
        ordinal="ordinal"
        )
    ret.sort(dict(
        ordinal = 1
        ))

    return ret