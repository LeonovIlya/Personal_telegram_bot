import logging
import locale
from sqlalchemy.exc import IntegrityError

from reminder.db.model import session, Reminder

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


def add_rec(user_id, datetime, text):
    try:
        record = Reminder(user_id=int(user_id),
                          text=text,
                          reminder_time=datetime
                          )
        session.add(record)
        try:
            session.commit()
            return True
        except IntegrityError:
            session.rollback()
            return False
    except Exception as error:
        logging.info(f'{error}')


def get_recs(user_id):
    try:
        recs = session.query(Reminder).filter(Reminder.done == False).order_by(
                                              Reminder.reminder_time.asc())
        result = [(str(i.reminder_time.strftime("%d %B в %H:%M")),
                   i.text)
                  for i in recs]
        return result
    except Exception as error:
        logging.info(f'{error}')


def check_recs(datetime):
    try:
        result = session.query(Reminder).filter(Reminder.reminder_time ==
                                                datetime, Reminder.done is not
                                                True).first()
        return result
    except Exception as error:
        logging.info(f'{error}')


def make_done_rec(rec_id):
    try:
        session.query(Reminder).filter(Reminder.id == rec_id).update({'done':
                                                                      True})
        session.commit()
    except Exception as error:
        logging.info(f'{error}')


def change_time(rec_id, new_time):
    try:
        session.query(Reminder).filter(Reminder.id == rec_id).update({
            'reminder_time': new_time})
        session.commit()
    except Exception as error:
        logging.info(f'{error}')
