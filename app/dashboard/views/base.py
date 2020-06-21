from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from app.models.video import Origin, VideoType, Nationality, StartIdentify
from app.models.video import Video, VideoStar, VideoSub
from app.lib.commer_func import video_handel
from app.task.task import sayHello


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


class VideoHandle(View):
    TEMPLATE = 'dashboard/video_create.html'

    @method_decorator(login_required(login_url='login'))
    @admin_auth
    def get(self, request):
        page = int(request.GET.get("page", "1"))
        err_msg = request.GET.get("error", "")
        videos = Video.objects.all().order_by('-update_time')
        p = Paginator(videos, 10)  # 设置每页数据10条
        current_page = p.get_page(page)  # 返回当前页数据
        current_videos = current_page.object_list  # 当前页数据列表
        total_page = p.num_pages  # 总的页码

        data = {"nationalities": get_enum_list(Nationality),
                "origins": get_enum_list(Origin),
                "types": get_enum_list(VideoType),
                "videos": current_videos,
                "pageInfo": {"count": total_page, "countCircle": range(total_page)},
                "error": err_msg}
        return render(request, self.TEMPLATE, data)

    @method_decorator(login_required(login_url='login'))
    @admin_auth
    def post(self, request):
        video_id = request.POST.get("video_id")
        video_name = request.POST.get("video_name")
        video_image = request.POST.get("video_image")
        video_type = request.POST.get("video_type")
        video_origin = request.POST.get("video_origin")
        video_nationality = request.POST.get("video_nationality")

        if not all([video_name, video_image, video_type, video_origin, video_nationality]):
            error_msg = "必填字段为空"
            reverse_url = "{}?error={}".format(reverse('video'), error_msg)
            return redirect(reverse_url)

        result = get_enum(VideoType, video_type, "视频类型错误")
        if result["code"] == -1:
            reverse_url = "{}?error={}".format(reverse('video'), result["message"])
            return redirect(reverse_url)

        result = get_enum(Origin, video_origin, "视频来源错误")
        if result["code"] == -1:
            reverse_url = "{}?error={}".format(reverse('video'), result["message"])
            return redirect(reverse_url)
        result = get_enum(Nationality, video_nationality, "视频产地错误")
        if result["code"] == -1:
            reverse_url = "{}?error={}".format(reverse('video'), result["message"])
            return redirect(reverse_url)
        if not video_id:  # id 为空则新增视频
            try:
                Video.objects.create(video_name=video_name,
                                     video_type=VideoType(video_type).value,
                                     origin=Origin(video_origin).value,
                                     nationality=Nationality(video_nationality).value,
                                     image=video_image)
            except:
                reverse_url = "{}?error={}".format(reverse('video'), "新增视频失败")
                return redirect(reverse_url)
            return redirect(reverse('video'))
        else:  # 修改视频
            video = Video.objects.get(pk=video_id)
            video.video_name = video_name
            video.image = video_image
            video.video_type = video_type
            video.origin = video_origin
            video.nationality = video_nationality
            try:
                video.save()
            except:
                reverse_url = "{}?error={}".format(reverse('video'), "修改视频失败")
                return redirect(reverse_url)
            return redirect(reverse('video'))


class VideoDelete(View):
    def get(self, request, videoid):
        try:
            video = Video.objects.get(pk=videoid)
            video.delete()
        except:
            reverse_url = "{}?error={}".format(reverse('video'), "删除视频失败")
            return redirect(reverse_url)
        return redirect(reverse('video'))


class FileCreat(View):
    TEMPLATE = 'dashboard/file_create.html'
    startIdentify = get_enum_list(StartIdentify)

    def get(self, request, videoid):
        video = Video.objects.get(pk=videoid)
        video_subs = VideoSub.objects.filter(video=videoid)
        video_stars = VideoStar.objects.filter(video=videoid)
        return render(request, self.TEMPLATE,
                      {"video": video,
                       "videoid": videoid,
                       "startIdentify": self.startIdentify,
                       "video_subs": video_subs,
                       "video_stars": video_stars})

    def post(self, request, videoid):
        video = Video.objects.get(pk=videoid)
        video_subs = VideoSub.objects.filter(video=videoid)
        video_stars = VideoStar.objects.filter(video=videoid)

        if 'number' in request.POST:
            number = request.POST.get('number')
            origin = video.origin
            id = videoid
            print(origin)
            print(Origin.custom.value)
            if origin == Origin.custom.value:
                # 为上传文件
                videl_file = request.FILES.get('videl_url')
                if not all([id, videl_file, number]):
                    return render(request, self.TEMPLATE, {"file_info": "必填字段为空",
                                                           "videoid": videoid,
                                                           "startIdentify": self.startIdentify,
                                                           "video_subs": video_subs,
                                                           "video_stars": video_stars,
                                                           "video": video})
                video_handel(videl_file, videoid, int(number))

                return redirect("test")
            # 非文件上传
            videl_url = request.POST.get('videl_url')
            if not all([id, videl_url, number]):
                return render(request, self.TEMPLATE, {"file_info": "必填字段为空",
                                                       "videoid": videoid,
                                                       "startIdentify": self.startIdentify,
                                                       "video_subs": video_subs,
                                                       "video_stars": video_stars,
                                                       "video": video})
            video = Video.objects.get(pk=id)
            VideoSub.objects.create(video=video,
                                    number=number,
                                    url=videl_url)
            return render(request, self.TEMPLATE,
                          {"file_info": "创建成功", "videoid": videoid,
                           "startIdentify": self.startIdentify,
                           "video_subs": video_subs,
                           "video_stars": video_stars,
                           "video": video})
        elif 'actor_name' in request.POST:
            id = videoid
            actor_name = request.POST.get('actor_name')
            actor_type = request.POST.get('actor_type')
            if not all([id, actor_name, actor_type]):
                return render(request, self.TEMPLATE, {"actor_info": "必填字段为空",
                                                       "videoid": videoid,
                                                       "startIdentify": self.startIdentify,
                                                       "video_subs": video_subs,
                                                       "video_stars": video_stars,
                                                       "video": video})
            video = Video.objects.get(pk=id)
            VideoStar.objects.create(video=video,
                                     name=actor_name,
                                     identify=actor_type)
            return render(request, self.TEMPLATE,
                          {"actor_info": "新增演员信息成功",
                           "videoid": videoid,
                           "startIdentify": self.startIdentify,
                           "video_subs": video_subs,
                           "video_stars": video_stars,
                           "video": video})


class FileModify(View):
    def post(self, request):
        videoId = int(request.POST.get("videoid"))
        videoFileId = int(request.POST.get("videofileid"))
        videoNumber = request.POST.get("videonumber")
        videoUrl = request.POST.get("videlurl")

        videoSub = VideoSub.objects.filter(video=videoId).get(pk=videoFileId)
        videoSub.number = videoNumber
        videoSub.url = videoUrl
        videoSub.save()
        return redirect(reverse('file', kwargs={"videoid": videoId}))

import datetime
class Test(View):
    def get(self, request):
        print(datetime.datetime.now())
        sayHello.delay()
        print(datetime.datetime.now())
        return render(request, 'dashboard/test.html')
