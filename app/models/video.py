# coding: utf-8

from django.db import models
from enum import Enum


class Origin(Enum):
    youku = 'YOUKU'
    custom = 'CUSTOM'


Origin.youku.label = '优酷'
Origin.custom.label = '自制'


class VideoType(Enum):
    movie = 'MOVIE'
    cartoon = 'CARTOON'
    episode = 'EPISODE'
    variety = 'VARIETY'
    other = 'OTHER'


VideoType.movie.label = '电影'
VideoType.cartoon.label = '动漫'
VideoType.episode.label = '剧集'
VideoType.variety.label = '综艺'
VideoType.other.label = '其他'


class Nationality(Enum):
    china = 'CHINA'
    japan = 'JAPAN'
    korea = 'KOREA'
    other = 'OTHER'


Nationality.china.label = '中国'
Nationality.japan.label = '日本'
Nationality.korea.label = '韩国'
Nationality.other.label = '其他'


class Video(models.Model):
    video_name = models.CharField(max_length=200, null=False)
    image = models.CharField(max_length=500, default='')
    video_type = models.CharField(max_length=50, default=VideoType.other)
    origin = models.CharField(max_length=20, default=Origin.custom)
    nationality = models.CharField(max_length=20, default=Nationality.other)
    status = models.BooleanField(default=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("video_name", "video_type", "origin")

    def __str__(self):
        return 'video_name:{},video_type:{},orgin:{},status{}'.format(self.video_name, self.video_type, self.origin,
                                                                      self.status)


class StartIdentify(Enum):
    actor = 'ACTOR'
    director = 'DIRECTOR'
    actress = 'ACTRESS'


StartIdentify.actor.label = '男演员'
StartIdentify.actress.label = '女演员'
StartIdentify.director.label = "导演"


class VideoStar(models.Model):
    video = models.ForeignKey(Video, related_name="video_star", on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=200)
    identify = models.CharField(max_length=200)
    info = models.TextField()

    class Meta:
        unique_together = ("video", "name", "identify")

    def __str__(self):
        return "video:{},name:{},identify:()".format(self.video.id, self.name, self.identify)


class VideoSub(models.Model):
    video = models.ForeignKey(Video, related_name="video_sub", on_delete=models.SET_NULL, null=True, blank=True)
    number = models.IntegerField(default=1)
    url = models.CharField(max_length=500, null=False)

    class Meta:
        unique_together = ("video", "number")

    def __str__(self):
        return "video:{},number:{}".format(self.video.id, self.number)
