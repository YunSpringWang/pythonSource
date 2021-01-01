# Create your views here.
import json

from django.shortcuts import render, HttpResponse, redirect
from django.views import View
######################################
# 自建模块
######################################

from .models import *
from django.core.paginator import Paginator, PageNotAnInteger


# Create your views here.

class Struct(dict):
    """
    - 为字典加上点语法. 例如:
    >>> o = Struct({'a':1})
    >>> o.a
    >>> 1
    >>> o.b
    >>> None
    """

    def __init__(self, dictobj={}):
        self.update(dictobj)

    def __getattr__(self, name):
        # Pickle is trying to get state from your object, and dict doesn't implement it.
        # Your __getattr__ is being called with "__getstate__" to find that magic method,
        # and returning None instead of raising AttributeError as it should.
        if name.startswith('__'):
            raise AttributeError
        return self.get(name)

    def __setattr__(self, name, val):
        self[name] = val

    def __hash__(self):
        return id(self)


def paginator(data_list, per_page, page_no):
    """
       功能说明      封装Django自带的分页函数
       接收三个值：需要分页的对象，每页多少条数据，需要返回的页码
       返回三个值：分页后的对象，需要返回的页码，分页信息
       """
    data = Struct()
    pages = Paginator(data_list, per_page)

    # 防止超出页数
    if not page_no > 0:
        page_no = 1
    if page_no > pages.num_pages:
        page_no = pages.num_pages

    p = pages.page(page_no)
    data.count = pages.count
    data.page_num = pages.num_pages
    data.per_page = per_page
    data.current = page_no
    data.start_index = p.start_index() - 1

    return p.object_list, page_no, data


def chromebookhome(request):
    if request.method == "GET":
        pageSize = request.GET.get('pageSize')
        pageNumber = request.GET.get('pageNumber')
        searchText = request.GET.get('searchText')
        sortName = request.GET.get('sortName')
        sortOrder = request.GET.get('sortOrder')

        test_data = {
            "data_id": 1,
            "ipaddr_name": "localhost",
            "ipaddr_public": "127.0.0.1",
            "ipaddr_inner": "10.17.80.58",
            "quanta_model": "0GJ",
            "google_model": "Drawlat",
            "HP_model": "Hitchcock",
            "ipType": 2,
            "ip_Port": "7161",
            "ipstatus": 1,
            "engine_manager": "spring wang"
        }
        test_data2 = {
            "data_id": 2,
            "ipaddr_name": "localhost",
            "ipaddr_public": "127.0.0.1",
            "ipaddr_inner": "10.17.80.58",
            "quanta_model": "0GJ",
            "google_model": "Drawlat",
            "HP_model": "Hitchcock",
            "ipType": 2,
            "ip_Port": "7161",
            "ipstatus": 1,
            "engine_manager": "spring wang"
        }
        rows = []
        rows.append(test_data)
        rows.append(test_data2)
        data = {"errcode": 0,
                "errmsg": "ok",
                "count": 3,
                "data": rows}
        return_dict = {"ret": True, "errMsg": "", "rows": rows, "total": "1"}

        return render(request, 'chromebook/chrome_server_list.html', {"ret": json.dumps(return_dict)})


######################################
# 主机列表
######################################
def HostListView(request):
    if request.method == "GET":
        # 获取主机记录
        host_records = HostInfo.objects.filter(host_port_status=1).order_by('-update_time')
        print(host_records)
        # 筛选条件
        # 记录数量
        record_nums = host_records.count()
        paginator = Paginator(host_records, 3)  # 对所有数据进行分页

        try:  # 捕捉前台传过来的数据，传过来不正常的数据都跳到第一页
            current_page_num = int(request.GET.get('page'))  # 前台传过来的要拿一页
            current_page = paginator.page(current_page_num)  # 拿哪一页
            print(current_page.object_list)  # 拿哪一页的所有数据

            # 这可以循环当前页的对象 paginator.page 也可以循环当前页的内容 current_page.object_list
            # for item in current_page:
            #     print(item.name)

            if paginator.num_pages > 11:  # 判断总页数是否大于 10 页
                if current_page_num - 5 < 1:  # 页数小于前5页就显示前10页
                    current_range = range(1, 11)
                elif current_page_num + 5 > paginator.num_pages:  # 页数大于最后5页就显示最后10页
                    current_range = range(paginator.num_pages - 10, paginator.num_pages + 1)
                else:
                    current_range = range(current_page_num - 5, current_page_num + 5)  # 其他范围为-5页到+5页
            else:
                page_range = paginator.page_range  # 小于10页就显示所有页数

        except Exception as e:
            current_page_num = 1  # 随便乱传取第一页
            current_page = paginator.page(current_page_num)  # 随便乱传则取第一页
            current_range = range(1, 12)
        # 分页处理后的 QuerySet
        context={
            'host_records': current_page,
        }
        return render(request, 'chromebook/host_list.html', context=context)


######################################
# 添加主机
######################################
class AddHostInfoView(View):
    def post(self, request):
        host = HostInfo()
        host.in_ip = request.POST.get('in_ip')
        host.out_ip = request.POST.get('out_ip', '')
        host.system_id = int(request.POST.get('system'))
        host.hostname = request.POST.get('hostname')
        host.cpu = request.POST.get('cpu')
        host.disk = int(request.POST.get('disk'))
        host.memory = int(request.POST.get('memory'))
        host.network = int(request.POST.get('network'))
        host.ssh_port = int(request.POST.get('ssh_port'))
        host.root_ssh = request.POST.get('root_ssh')
        host.op_env_id = int(request.POST.get('op_env'))
        host.use_id = int(request.POST.get('use'))
        host.project_id = int(request.POST.get('project'))
        host.idc_id = int(request.POST.get('idc'))
        host.admin_user = request.POST.get('admin_user')
        host.admin_pass = request.POST.get('admin_pass')
        host.normal_user = request.POST.get('normal_user', '')
        host.normal_pass = request.POST.get('normal_pass', '')
        host.op_user_id = int(request.POST.get('op_user'))
        host.update_user = request.user
        host.desc = request.POST.get('desc', '')
        host.save()
        return HttpResponse('{"status":"success", "msg":"主机信息添加成功！"}', content_type='application/json')

######################################
# 主机列表
######################################
def CheckServerDetailsView(request):
    if request.method == "GET":
        # 获取主机记录
        host_records = HostInfo.objects.filter(host_port_status=1).order_by('-update_time')
        print(host_records)
        # 筛选条件
        # 记录数量
        record_nums = host_records.count()
        paginator = Paginator(host_records, 3)  # 对所有数据进行分页

        try:  # 捕捉前台传过来的数据，传过来不正常的数据都跳到第一页
            current_page_num = int(request.GET.get('page'))  # 前台传过来的要拿一页
            current_page = paginator.page(current_page_num)  # 拿哪一页
            print(current_page.object_list)  # 拿哪一页的所有数据

            # 这可以循环当前页的对象 paginator.page 也可以循环当前页的内容 current_page.object_list
            # for item in current_page:
            #     print(item.name)

            if paginator.num_pages > 11:  # 判断总页数是否大于 10 页
                if current_page_num - 5 < 1:  # 页数小于前5页就显示前10页
                    current_range = range(1, 11)
                elif current_page_num + 5 > paginator.num_pages:  # 页数大于最后5页就显示最后10页
                    current_range = range(paginator.num_pages - 10, paginator.num_pages + 1)
                else:
                    current_range = range(current_page_num - 5, current_page_num + 5)  # 其他范围为-5页到+5页
            else:
                page_range = paginator.page_range  # 小于10页就显示所有页数

        except Exception as e:
            current_page_num = 1  # 随便乱传取第一页
            current_page = paginator.page(current_page_num)  # 随便乱传则取第一页
            current_range = range(1, 12)
        # 分页处理后的 QuerySet
        context = {
            'host_records': current_page,
        }
        return render(request, 'chromebook/query_check_server_details.html', context=context)