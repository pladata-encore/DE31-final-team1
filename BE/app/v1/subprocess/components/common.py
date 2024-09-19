from app.v1.users.components.common import *
from quart import jsonify
from app.models.model import *
from sqlalchemy.future import select
from datetime import datetime, timedelta
import logging


async def check_token(email, token):
    # function to check if the token is valid
    # get token from db by email
    try : 
        async with get_session() as session:
            stmt = await get_token_info(email) # CODE_TO_GET_TOKEN_FROM_DB
            access_token, exp_time = stmt.AccessToken, stmt.ExpiryAt
            current_time = datetime.now()

            if stmt is None:
                return "ERR_NO_USER_INFO"

            # if token is not in db, return false
            if access_token is None:
                return "ERR_NO_TOKEN"

            # if token is expired, return false
            if exp_time < current_time:
                return "ERR_EXPIRED_TOKEN"

            # if token is not matched, return false
            if access_token != token:
                return "ERR_NOT_MATCHED_TOKEN"

            # if expired time is less than 30 min, update exp_time and return true
            time_left = exp_time - current_time
            if time_left < timedelta(minutes=30):
                update_token = await verify_token(email)
                if update_token:
                    return "OK_UPDATED_EXPIRE_TIME"
        
            # else return true
            return "OK_VALID_TOKEN"
        
    except Exception as e:
        logging.error(f"Error checking token for email {email}: {str(e)}")
        return "ERR_DATABASE_ERROR"