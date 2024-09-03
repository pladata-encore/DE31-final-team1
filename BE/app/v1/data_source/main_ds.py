from quart import Blueprint
from .components.database import * 
from .components.authorization import *

data_source_bp = Blueprint('data-source',__name__)

@data_source_bp.route('/getlist/', methods=['GET', 'OPTIONS'])
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
    ds_to_create = {
        "ds_id": req.ds_id,
        "ds_name": req.ds_name,
        "ds_type": req.ds_type,
        "ds_colnm": req.ds_colnm,
        "ds_data": req.ds_data
    }
    # split status message, first part is status code, else is message
    code, message = create_ds(req.email, req.ds_id, req.ds_name, req.ds_type, req.ds_colnm, req.ds_data).split('_', 1)

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