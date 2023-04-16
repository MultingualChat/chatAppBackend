
from fastapi import HTTPException, status, Header, Depends, Response
from ext.db_connection import users_collection, session_store
import bcrypt
from loguru import logger
from .schemas import LoginBase
from utils.auth import generate_session, validate_user
from fastapi.security import HTTPBearer


security = HTTPBearer()


def login(user: LoginBase, response: Response):
    logger.info(f" !! LogIn path !!")
    logger.info(f"getting user {user.email} from DB")
    user_dict = users_collection.find_one({'email': user.email})
    
    if user_dict:
        hashed_password = user_dict['password'].encode('utf-8')
        if bcrypt.checkpw(user.password.encode('utf-8'), hashed_password):
            token = generate_session(user_dict)
            response.set_cookie(key="user", value=user_dict['nickname'], httponly=True)
            return {'access_token': token, 'token_type': 'bearer'}
        logger.error(f"Invalid password")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    else:
        logger.error(f"there is not user with email: {user.email}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"there is not user with email: {user.email}")


def logout(authorization: str = Depends(security)):
    logger.info(f" !! LogOut path !!")
    user_dict = validate_user(authorization)
    logger.info(f"deleting session for user {user_dict['email']} from DB")
    session_store.delete_one({'user_id': user_dict['id']})
    logger.info(f"user {user_dict['email']} logged out")
    return {'success': True}

