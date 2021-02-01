from db.db_connect import User, Notice, Interaction, session
from sqlalchemy.sql import exists
from datetime import datetime


def is_user_exists(tg_id):
    user_exists = session.query(exists().where(User.tg_id == tg_id)).scalar()
    return user_exists


def create_user(tg_id):
    if is_user_exists(tg_id):
        return 'This user alredy exists'
    else:
        user = User(tg_id)
        session.add(user)
        session.commit()


def get_user_by_tg_id(tg_id):
    user = session.query(User).filter(User.tg_id == tg_id).first()
    return user


def is_user_has_close_notices(tg_id, gp, gp_type):
    notices = session.query(Notice).join(User).filter(User.tg_id == tg_id).all()
    for notice in notices:
        if notice.gp - 1 < gp < notice.gp + 1 and notice.type.name == gp_type:
            return True
    return False


def create_notice(tg_id, gp, gp_type):
    user_id = get_user_by_tg_id(tg_id).id
    notice = Notice(user_id, gp, gp_type)
    session.add(notice)
    session.commit()
    return notice


def delete_notice(notice_id):
    session.query(Notice).filter(Notice.id == notice_id).delete(synchronize_session=False)
    session.commit()


def get_user_notices(tg_id):
    user_notices = session.query(Notice).join(User).filter(User.tg_id == tg_id).all()
    return user_notices


def get_notices_larger_arg_by_type(arg, type):
    notices_query = session.query(Notice).filter(Notice.gp >= arg, Notice.type == type).all()
    return notices_query


def delete_user(user):
    for notice in get_user_notices(user.tg_id):
        delete_notice(notice.id)
    res = session.query(User).filter(User.id == user.id).delete(synchronize_session=False)
    session.commit()


def create_interaction(tg_id):
    user = get_user_by_tg_id(tg_id)
    now = datetime.now()
    interaction = Interaction(user.id, now)
    session.add(interaction)
    session.commit()
