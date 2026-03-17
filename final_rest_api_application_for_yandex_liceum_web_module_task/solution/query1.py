from data import db_session
from data.users import User

from sqlalchemy import select

db_session.global_init(input())
sess = db_session.create_session()

users = select(User)
print(*sess.scalars(users), sep='\n')