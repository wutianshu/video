# coding: utf-8

from django.db import models
import hashlib,datetime


def make_pwd(password):
    if isinstance(password, str):
        password = password.encode('utf-8')
    return hashlib.md5(password).hexdigest().upper()


class ClientUser(models.Model):
    username = models.CharField(max_length=50, null=False, unique=True)
    password = models.CharField(max_length=200, null=False)
    avatar = models.CharField(max_length=500, null=True, blank=True)  # 头像
    gender = models.CharField(max_length=10, null=True, blank=True,)  # 性别
    birthday = models.DateField(null=True,default=datetime.date(1770,1,1))
    status = models.BooleanField(default=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'username:{}'.format(self.username)

    @classmethod
    def add(cls, username, password, avatar='', gender='', birthday=datetime.date(1770,1,1), status=True):
        return cls.objects.create(username=username,
                                  password=make_pwd(password),
                                  avatar=avatar,
                                  gender=gender,
                                  birthday=birthday,
                                  status=status)

    @classmethod
    def get_user(cls, username, password):
        try:
            user = cls.objects.get(username=username,
                                   password=make_pwd(password))
            return user
        except:
            return None


    def update_password(self,new_pwd, old_pwd):
        old_pwd = make_pwd(old_pwd)
        if old_pwd == self.password: # 旧密码验证通过
            if not make_pwd(new_pwd) == self.password: # 新密码和旧密码不一样
                self.password = make_pwd(new_pwd)
                self.save()
                return True
            else:
                return False
        else:
            return False

    def update_status(self):
        self.status = not self.status
        self.save()
        return True