from quart import Blueprint
from .components.database import * 
from .components.authorization import *

data_source_bp = Blueprint('data-source',__name__)

# API LIST
# 1. get data source list (GET)
# 2. create data source (POST)
# 3. get data source info (GET)

@main_ds.route('/getdslist/', methods=['GET', 'OPTIONS'])
async def getlist():
    # check token
    status_message = await check_token(req.email, req.token)
    # split status message, first part is status code, else is message
    code, message = status_message.split('_', 1)

    # if code is "ERR" then return error message
    if code == "ERR":
        return message, 401

    # get data source list
    ds_list_data = get_ds_list(req.email)

    return ds_list_data, 200

@main_ds.route('/createds/', methods=['POST', 'OPTIONS'])
async def createds():
    # check token
    status_message = await check_token(req.email, req.token)
    # split status message, first part is status code, else is message
    code, message = status_message.split('_', 1)

    # if code is "ERR" then return error message
    if code == "ERR":
        return message, 401

    # create data source
    # split status message, first part is status code, else is message
    code, message = create_ds(req.email, req.id, req.name, req.type).split('_', 1)

    # if code is "ERR" then return error message
    if code == "ERR":
        return message, 400

    return message, 200
    
    

@data_source_bp.route('/getdsinfo/', methods=['GET', 'OPTIONS'])
async def getinfo():
    # check token
    status_message = await check_token(req.email, req.token)
    # split status message, first part is status code, else is message
    code, message = status_message.split('_', 1)

    # if code is "ERR" then return error message
    if code == "ERR":
        return message, 401

    # get data source info and data
    ds_info = get_ds_info(req.email, req.ds_id)
    ds_data = get_ds_data(req.email, req.ds_id)

    ds_info_data = {
        "info": ds_info,
        "data": ds_data
    }

    return ds_info_data, 200