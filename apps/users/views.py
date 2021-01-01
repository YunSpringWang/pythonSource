from django.conf import settings
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib import auth
# Create your views here.
#全局环境设置：
def globbal_setting(request):
    return {'SITE_UID':settings.SITE_UID,
            'SITE_USER':settings.SITE_USER,
            'SITE_UNAME':settings.SITE_UNAME}
def home(request):
    # if request.method == 'POST':
    #     rdata={}
    #     username = request.POST['username']
    #     password = request.POST['password']
    #     r = requests.post(url='http://192.168.10.2:8080/api/Auth/login',
    #                       data={'grant_type': 'password', 'username': username, 'password': password,
    #                             'client_id': 'wispirit'})
    #     r.encoding = 'utf-8'
    #     datas = json.loads(r.text)
    #     r2 = requests.get(url='http://192.168.10.2:8080/api/Users/me', params={'access_token': datas['access_token']})
    #     r2.encoding = 'utf-8'
    #     users = json.loads(r2.text)
    #     rdata['access_token']=datas['access_token']
    #     rdata['url'] = "/teacher/home"
    #     try:
    #         uname = users['name']
    #         uid = users['account_uuid']
    #         access_token = datas['access_token']    #取得用户access_token
    #         settings.SITE_DATA = users      #全局变量设置用户信息
    #         request.session['sdatas']=users #session设置用户信息
    #         request.session['access_token']=datas['access_token']   #session设置用户信息
    #         response = HttpResponse(json.dumps(rdata))
    #         response.set_cookie('access_token',datas['access_token'],3600)#设置cookie过期为一小时
    #         settings.SITE_UNAME = uname #全局变量设置用户名
    #         settings.SITE_ACC = access_token    #全局变量设置用户access_token
    #     except:
    #         pass
    #     finally:
    #         # print(settings.SITE_UNAME)
    #         return HttpResponse(json.dumps(rdata))
    # else:
    #     pass
        # return HttpResponse('0')
    return render(request,'index.html',locals())
# 注销
def do_logout(request):
    try:
        logout(request)
    except Exception as e:
        print(e)
        # logger.error(e)
    return redirect(request.META['HTTP_REFERER'])

# # 注册
# def do_reg(request):
#     try:
#         if request.method == 'POST':
#             reg_form = RegForm(request.POST)
#             if reg_form.is_valid():
#                 # 注册
#                 user = User.objects.create(username=reg_form.cleaned_data["username"],
#                                     email=reg_form.cleaned_data["email"],
#                                     url=reg_form.cleaned_data["url"],
#                                     password=make_password(reg_form.cleaned_data["password"]),)
#                 user.save()
#
#                 # 登录
#                 user.backend = 'django.contrib.auth.backends.ModelBackend' # 指定默认的登录验证方式
#                 login(request, user)
#                 return redirect(request.POST.get('source_url'))
#             else:
#                 return render(request, 'basic/failure.html', {'reason': reg_form.errors})
#         else:
#             reg_form = RegForm()
#     except Exception as e:
#         print(e)
#         # logger.error(e)
#     return render(request, 'basic/reg.html', locals())

# 登录
def do_login(request):
    if request.method == 'GET':
        return render(request, 'users/login.html')
    else:
        # Json 返回登陆结果
        response = {'user': None, 'msg': None}
        # 提交的登陆post
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        valid_code = request.POST.get('valid_code')  # 图片验证码

        # 获取到session中的验证码值
        valid_code_str = request.session.get('valid_code_str')
        print(valid_code,valid_code_str)
        if valid_code.upper() == valid_code_str.upper():  # 不区分大小写
            # 进行账号认证
            user = auth.authenticate(username=user, password=pwd)
            print(user)
            if user:  # 有这个用户
                auth.login(request, user)  # request.user == 当前登陆对象
                response['user'] = user.username
            else:
                response['msg'] = '用户名或密码错误！'

        else:
            response['msg'] = '验证码错误'

        return JsonResponse(response)


def get_validCode_img(request):
    """
    给予PIL模块动态生产验证码
    :param request:
    :return:
    """
    from .utils.validCode import get_valid_code_img  # 导入自己创建的工具文件utils
    data = get_valid_code_img(request)
    print(data)
    return HttpResponse(data,'image/png')
