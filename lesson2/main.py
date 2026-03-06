from data.users import User
import data.db_session as db_session

from sqlalchemy import select

db_session.global_init(input())
session = db_session.create_session()

stmt = select(User).where(User.address == '1',
                          User.position.notlike('engineer'),
                          User.position.notlike("engineer"))

print(*(user.id for user in session.scalars(stmt)), sep='\n')
