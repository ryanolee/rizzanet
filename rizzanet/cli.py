import click
from flask.cli import AppGroup
def bind_cli_commands(app):
    '''Callback to bind CLI commands to app'''
    rizzanet_cli=AppGroup('rizzanet',help='The Commands for rizzanet.')
    
    @rizzanet_cli.command(help='Installs rizzanet.')
    @click.option('-u','--username',help='The new username of the admin.', default='rizza')
    @click.option('-p','--password',help='The new password of the admin user.', default='rizza')
    def install(username,password):
        import sqlalchemy
        from rizzanet.models import User,Content
        from rizzanet.db import db_session
        click.echo('Creating user %s...' % username)
        admin_user=User('admin',username,password,99999)
        db_session.add(admin_user)
        click.echo('Creating root content node.')
        root_node=Content(None,'root',0,0)
        db_session.add(root_node)
        click.echo('Comitting to database...')
        try:
            db_session.commit()
        except Exception as i_error:
            click.secho("Command failed: %s " % i_error._message, err=True, bg='red')
            return
        child=root_node.add_child('index',0,0)
        click.echo('Creating index content node. %r'%child)
        click.secho('Done!',fg='white',bg='green')
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
            