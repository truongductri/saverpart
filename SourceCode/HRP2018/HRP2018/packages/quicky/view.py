from . import extens
from . import applications

from . import authorize
import threading
import logging
import os
import sys
from . import tenancy
logger=logging.getLogger(__name__)
global lock
settings=None
lock=threading.Lock()
_cache_view={}
def template_uri(fn):

    def layer(*args, **kwargs):
        def repl(f):
            return fn(f, *args, **kwargs)
        return repl
    return layer
@template_uri
def template(fn,*_path,**kwargs):

    if _path.__len__()==1:
        _path=_path[00]
    if _path.__len__()==0:
        _path=kwargs
    app = None
    if sys.version_info[0] <= 2:
        app=applications.get_app_by_file(fn.func_code.co_filename)
    else:
        app = applications.get_app_by_file(fn.__code__.co_filename)

    setattr(fn,"__application__",app)
    from . import get_django_settings_module
    is_multi_tenancy = get_django_settings_module().__dict__.get("USE_MULTI_TENANCY", False)
    def exec_request(request, **kwargs):
        from . import applications as apps

        setattr(threading.current_thread(), "user", request.user)
        setattr(threading.currentThread(), "user", request.user)
        _app = None
        if sys.version_info[0]<=2:
            _app= apps.get_app_by_file(fn.func_code.co_filename)
        else:
            _app = apps.get_app_by_file(fn.__code__.co_filename)
        print(request.session.session_key)
        if _app != None:
            if hasattr(_app.settings, "DEFAULT_DB_SCHEMA"):
                tenancy.set_schema(_app.settings.DEFAULT_DB_SCHEMA)
        global  settings
        if settings==None:
            from . import get_django_settings_module
            settings=get_django_settings_module()
        host_dir=None
        if hasattr(settings,"HOST_DIR"):
            host_dir=settings.HOST_DIR
        app=fn.__application__

        try:
            from django.shortcuts import redirect



            not_inclue_tenancy_code=False
            if hasattr(request,"not_inclue_tenancy_code"):
                not_inclue_tenancy_code=request.not_inclue_tenancy_code
            is_allow = True
            is_public = False
            authenticate = None
            request_path=request.path
            tenancy_code=tenancy.get_customer_code()
            if not not_inclue_tenancy_code and tenancy_code!=None:
                request_path=request_path[tenancy_code.__len__()+1:request_path.__len__()]
            if app == None:
                x=1

            if app==None and request_path[request_path.__len__() - 4:request_path.__len__()]=="/api":
                app_name=request_path.split('/')[request_path.split('/').__len__()-2]
                if app_name==tenancy_code:
                        app_name="" 
                from . import applications
                app=applications.get_app_by_name(app_name)
                if app != None:
                    if hasattr(app.settings, "DEFAULT_DB_SCHEMA"):
                        tenancy.set_schema(app.settings.DEFAULT_DB_SCHEMA)
                    else:
                        from . import get_tenancy_schema
                        _tenancy_code=request_path.split('/')[1]
                        _schema=get_tenancy_schema(request_path.split('/')[1])

                        setattr(threading.currentThread(), "tenancy_code", _tenancy_code)
                        setattr(threading.currentThread(), "request_tenancy_code", _schema)
                        setattr(request, "tenancy_code", _schema)


                else:
                    if sys.modules["settings"].MULTI_TENANCY_DEFAULT_SCHEMA == app_name:
                        app = applications.get_app_by_host_dir("")
                        if app != None:

                            setattr(threading.currentThread(),"tenancy_code",app_name)
                            setattr(threading.currentThread(),"request_tenancy_code",app_name)
                            setattr(request,"tenancy_code",app_name)
                    else:
                        app = applications.get_app_by_host_dir(app_name)
                        if app != None:
                            tenancy_code=request_path.split('/')[1];

                            setattr(threading.currentThread(),"tenancy_code",tenancy_code)
                            setattr(threading.currentThread(),"request_tenancy_code",tenancy_code)
                            setattr(request,"tenancy_code",tenancy_code)
                            if hasattr(app.settings, "DEFAULT_DB_SCHEMA"):
                                tenancy.set_schema(app.settings.DEFAULT_DB_SCHEMA)
                                setattr(request, "tenancy_code", app.settings.DEFAULT_DB_SCHEMA)



            if not hasattr(app, "settings") or app.settings==None:
                raise (Exception("'settings.py' was not found in '{0}' at '{1}' or look like you forgot to place 'import settings' in '{1}/__init__.py'".format(app.name, os.getcwd()+os.sep+app.path)))

            login_url = app.get_login_url()

            if hasattr(app.settings, "is_public"):
                is_public = getattr(app.settings, "is_public")

            # if not is_public or callable(authenticate):

            extens.apply(request, _path, app)
            if type(_path) is dict:
                if _path.get("is_public", False):
                    return fn(request, **kwargs)
                elif _path.get("login_url", None) != None:
                    if app.host_dir != "":
                        login_url = "/" + app.host_dir + "/" + _path["login_url"]
                    else:
                        login_url = "/" + _path["login_url"]

            # if login_url != None:
            #     cmp_url = login_url
            #     if host_dir != None:
            #         cmp_url = "/"+host_dir +  login_url
            #     if request.user.is_anonymous():
            #         if request.path_info.lower() == cmp_url.lower():
            #             return fn(request, **kwargs)
            #         else:
            #             url = request.get_abs_url() + login_url
            #             url += "?next=" + request.get_abs_url() + request.path
            #             return redirect(url)
            if hasattr(app.settings, "authenticate"):
                from django.http.response import HttpResponseRedirect
                ret_auth=app.settings.authenticate(request)
                if ret_auth != True:

                    if ret_auth == False:
                        if login_url==None:
                            raise (Exception("it look like you forgot set 'login_url' in {0}/settings.py".format(app.path)))
                        cmp_url=login_url
                        if host_dir!=None:
                            cmp_url = "/" + host_dir + login_url
                        if request.path_info.lower() == cmp_url.lower():
                            return fn(request, **kwargs)
                        url = request.get_abs_url() + login_url
                        url += "?next=" + request.get_abs_url() + request.path
                        return redirect(url)
                elif type(ret_auth) is HttpResponseRedirect:
                    return ret_auth

            return fn(request, **kwargs)
        except Exception as ex:
            logger.debug(ex)
            raise (ex)
    def exec_request_for_multi(request,tenancy_code, **kwargs):

        from . import get_tenancy_schema
        code=get_tenancy_schema(tenancy_code)
        if code==None:
            from django.http import HttpResponse, HttpResponseNotFound
            return HttpResponseNotFound("Page not found")
        setattr(threading.current_thread(),"tenancy_code",code)
        setattr(threading.currentThread(), "tenancy_code", code)
        setattr(threading.current_thread(),"request_tenancy_code",tenancy_code)
        setattr(threading.currentThread(), "request_tenancy_code", tenancy_code)
        setattr(threading.current_thread(),"user",request.user)
        setattr(threading.currentThread(), "user", request.user)

        return exec_request(request,**kwargs)
    if is_multi_tenancy:
        if app == None:
            return exec_request
        elif hasattr(app.settings, "DEFAULT_DB_SCHEMA"):
            if app.host_dir == "":
                return  exec_request_for_multi
            else:
                return exec_request
        else:
            return exec_request_for_multi
    else:


        return exec_request







