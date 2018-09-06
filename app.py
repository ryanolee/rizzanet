import rizzanet
app=rizzanet.app
if __name__ == '__main__':
    #Scan for all changes in templates and app dir
    #from formic import FileSet
    import os,time

    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    dir_name = os.path.dirname(__file__)
    extra_files = []#list(FileSet(include=[dir_name+'rizzanet/**/*', dir_name+'templates/**/*'],exclude=[dir_name+'rizzanet/admin/admin_app/**/*']))
    
    app.run(host='0.0.0.0', debug=True, port=8080, extra_files=extra_files)

            
        