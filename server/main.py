from logger_chain import *
from permission_decorator import *
from record_factory import *
import configparser


config = configparser.ConfigParser()
config.read('config.server.cfg')

# Logger demo

tag_api_currency = "API|CURRENCY"
tag_api_amdoren_ = "API|AMDOREN_"
tag_act_service_ = "ACT|SERVICE_"

logger = None
if config["Log"]["console"] == "TRUE":
    logger = ConsoleLogger().next(logger)
if config["Log"]["file"] == "TRUE":
    logger = FileLogger(config["Log"]["log_file"]).next(logger)

logger.log(tag_act_service_, "test")

# Permission demo

permission = PermissionBasic(1)
permission = PermissionManipulation(permission, 1)
permission = PermissionAdvanced(permission, 0)

print(permission.get_string())

# Record demo

recordFactory = RecordFactory()
token = recordFactory.get_record("token", {
    "id": 1,
    "active": True,
    "access_token": "123",
    "permission": permission.get_string()
})

print(token.get_json())
