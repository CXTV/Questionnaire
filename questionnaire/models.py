from django.db import models


# Create your models here.
class UserInfo(models.Model):
    """"用户"""
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "用户表"


class Student(models.Model):
    """学生"""
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    stu2cls = models.ForeignKey(to="Class")

    class Meta:
        verbose_name_plural = "学生表"

    def __str__(self):
        return self.name


class Class(models.Model):
    """班级"""
    name = models.CharField(max_length=32)
    num = models.IntegerField()
    cls2user = models.ForeignKey(to="UserInfo")

    class Meta:
        verbose_name_plural = "班级表"

    def __str__(self):
        return self.name


class Questionnaire(models.Model):
    """问卷表"""
    name = models.CharField(max_length=64)
    que2user= models.ForeignKey(to="UserInfo")
    que2cls = models.ForeignKey(to="Class")

    class Meta:
        verbose_name_plural = "问卷表"

    def __str__(self):
        return self.name


class Question(models.Model):
    """问题表"""
    name = models.CharField(max_length=64)
    question_type = (
        (1, "打分(1~10分)"),
        (2, "单选"),
        (3, "评价"),
    )
    type = models.IntegerField(choices=question_type)
    que2quen = models.ForeignKey(to="Questionnaire")

    class Meta:
        verbose_name_plural = "问题表"

    def __str__(self):
        return self.name


class Option(models.Model):
    """单选题"""
    name = models.CharField(max_length=32)
    score = models.IntegerField()
    opt2que = models.ForeignKey(to="Question")

    class Meta:
        verbose_name_plural = "单选题"

    def __str__(self):
        return self.name


class Answer(models.Model):
    """答案"""
    ans2stu = models.ForeignKey(to="Student")
    ans2que = models.ForeignKey(to="Question", verbose_name='关联的第几题')
    ans2opt = models.ForeignKey(to="Option")
    val = models.IntegerField(null=True, blank=True)
    content = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = "答案"
