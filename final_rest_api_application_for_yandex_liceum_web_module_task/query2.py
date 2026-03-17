from data.db_session import global_init, create_session
from data.users import User

from sqlalchemy import select

global_init(input())
sess = create_session()

users = select(User).where(User.address == 'module_1',
                           User.position.notilike['%engineer%'],
                           User.speciality.notilike(['%engineer%']))
print(*(user.id for user in sess.scalars(users)), sep='\n')