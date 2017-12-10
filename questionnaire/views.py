from django.shortcuts import render, redirect, HttpResponse
import json
from . import models
from django.forms import ModelForm
from django.forms import widgets as wb


# Create your views here.
# 创建编辑问题页面的问题
class Question(ModelForm):
    class Meta:
        model = models.Question
        fields = ["name", "type"]
        widgets = {  # 格式
            'name': wb.Textarea(attrs={"cols": 50, "rows": 2})
        }


class Option(ModelForm):
    class Meta:
        model = models.Option
        fields = ["name", "score"]


def index(request):
    survey_list = models.Questionnaire.objects.all()
    return render(request, 'index.html', {'survey_list': survey_list})


def add(request):
    if request.method == 'POST':
        surveyName = request.POST.get("surveyName")
        cls_id = request.POST.get('cls')
        user_id = request.POST.get('user')
        models.Questionnaire.objects.create(name=surveyName, que2cls_id=cls_id, que2user_id=user_id)
        return redirect('/index/')
    cls_list = models.Class.objects.all()
    user_list = models.UserInfo.objects.all()
    return render(request, 'add.html', {'class_list': cls_list, 'user_list': user_list})


def dele(request):
    surveyInfoId = request.GET.get("survey_id")
    models.Questionnaire.objects.filter(id=surveyInfoId).delete()
    return HttpResponse(1)


def edit(request, nid):
    # 方法一: 直接循环
    # 获取当前问卷中的所有问题
    # que_list = models.Question.objects.filter(que2quen_id=nid)
    # form_list = []
    # if not que_list:
    #     #新问卷
    #     form =Question()
    #     form_list.append(form)
    # else:
    #     #已经添加过问题的
    #     for que in que_list:
    #         form = Question(instance=que)   # 原来的数据库的问题
    #         form_list.append(form)
    # return render(request, "edit.html", {'form_list': form_list})
    # 方法二：通过yield
    # def inner():
    #     que_list = models.Question.objects.filter(que2quen_id=nid)
    #     if not que_list:
    #         form = Question()
    #         # yield form
    #         yield {'form': form, 'obj': None, 'option_class': 'hide', 'options': None}  # 默认情况下 单选是空
    #     else:
    #         for que in que_list:
    #             form = Question(instance=que)
    #             # yield form
    #             temp = {'form': form, 'obj': que, 'option_class': 'hide', 'options': None}  # 添加obj可以在前端拿到问题id
    #             if que.type == 2:  # 如果是单选
    #                 temp['option_class'] = None
    #                 # 获取当前单选的所有选项
    #                 choices = []
    #                 option_list = models.Option.objects.filter(opt2que=que)  #外间=对象
    #                 for i in option_list:
    #                     choice_list =Option(instance=i)
    #                     choices.append(choice_list)
    #                 temp['options'] = choices
    #             yield temp
    #
    # return render(request, 'edit.html', {'form_list': inner()})
    # 方法三：
    def inner():
        que_list = models.Question.objects.filter(que2quen_id=nid)
        if not que_list:
            form = Question()
            yield {'form': form, 'obj': None, 'option_class': 'hide', 'options': None}
        else:
            for que in que_list:
                form = Question(instance=que)
                temp = {'form': form, 'obj': que, 'option_class': 'hide', 'options': None}
                if que.type == 2:
                    temp['option_class'] = ''

                    def inner_loop(quee):
                        option_list = models.Option.objects.filter(opt2que=quee)
                        for v in option_list:
                            yield {"form": Option(instance=v), 'obj': v}

                    temp['options'] = inner_loop(que)
                yield temp
    return render(request, 'edit.html', {'form_list': inner()})


# def data(request, nid):
#     ret = {'status': True, 'msg': None, 'data': None}
#     try:
#         ajax_question_list = json.loads(request.body.decode("utf-8"))  # ajax获取前端传来的值
#         question_id = models.Question.objects.filter(que2quen_id=nid)  # 数据库中的
#         post_id_list = [i.get('id') for i in ajax_question_list if i.get('id')]
#         db_id_list = [i.id for i in question_id]
#
#         # 哪些id需要删除
#         del_id_list = set(db_id_list).difference(post_id_list)
#
#         # 取出前端发来的问题信息
#         for item in ajax_question_list:
#             have_id = item.get('id')
#             if not have_id in db_id_list:  # 判断更新还是增加
#                 # 增加
#                 temp = {
#                     'name': item.get('name'),
#                     'type': item.get('type')
#                 }
#                 new_question_list = models.Question.objects.create(**temp)
#                 if item.get('type') == 2:
#                     for op in item.get('options'):
#                         new_option_list = models.Option.objects.creat(opt2que=new_question_list, name=op.get('name'),
#                                                                       score=op.get('score'))
#             else:
#                 # 更新
#                 models.Question.objects.filter(id=nid).update(name=item.get('name'), type=item.get('type'))
#
#                 if not item.get('options'):  # 判断有没有option
#                     models.Option.objects.filter(opt2que=nid).delete()  # 没有则删除
#                 else:
#                     models.Option.objects.filter(opt2que=nid).delete()  # 不推荐，需要再次判断，哪些该删除，哪些该增加，取交集同上方法
#                     for op in item.get('options'):
#                         models.Option.objects.create(opt2que=nid, name=op.get('name'), score=op.get('score'))
#
#         # 删除的
#         models.Question.objects.first(id__in=del_id_list).delete()
#     except Exception as e:
#         ret['msg'] = 'aaa'
#         ret['status'] = False
#     return HttpResponse(json.dumps(True))
