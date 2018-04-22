from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool
from flask import g

Base = declarative_base()

def bind_app_events(app):
    global engine
    engine = create_engine('sqlite:///./database/rizza.db', convert_unicode=True, echo=True, poolclass=NullPool)
    sessioncreate = sessionmaker(autocommit=False,
                                            autoflush=False,
                                            bind=engine)
    scoped_session_maker = scoped_session(sessioncreate)
    db_session = scoped_session_maker()
    Base.query = scoped_session_maker.query_property()

    @app.before_first_request
    def init_db():
        '''Initilises schema for the database'''
        import rizzanet.models
        Base.metadata.create_all(bind=engine)
    from flask import request_tearing_down
    @app.after_request
    def close_db(response):

        if response.status_code == 500:
            g.db_session.rollback()
        g.db_session.close()
        g.db_session.remove()
        return response

    @app.before_request
    def start_session():
        g.db_session = scoped_session(sessioncreate)