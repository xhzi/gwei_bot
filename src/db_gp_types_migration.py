import enum
from db.db_connect import *

def migrate():
    notices = session.query(Notice).all()
    for notice in notices:
        if notice.type == GP_type.fastest:
            notice.type = GP_type.fast
        if notice.type == GP_type.standard:
            notice.type = GP_type.average
        print(notice)
        session.commit()

if __name__ == '__main__':
    migrate()