# coding:utf-8

from django import template
from app.models.video import VideoType, Origin, Nationality

register = template.Library()


@register.filter(name='origin_video')
def origin_video(v):
    for i in Origin:
        if i.value == v:
            return i.label


@register.filter(name='type_video')
def type_video(v):
    for i in VideoType:
        if i.value == v:
            return i.label


@register.filter(name='nationality_video')
def nationality_video(v):
    for i in Nationality:
        if i.value == v:
            return i.label
