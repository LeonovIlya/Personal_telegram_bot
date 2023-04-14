"""Модуль работы с базой данных напоминаний"""

import logging
import locale
from datetime import datetime as dt
from typing import Any, Optional
from sqlalchemy.exc import IntegrityError

from reminder.db.model import session, Reminder

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


# добавляем запись
def add_rec(user_id: int, datetime: dt, text: str) -> Optional[bool]:
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
        logging.info('%s', error)
        return None


# получаем все записи для пользователя
def get_recs(user_id: int) -> Optional[list[tuple[str, Any]]]:
    try:
        recs = session.query(Reminder)\
            .filter(Reminder.done is False)\
            .filter(Reminder.user_id == user_id)\
            .order_by(Reminder.reminder_time.asc())
        result = [(str(i.reminder_time.strftime("%d %B в %H:%M")),
                   i.text)
                  for i in recs]
        return result
    except Exception as error:
        logging.info('%s', error)
        return None


# проверяем записи
def check_recs(datetime: str) -> Optional[tuple]:
    try:
        result = session.query(Reminder).filter(Reminder.reminder_time ==
                                                datetime, Reminder.done is not
                                                True).first()
        return result
    except Exception as error:
        logging.info('%s', error)
        return None


# помечаем запись выполненной
def make_done_rec(rec_id: int) -> None:
    try:
        session.query(Reminder).filter(Reminder.id == rec_id).update({'done':
                                                                      True})
        session.commit()
        return None
    except Exception as error:
        logging.info('%s', error)
        return None


# меняем время напоминания в записи
def change_time(rec_id: int, new_time: dt) -> None:
    try:
        session.query(Reminder).filter(Reminder.id == rec_id).update({
            'reminder_time': new_time})
        session.commit()
        return None
    except Exception as error:
        logging.info('%s', error)
        return None
