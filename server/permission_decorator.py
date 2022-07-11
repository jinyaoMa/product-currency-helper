################################################################################
# Permission using Decorator pattern
#
# Purpose:
#
#
# Student Name: Jinyao Ma
# Student ID:   001433428
#
################################################################################

from abc import ABC, abstractmethod


class Permission(ABC):

    def __init__(self, bit):
        self.bit = bit  # set bit to 1 for allow access, 0 to deny

    @abstractmethod
    def get_string(self):
        pass

    def __repr__(self):
        return self.get_string()


class BasicPermission(Permission):

    def get_string(self):
        return "basic:" + str(self.bit)


class PermissionDecorator(Permission):

    __permission: Permission

    def __init__(self, permission, bit):
        self.__permission = permission
        super().__init__(bit)

    @property
    def permission(self):
        return self.__permission

    def get_string(self):
        return self.__permission.get_string()


class ManipulationPermission(PermissionDecorator):

    def get_string(self):
        return self.permission.get_string() + ",manipulation:" + str(self.bit)


class AdvancedPermission(PermissionDecorator):

    def get_string(self):
        return self.permission.get_string() + ",advanced:" + str(self.bit)
