from config import database, helpers, db_context
import base
_hasCreated=False
def HCSLS_TrainDomain():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "HCSLS_TrainDomain",
            "base",
            [["domain_code"]],
            domain_code=helpers.create_field("text", True),
            domain_name=helpers.create_field("text", True),
            ordinal=helpers.create_field("numeric"),
            note=helpers.create_field("text"),
            lock=helpers.create_field("bool"),
            domain_name2=helpers.create_field("text"),
            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text")
        )
        _hasCreated=True
    ret = db_context.collection("HCSLS_TrainDomain")

    return ret