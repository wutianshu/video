from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from app.models.video import Origin, VideoType, Nationality
from app.models.video import Video


def admin_auth(func):
    def inner(obj, request, *args, **kwargs):
        if request.user.is_superuser:
            return func(obj, request, *args, **kwargs)
        else:
            return redirect(reverse('admin_permission'))

    return inner


class Index(View):
    TEMPLATE = 'dashboard/index.html'

    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        user = str(request.user)
        data = {"user": user}
        return render(request, self.TEMPLATE, data)


class Admin(View):
    TEMPLATE = 'dashboard/admin.html'
    TEMPLATE_PERMISSION = 'dashboard/auth/permission.html'

    @method_decorator(login_required(login_url='login'))
    @admin_auth
    def get(self, request):
        username = request.GET.get("username", "")
        page = request.GET.get("page", 1)
        page = int(page)
        if username:
            users = User.objects.filter(username__contains=username).order_by('id')
        else:
            users = User.objects.all().order_by('id')
        total_users = users.count()
        p = Paginator(users, 10)
        current_page = p.get_page(page)
        users = current_page.object_list
        total_page = p.num_pages
        return render(request, self.TEMPLATE,
                      {"users": users, "total_page": total_page, "total_users": total_users, "current_page": page,
                       "query_name": username})


class Admin_setting(View):
    @method_decorator(login_required(login_url='login'))
    @admin_auth
    def get(self, request):
        seeting = request.GET.get("setting")
        username = request.GET.get("username")
        user = User.objects.get(username=username)
        if seeting == 'on':
            user.is_superuser = True
        elif seeting == 'off':
            user.is_superuser = False
        user.save()
        return redirect(reverse('admin'))


def get_enum_list(enum):
    l = []
    for e in enum:
        l.append({"name": e.value, "label": e.label})
    return l


def get_enum(e, v, msg):
    try:
        e(v)
        return {"code": 0, "message": "success"}
    except:
        return {"code": -1, "message": msg}


class VideoCreate(View):
    TEMPLATE = 'dashboard/video_create.html'

    def get(self, request):
        videos = Video.objects.filter(origin=Origin('YOUKU').value)
        data = {"nationalities": get_enum_list(Nationality),
                "origins": get_enum_list(Origin),
                "types": get_enum_list(VideoType),
                "videos": videos}
        return render(request, self.TEMPLATE, data)

    def post(self, request):
        video_name = request.POST.get("video_name")
        video_image = request.POST.get("video_image")
        video_type = request.POST.get("video_type")
        video_origin = request.POST.get("video_origin")
        video_nationality = request.POST.get("video_nationality")

        if not all([video_name, video_image, video_type, video_origin, video_nationality]):
            data = {"error": "必填字段为空"}
            return render(request, self.TEMPLATE, data)

        result = get_enum(VideoType, video_type, "视频类型错误")
        if result["code"] == -1:
            data = {"error": result["message"]}
            return render(request, self.TEMPLATE, data)
        result = get_enum(Origin, video_origin, "视频来源错误")
        if result["code"] == -1:
            data = {"error": result["message"]}
            return render(request, self.TEMPLATE, data)
        result = get_enum(Nationality, video_nationality, "视频产地错误")
        if result["code"] == -1:
            data = {"error": result["message"]}
            return render(request, self.TEMPLATE, data)

        Video.objects.create(video_name=video_name,
                             video_type=VideoType(video_type).value,
                             origin=Origin(video_origin).value,
                             nationality=Nationality(video_nationality).value,
                             image=video_image,
                             )
        return redirect(reverse('video'))
