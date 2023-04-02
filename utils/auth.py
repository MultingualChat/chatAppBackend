from config import config
from jose import JWTError, jwt
from ext.db_connection import session_store, users_collection
import uuid
from loguru import logger
from fastapi import HTTPException, status


def generate_session(user_dict):
    logger.info(f"Generating JWT for user {user_dict['nickname']}")
    data = {'email': user_dict['email'], 'nickname': user_dict['nickname'], 'language': user_dict['language'], 'avatar': user_dict['avatar']}
    token = jwt.encode(data, config.JWT_SECRET, algorithm='HS256')

    logger.info(f"creating new session for user {user_dict['nickname']}")
    current_session = session_store.find_one({'user_id': user_dict['id']})
    if not current_session:
        session_id = str(uuid.uuid4())
        session_store.insert_one({'session_id': session_id, 'user_id': user_dict['id']})
    else:
        session_id = current_session['session_id']

    logger.info(f"session_id: {session_id}")

    return token


def validate_user(authorization):
    logger.info(f"Validating User")
    logger.info(f"Decoding JWT")
    data = jwt.decode(authorization.credentials, config.JWT_SECRET, algorithms=['HS256'])

    logger.info(f"Getting User {data['email']} from DB")
    user_dict = users_collection.find_one({'email': data['email']})

    if not user_dict:
        logger.error(f"User not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found")
    session = session_store.find_one({'user_id': user_dict['id']})
    if not session:
        logger.error(f"The session is already inactive")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Token Expire, please login again")
    return user_dict
