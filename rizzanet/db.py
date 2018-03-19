from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool

engine = create_engine('sqlite:///./database/rizza.db', convert_unicode=True, echo=True, poolclass=NullPool)
sessioncreate = sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine)
global db_session
scoped_session_maker = scoped_session(sessioncreate)
db_session = scoped_session_maker()
Base = declarative_base()
Base.query = scoped_session_maker.query_property()

def init_db():
    '''Initilises schema for the database'''
    import rizzanet.models
    Base.metadata.create_all(bind=engine)

def bind_app_events(app):
    from flask import request_tearing_down
    @app.after_request
    def close_db(response):
        global db_session
        if response.status_code == 500:
            db_session.rollback()
        db_session.close()
        db_session.remove()
        return response

    @app.before_request
    def start_session():
        global db_session
        db_session = scoped_session(sessioncreate)