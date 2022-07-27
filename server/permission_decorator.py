################################################################################
# Permission using Decorator pattern
#
# Purpose: Define an abstract class for permission to make up mandatory
#          permission string. Define an abstract decorator to allow optional
#          permissions to build on top of the mandatory permission.
#          Implementation refers to /$references/decorator.jpg
#          from the project root folder.
#
# Reason to use Decorator pattern:
#  - need to allow different permissions to be composed together
#
# Student Name: Jinyao Ma
# Student ID:   001433428
#
################################################################################

from abc import ABC, abstractmethod


class Permission(ABC):
    ##
    # Permission abstract permission defined with a bit to control permission
    ##

    def __init__(self, bit):
        # set bit to 1 for allow access, 0 to deny
        self.bit = bit

    # Get permission string
    @abstractmethod
    def get_string(self):
        pass

    def __repr__(self):
        # in case, for string concat directly
        return self.get_string()


class BasicPermission(Permission):
    ##
    # BasicPermission basic permission
    ##

    def get_string(self):
        return "basic:" + str(self.bit)


class PermissionDecorator(Permission):
    ##
    # PermissionDecorator decorator to link a permission and build on the top of it
    ##

    __permission: Permission

    def __init__(self, permission, bit):
        self.__permission = permission  # to build on the top of this permission
        super().__init__(bit)

    @property
    def permission(self):
        return self.__permission

    # Get the whole permission string with all optional permissions
    # built on the top of the mandatory permission
    def get_string(self):
        return self.__permission.get_string()


class ManipulationPermission(PermissionDecorator):
    ##
    # ManipulationPermission decorator to add on manipulation permission
    ##

    def get_string(self):
        return self.permission.get_string() + ",manipulation:" + str(self.bit)


class AdvancedPermission(PermissionDecorator):
    ##
    # AdvancedPermission decorator to add on advanced permission
    ##

    def get_string(self):
        return self.permission.get_string() + ",advanced:" + str(self.bit)
