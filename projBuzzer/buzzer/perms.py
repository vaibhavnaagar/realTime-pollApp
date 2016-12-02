from permission.logics import AuthorPermissionLogic
from permission.logics import CollaboratorsPermissionLogic

PERMISSION_LOGICS = (
    ('buzzer.Article', AuthorPermissionLogic()),
    ('buzzer.Article', CollaboratorsPermissionLogic()),
)
