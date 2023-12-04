from typing import List

from fastapi import Depends, HTTPException, Request, status

from src.database.models import User, Role
from src.services.auth import auth_service


class RoleAccess:
    def __init__(self, allowed_roles: List[Role]):
        """
        The __init__ function is called when the class is instantiated.
            It sets up the instance of the class with a list of allowed roles.

        :param self: Represent the instance of the class
        :param allowed_roles: List[Role]: Define the allowed roles that can access the command
        :return: Nothing
        :doc-author: Trelent
        """
        self.allowed_roles = allowed_roles

    async def __call__(
        self,
        request: Request,
        current_user: User = Depends(auth_service.get_current_user),
    ):
        """
        The __call__ function is a decorator that takes in the request and current_user,
        and checks if the user's role is allowed to access this endpoint. If not, it raises an HTTPException.

        :param self: Refer to the class itself
        :param request: Request: Access the request object
        :param current_user: User: Get the current user from the database
        :param : Get the current user
        :return: A function that takes a request and current_user as arguments
        :doc-author: Trelent
        """
        print(request.method, request.url)
        print(f"User role: {current_user.role}")
        print(f"Allowed roles: {self.allowed_roles}")
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Operation forbidden"
            )
