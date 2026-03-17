from data.db_session import create_session, global_init
from data.users import User

from sqlalchemy import select

global_init(input())
sess = create_session()

users = select(User).where(User.address == 'module_1')
print(*sess.scalars(users), sep='\n')