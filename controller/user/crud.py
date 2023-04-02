import uuid
from ext.db_connection import users_collection
from loguru import logger
from .schemas import UserCreateResponse, UserEdit, UserObjResponse, User
from fastapi import Header, Depends
import bcrypt
from utils.auth import validate_user, generate_session
from fastapi.security import HTTPBearer

security = HTTPBearer()


def user_exists(email):
    logger.info('Validating if email already exists')
    user_dict = users_collection.find_one({'email': email})
    if user_dict:
        return True
    return False


def create_new_user(user: User):
    logger.info(f" !! Creating User !!: {user.email}")

    data = user.dict()
    if user_exists(data['email']):
        msg = "There is already an user with the same email"
        logger.error(msg)
        return {"email": msg}

    logger.info('encoding password')
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    data['password'] = hashed_password.decode('utf-8')
    data['id'] = str(uuid.uuid4())

    try:
        logger.info('creating user in DB')
        user_dict = users_collection.insert_one(data)
    except Exception as e:
        logger.error(e)
        return {"something fail": str(e)}
    token = generate_session(data)
    res = UserCreateResponse(**{'access_token': token, 'token_type': 'bearer', 'user': UserObjResponse(**user.to_json())})

    return res


def edit_user(user: UserEdit, authorization: str = Depends(security)):
    logger.info(f" !! Updating path !!")
    user_dict = validate_user(authorization)
    data = user.dict()

    logger.info(f"updating user {user_dict['email']}")
    for k, v in data.items():
        if v:
            user_dict[k] = v
    users_collection.update_one({'email': user_dict['email']}, {"$set": user_dict})
    user_dict = UserObjResponse(**users_collection.find_one({'email': user_dict['email']}))
    logger.info(f"updated")
    return user_dict



