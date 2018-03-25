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
            click.secho("Command failed: %s " % i_error._message, err=True, bg='red')
            return        
        click.echo('Creating article content type.')
        article=ContentType.create('article',{
            'title':str,
            'content':str
        },'content_types/article.html')
        click.echo('Creating article content object.')
        data = ContentData.create('article',{
            'title':'my content',
            'content':'This is as website!'
        })
        click.echo('Creating root content node.')
        root_node=Content(None,'root',article,data)
        g.db_session.add(root_node)
        g.db_session.commit()
        click.secho('Done!',fg='white',bg='green')
        #destroy_app_context(ctx)
        
    @rizzanet_cli.command(help='Drops all tables from the database.')
    def purge_db():
        from rizzanet.db import Base,engine
        click.secho("!!! WARNING Running this command will purge all data from the current database !!!",bg='red',blink=True)
        click.echo("Are you sure you wish to continue? [y/N]", nl=False)
        input_char = click.getchar()
        click.echo()
        if input_char.decode().upper() == 'Y':
            click.secho("Purging database ...")
            for tbl in reversed(Base.metadata.sorted_tables):
                click.echo('Dropping table %s ...' % tbl)
                tbl.drop(engine)
            click.secho('Done!',fg='white',bg='green')
        else:
            click.echo("Database purge aborted. No changes made.")
    
    
    app.cli.add_command(rizzanet_cli)
            