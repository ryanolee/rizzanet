import click
from flask.cli import AppGroup
from flask import g
from functools import wraps
def bind_cli_commands(app):
    '''Callback to bind CLI commands to app'''
    
    def build_app_context():
        ctx = app.test_request_context()
        ctx.push()
        app.preprocess_request()
        return ctx
    
    def destroy_app_context(ctx):
        app.process_response(app.response_class())
        ctx.pop()

    def in_app_context(func):
        '''Redirects to the current full path ('/login/{path}')'''
        @wraps(func)
        def context_wrap(*args,**kwargs):
            ctx = build_app_context()
            res = func(*args,**kwargs)
            destroy_app_context(ctx)
            return res
        return context_wrap
    
    rizzanet_cli=AppGroup('rizzanet',help='The Commands for rizzanet.')
    
    @rizzanet_cli.command(help='Installs rizzanet.')
    @click.option('-u','--username',help='The new username of the admin.', default='rizza')
    @click.option('-p','--password',help='The new password of the admin user.', default='rizza')
    @in_app_context
    def install(username,password):
        import sqlalchemy
        from rizzanet.models import User,Content,ContentType,ContentData
        from rizzanet.db import Base,engine
        #ctx = build_app_context()
        click.echo('Building database schema...')
        Base.metadata.create_all(bind=engine)
        click.echo('Creating user %s...' % username)
        admin_user=User('admin',username,password,99999)
        g.db_session.add(admin_user)
       
        click.echo('Comitting to database...')
        try:
            g.db_session.commit()
        except Exception as i_error:
            click.secho("Command failed: %s " % i_error, err=True, bg='red')
            return        
        click.echo('Creating article content type.')
        from rizzanet.migrations import Migration
        installer = Migration('install.yml',True)
        try: installer.load()
        except Exception as error:
            click.secho("Command failed: {0!s}".format(error), err=True, bg='red')
            return
        installer.commit()
        #from rizzanet.fieldtypes import StringType,LinkType
        '''article=ContentType.create('article',{
            'title':StringType,
            'content':StringType
        },'content_types/article.html')
        click.echo('Creating article content object.')
        data = ContentData.create('article',{
            'title':'my content',
            'content':'This is as website!'
        })
        click.echo('creating nav item...')

        nav_item=ContentType.create('nav_item',{
            'label':StringType,
            'link':LinkType
        })
        click.echo('Creating content structure.')
        root_node=Content(None,'root',article,data)
        g.db_session.add(root_node)
        
        
        
        g.db_session.commit()
        nav_bar = ContentData.create('nav_item',{
            'label':'nav_root',
            'link':root_node.id
        })
        root_node.add_child('nav',nav_bar).add_child('home',ContentData.create('nav_item',{
            'label':'home',
            'link':root_node.id
        }))'''
        g.db_session.commit()
        click.secho('Done!',fg='white',bg='green')
        #destroy_app_context(ctx)
    
    @rizzanet_cli.command(help='Creates database schema.')
    @in_app_context
    def create_schema():
        from rizzanet.models import User,Content,ContentType,ContentData
        from rizzanet.db import Base,engine
        click.echo('Building database schema...')
        Base.metadata.create_all(bind=engine)
        click.secho('Done!',fg='white',bg='green')

    @rizzanet_cli.command(help='Drops all tables from the database.')
    @click.option('-f','--force',help='Forces the command to execute without user confirmation.', is_flag=True)
    def drop_db(force):
        from rizzanet.db import Base,engine
        from rizzanet.models import Content,ContentData,ContentType,User,APIKey
        input_char = b''
        if force:
            click.echo("Force flag set. Dropping all tables...")
        else:
            click.secho("!!! WARNING Running this command will purge all data from the current database !!!",bg='red',blink=True)
            click.echo("Are you sure you wish to continue? [y/N]", nl=False)
            input_char = click.getchar()
            click.echo()
        if input_char.upper() == 'Y' or force:
            click.secho("Purging database ...")
            for tbl in reversed(Base.metadata.sorted_tables):
                click.echo('Dropping table %s ...' % tbl)
                tbl.drop(engine)
            click.secho('Done!',fg='white',bg='green')
        else:
            click.echo("Database purge aborted. No changes made.")
    
    @rizzanet_cli.command(help='Creates an API key for rizzanet.')
    @in_app_context
    def create_api_key():
        from rizzanet.models import APIKey
        import secrets
        key = secrets.token_urlsafe(64)
        api_key = APIKey.create(key)
        g.db_session.commit()
        key = APIKey.to_base64('{0}__{1}'.format(api_key.id, key))
        click.secho('Api key created! Take note of this secret as it will be non recoverable.',fg='white',bg='green')
        click.secho(key,fg='white',bg='green')

    @rizzanet_cli.command(help='Reindexes elastic search for rizzanet.')
    @in_app_context
    def reindex_elasticsearch():
        from rizzanet.elasticsearch import ContentES,ContentDataES,getConnectionFromApp
        from elasticsearch import Elasticsearch       
        conn = getConnectionFromApp(app)
        ContentES(conn).reindex() 
        ContentDataES(conn).reindex()


    app.cli.add_command(rizzanet_cli)
            