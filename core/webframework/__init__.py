# -*- coding: utf-8 -*-

"""

    Module :mod:``


    LICENSE: The End User license agreement is located at the entry level.

"""

# ----------- START: Native Imports ---------- #
__import__('pkg_resources').declare_namespace(__name__)
# ----------- END: Native Imports ---------- #

# ----------- START: Third Party Imports ---------- #
import sqlite3

from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
# ----------- END: Third Party Imports ---------- #

# ----------- START: In-App Imports ---------- #
# ----------- END: In-App Imports ---------- #

__all__ = [
    # All public symbols go here.
]


def create_session():
    """."""
    # application starts
    Session = sessionmaker()
    conn = sqlite3.connect('example.db')

    #c = conn.cursor()
    # Create table
    #c.execute('''CREATE TABLE user (id number, username text, password text)''')
    #c.execute('''insert into user (id, username, password) values (1, 'admin', 'admin')''')
    #ss = c.execute('''select * from user''')

    # ... later
    engine = create_engine('sqlite:///example.db')
    Session.configure(bind=engine)

    session = Session()

    #session.execute('''insert into user (id, user, passwd) values (1, 'siva', 'sri')''')
    return session


class use_transaction(object):

    def __init__(self, _func):
        self._func = _func

    def __call__(self, *args, **kwargs):

        #form_data = decode_form_data(brequest.forms)
        session = create_session()
        _response = None

        #if form_data:
        #    kwargs['form_data'] = form_data

        try:
            _response = self._func(session, *args, **kwargs)
        except SQLAlchemyError:
            session.rollback()
        else:
            session.commit()

        return _response
