from quart import Blueprint
from .components.database import * 
from .components.authorization import *

main_ds = Blueprint('data_source',__name__)

@main_ds.route('/getlist/', methods=['GET', 'OPTIONS'])
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
    
    

@main_ds.route('/getdsinfo/', methods=['GET', 'OPTIONS'])
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