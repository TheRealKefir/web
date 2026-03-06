from data.users import User
from data.jobs import Jobs
from data.db_session import create_session, global_init





global_init("./db/testdb.sqlite")
session = create_session()
capitan = {'surname': "Scott",
           'name': "Ridley",
           'age': 21,
           'position': "captain",
           'speciality': "research engineer",
           'address': "module_1",
           'email': "scott_chief@mars.org"}

user1 = {'surname': "Lovin",
           'name': "Mc",
           'age': 25,
           'position': "Driver",
           'speciality': "python developer",
           'address': "892 Momona ST",
           'email': "McLovin@mars.org"}
dwayne = {'surname': "Johnson",
           'name': "Dwayne",
           'age': 50,
           'position': "Skala",
           'speciality': "film actor",
           'address': "moana",
           'email': "dwayne@mars.org"}

johnny = {'surname': "Sins",
           'name': "Johnny",
           'age': 47,
           'position': "boss",
           'speciality': "too many specialities",
           'address': "Pittsburg",
           'email': "good_man@gmail.com"}

user = User(**capitan)
user1 = User(**user1)
user2 = User(**dwayne)
user3 = User(**johnny)
session.add(user)
session.add(user1)
session.add(user2)
session.add(user3)
session.commit()
session.close()


