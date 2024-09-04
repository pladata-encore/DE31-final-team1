from quart import Blueprint
from .components.database import * 
from .components.authorization import *

main_dg = Blueprint('data_group',__name__)

# API LIST
# 1. get data group list (GET)
# 2. create data group (POST)
# 3. get data group info (GET)

@main_dg.route('/getdglist/', methods=['GET', 'OPTIONS'])
async def getlist():
    # check token
    status_message = await check_token(req.email, req.token)
    # split status message, first part is status code, else is message
    code, message = status_message.split('_', 1)

    # if code is "ERR" then return error message
    if code == "ERR":
        return message, 401

    # get data source list
    dg_list_data = get_dg_list(req.email)

    return dg_list_data, 200


@main_dg.route('/createdg/', methods=['POST', 'OPTIONS'])
async def createdg():
    # check token
    status_message = await check_token(req.email, req.token)
    # split status message, first part is status code, else is message
    code, message = status_message.split('_', 1)

    # if code is "ERR" then return error message
    if code == "ERR":
        return message, 401

    # create data group
    status_message = create_dg(req.email, req.dg_name, req.dg_desc, req.dg_data)
    # split status message, first part is status code, else is message
    code, message = status_message.split('_', 1)

    # if code is "ERR" then return error message
    if code == "ERR":
        return message, 400

    return message, 200
    
    

@main_dg.route('/getdginfo/', methods=['GET', 'OPTIONS'])
async def getinfo():
    # check token
    status_message = await check_token(req.email, req.token)
    # split status message, first part is status code, else is message
    code, message = status_message.split('_', 1)

    # if code is "ERR" then return error message
    if code == "ERR":
        return message, 401

    # get data group info and data
    dg_info = get_dg_info(req.email, req.dg_id)
    dg_data = get_dg_data(req.email, req.dg_id)

    dg_info_data = {
        "info": dg_info,
        "data": dg_data
    }

    return dg_info_data, 200
