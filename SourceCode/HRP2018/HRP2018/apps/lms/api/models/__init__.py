import django
import quicky
import authorization
import qmongo
from qmongo import database, helpers
app=quicky.applications.get_app_by_file(__file__)
db_context=database.connect(app.settings.Database)
from SYS_FunctionList import SYS_FunctionList
from HCSSYS_DataDomain import HCSSYS_DataDomain
from HCSSYS_Departments import HCSSYS_Departments
from SYS_ValueList import SYS_ValueList
from HCSSYS_SystemConfig import HCSSYS_SystemConfig
from LMSLS_MaterialFolder import LMSLS_MaterialFolder
from HCSSYS_ComboboxList import HCSSYS_ComboboxList
from HCSEM_Employees import HCSEM_Employees