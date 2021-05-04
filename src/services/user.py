# -*- coding: utf-8 -*-

from fastapi import Request

from db.crud.user import User as UserCRUD
from services.operation_log import set_new_data_id


async def add_user(request: Request, info, owner: int = None):
    user_crud = UserCRUD(request.app.state.pgpool)
    current_user = request.state.current_user
    # print("current_user = ", request.state.current_user)

    # eq 0 means root user
    # Users created by this user or its sub-users belong to this user
    if owner == None:
        owner = current_user.owner or current_user.id

    user = await user_crud.add_user( \
        username=info.username, password=info.password, \
        creator=current_user.id, owner=owner, email=info.email)

    # for oplog
    await set_new_data_id(request, user.id)     # user.json()

    return user