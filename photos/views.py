from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse

# by Group5 - Sumi(21700520@handong.edu) for adding 'Answer' 
from .models import Data, Announcement, Profile, Verification, Year, UserInfo, StudentInfo, Group, Current, Answer
from .forms import DataForm, AnnouncementForm#, ProfileForm

from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import transaction

from django.db.models import Count, Max, Sum, Subquery, OuterRef, F, Min, Value, DateTimeField, CharField
from django.db.models.expressions import RawSQL

#For Code Verification
from datetime import datetime, timedelta
from django.utils import timezone
import json, random

#CSV import
from tablib import Dataset
import pandas
import magic, copy, csv

# for Infinite Scroll
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# for device detection
from django_user_agents.utils import get_user_agent

from operator import attrgetter, itemgetter # toplist

LOGIN_REDIRECT_URL = '/user_check/'


def current_year():
    return datetime.date.today().year

def current_sem():
    if datetime.date.today().month < 8 and datetime.date.today().month > 1:
        return 1
    else:
        return 2

@staff_member_required
def set_current(request):
    ctx = {}

    currents = Current.objects.all()
    if request.method == 'POST':
        year = request.POST['year']
        if request.POST['semester'] == 'spring':
            semester = 1
        elif request.POST['semester'] == 'fall':
            semester = 2

        if int(year) < 2000:
            pass # 에러 처리
        else:
            try:
                yearobj = Year.objects.get(year=year)
            except:
                yearobj = Year.objects.create(year=year)

        if currents.exists():
            current = currents[0]
            current.year = yearobj
            current.sem = semester
            print(semester)
            print(current.year, current.sem)
            current.save()
        else:
            Current.objects.create(year=yearobj, sem=semester)

    ctx['current'] = Current.objects.all()[0]
    ctx['username'] = request.user.username

    return render(request, 'set_current.html', ctx)

@staff_member_required
def reset_profile_group(request):
    ctx = {}

    if request.method == 'POST':
        year = request.POST['year']
        if request.POST['semester'] == '1':
            semester = 1
        elif request.POST['semester'] == '2':
            semester = 2

        if int(year) < 2000:
            pass # 에러 처리
        else:
            try:
                yearobj = Year.objects.get(year=year)
            except:
                yearobj = Year.objects.create(year=year)

        userinfo_list = UserInfo.objects.filter(year=yearobj, sem=semester)
        for userinfo in userinfo_list:
            try:
                profile = Profile.objects.get(student_info=userinfo.student_info)
                if profile.group != userinfo.group:
                    profile.group = userinfo.group
                    profile.save()
            except:
                pass
            

    return render(request, 'reset_profile_group.html')

@login_required(login_url=LOGIN_REDIRECT_URL)
def detail(request, pk):
    data = get_object_or_404(Data, pk=pk)
    current = Current.objects.all()[0]
    ctx={}
    if request.user.is_authenticated:
        username = request.user.username
        ctx['userobj'] = request.user
    else:
        return redirect('loginpage')

    if not (request.user.is_staff or (data.group == request.user.profile.group and data.year == current.year and data.sem == current.sem)):
        messages.warning(request, 'invalid access', extra_tags='alert')
        return HttpResponseRedirect(reverse('main'))

    participators = data.participator.all()
    print("detail participators: ", participators)

    ctx = {
        'post': data,
        'username': username,
        'participators': participators,
    }

    now_time = timezone.localtime()
    time_diff = now_time - data.date

    if time_diff.seconds / 3600 < 1 :
        ctx['can_edit'] = True
    else:
        ctx['can_edit'] = False

    return render(request, 'detail.html', ctx)

# For Random Code Generator
all_pins = [format(i, '04') for i in range(1000, 10000)]
possible = [i for i in all_pins if len(set(i)) > 3]

@login_required(login_url=LOGIN_REDIRECT_URL)
def data_upload(request):
    ctx={}

    try:
        user = User.objects.get(pk=request.user.pk)
        ctx['userobj'] = user
        if user.is_staff is True:
            return redirect('userList')
    except User.DoesNotExist:
        return redirect(reverse('loginpage'))

    is_mobile = request.user_agent.is_mobile
    is_tablet = request.user_agent.is_tablet

    now_time = timezone.localtime()

    verification = user.profile.group.verification

    if verification.code_when_saved is None:
        verification.code_when_saved = now_time
        verify_code = random.choice(possible)
        verification.code = verify_code
        verification.save()

    time_diff = now_time - verification.code_when_saved

    if (60*10 - time_diff.seconds) > 0:
        ctx['code_time'] = time_diff.seconds
    else:
        ctx['code_time'] = 0

    if request.method.get == "GET":
        if is_mobile or is_tablet:
            form = DataForm(user=request.user, is_mobile=True)
            form.set_is_mobile()
        else:
            form = DataForm(user=request.user, is_mobile=False)
            form.set_is_mobile()
    elif request.method == "POST":
        form = DataForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            obj = form.save()
            obj.author = user
            # latestid = Data.objects.filter(author=user).order_by('-id')
            # if latestid:
            #     obj.idgroup = latestid[0].idgroup + 1
            # else:
            #     obj.idgroup = 1

            if verification.code is not None:
                if (time_diff.seconds)/60 < 10:
                    obj.code = verification.code
                    obj.code_when_saved = verification.code_when_saved
                    verification.code = None
                    verification.code_when_saved = None
                else:
                    verification.code = None
                    verification.code_when_saved = None
                    messages.warning(request, '코드가 생성된지 10분이 지났습니다.', extra_tags='alert')

            # num = user.userinfo.num_posts
            # user.userinfo.num_posts = num + 1
            # user.userinfo.most_recent = obj.date
            # user.userinfo.name = username
            verification.save()

            current = Current.objects.all()
            if current.exists():
                yearobj = current[0].year
                semester = current[0].sem
            else:
                year = current_year()
                try:
                    yearobj = Year.objects.get(year=year)
                except:
                    yearobj = Year.objects.create(year=year)
                semester = current_sem()

            obj.group = user.profile.group
            obj.year = yearobj
            obj.sem = semester

            obj.save()
            messages.success(request, '게시물을 등록하였습니다.', extra_tags='alert')
            return HttpResponseRedirect(reverse('main'))
        else:
            messages.warning(request, '모든 내용이 정확하게 입력되었는지 확인해주세요.', extra_tags='alert')

    ctx['form'] = form
    ctx['userobj'] = user

    return render(request, 'upload.html', ctx)


def data_edit(request, pk):
    ctx={}

    if request.user.is_authenticated:
        username = request.user.username
        ctx['username'] = request.user.username
    else:
        return redirect('loginpage')

    if username:
        user = User.objects.get(username=username)
        ctx['userobj'] = user
        if user.is_staff is True:
            return redirect('userList')
    else:
        return redirect('loginpage')

    is_mobile = request.user_agent.is_mobile
    is_tablet = request.user_agent.is_tablet


    # if (60*10 - time_diff.seconds) > 0:
    #     ctx['code_time'] = time_diff.seconds
    # else:
    #     ctx['code_time'] = 0

    # find the target post
    post = Data.objects.get(id=pk)
    if post.group != user.profile.group:
        messages.warning(request, '해당 게시물의 그룹이 아닙니다', extra_tags='alert')
        return HttpResponseRedirect(reverse('main'))

    if request.method == "GET":
        if is_mobile or is_tablet:
            form = DataForm(user=request.user, is_mobile=True, instance=post)
            form.set_is_mobile()
        else:
            form = DataForm(user=request.user, is_mobile=False, instance=post)
            form.set_is_mobile()
    elif request.method == "POST":
        form = DataForm(request.POST, request.FILES, user=request.user, instance=post)
        if form.is_valid():
            # print(form.cleaned_data)
            post.title = form.cleaned_data['title']
            post.text = form.cleaned_data['text']
            post.participator.set(form.cleaned_data['participator'])
            post.study_start_time = form.cleaned_data['study_start_time']
            post.study_total_duration = form.cleaned_data['study_total_duration']

            post.save()

            messages.success(request, '게시물을 등록하였습니다.', extra_tags='alert')
            return redirect('detail', pk)
        else:
            messages.warning(request, '모든 내용이 정확하게 입력되었는지 확인해주세요.', extra_tags='alert')

    ctx['form'] = form
    ctx['userobj'] = user

    return render(request, 'edit.html', ctx)


def warn_overwrite(request, year_pk, sem):
    ctx={}
    yearobj = Year.objects.get(pk=year_pk)
    userinfo_list = UserInfo.objects.filter(year=yearobj, sem=sem)
    ctx['userinfo_list'] = userinfo_list

    if request.method == 'POST':
        imported_data_string = request.session.get('imported_data_string', None)
        imported_data_json = json.loads(imported_data_string)
        imported_data_list = []

        for data in imported_data_json.items():
            value_list = list(data[1].values())
            imported_data_list.append(copy.deepcopy(value_list))

        # but first remove existing userinfo
        userinfo_list.delete()

        num_of_ppl = len(data[1])
        for i in range(num_of_ppl):
            groupNo = imported_data_list[0][i]
            stuID = imported_data_list[1][i]
            name = imported_data_list[3][i]

            try:
                groupobj = Group.objects.get(no=groupNo)
            except:
                groupobj = Group.objects.create(no=groupNo)
                try:
                    verifyobj = Verification.objects.create(group=groupobj)
                except Verification.DoesNotExist:
                    messages.warning(request, 'Group에 대한 Verification을 생성할 수 없습니다.', extra_tags='alert')

            try:
                student_info_obj = StudentInfo.objects.get(student_id=stuID)
            except:
                student_info_obj = StudentInfo.objects.create(student_id=stuID, name=name)

            UserInfo.objects.create(year=yearobj, sem=sem, group=groupobj, student_info=student_info_obj)

        messages.success(request, 'csv 정보를 성공적으로 덮어씌웠습니다. ', extra_tags='alert')

        return redirect(reverse('csv_upload'))

    else:
        return render(request, 'warn_overwrite.html', ctx)




@csrf_exempt
@staff_member_required
def csv_upload(request):
    ctx = {}

    if request.user.is_authenticated:
        username = request.user.username
        user = User.objects.get(username=username)
        ctx['userobj'] = user
        if user.is_staff is False:
            return redirect('main')
    else:
        return redirect('loginpage')

    if request.method == 'POST':
        dataset = Dataset()
        data = request.FILES
        new_usergroup = data['myfile']

        csv_file = copy.deepcopy(new_usergroup)

        blob = csv_file.read()
        m = magic.Magic(mime_encoding=True)
        encoding = m.from_buffer(blob)

        if encoding == "iso-8859-1":
            encoding = "euc-kr"

        imported_data = dataset.load(new_usergroup.read().decode(encoding), format='csv')


        if imported_data is None:
            messages.warning(request, 'CSV파일의 Encoding이 UTF-8이거나 EUC-KR형식으로 변형해주세요.', extra_tags='alert')
            redirect('csv_upload')

        group_no = "1"
        group_list = []

        year = request.POST['year']
        if request.POST['semester'] == 'spring':
            semester = 1
        elif request.POST['semester'] == 'fall':
            semester = 2

        if int(year) < 2000:
            messages.warning(request, '년도가 2000보다 작습니다', extra_tags='alert')
            return render(request, 'csv_upload.html', ctx)
        else:
            try:
                yearobj = Year.objects.get(year=year)
            except:
                yearobj = Year.objects.create(year=year)


        userinfo_list = UserInfo.objects.filter(year=yearobj, sem=semester)
        if userinfo_list:
            df = pandas.DataFrame(data=list(imported_data))
            request.session['imported_data_string'] = df.to_json()
            return redirect(reverse('warn_overwrite', args=(yearobj.pk, semester)))


        for data in imported_data:
            print("data", data)
            try:
                groupobj = Group.objects.get(no=data[0])
            except:
                groupobj = Group.objects.create(no=data[0])
                verifyobj = Verification.objects.filter(group=groupobj)
                if not verifyobj.exists():
                    try:
                        verifyobj = Verification.objects.create(group=groupobj)
                    except Verification.DoesNotExist:
                        messages.warning(request, 'Group에 대한 Verification을 생성할 수 없습니다.', extra_tags='alert')

            try:
                student_info_obj = StudentInfo.objects.get(student_id=data[1])
            except:
                student_info_obj = StudentInfo.objects.create(student_id=data[1], name=data[3])
            UserInfo.objects.create(year=yearobj, sem=semester, group=groupobj, student_info=student_info_obj)

        messages.success(request, 'csv 정보를 저장했습니다. ', extra_tags='alert')

    if username:
        ctx['username'] = username

    return render(request, 'csv_upload.html', ctx)

@csrf_exempt
@staff_member_required
def new_userinfo(request):
    ctx = {}

    if request.method == 'POST':
        year = request.POST['year']
        sem = request.POST['semester']
        student_id = request.POST['student_id']
        name = request.POST['name']
        groupno = int(request.POST['group'])
        try:
            yearobj = Year.objects.get(year=year)
        except:
            yearobj = Year.objects.create(year=year)
        try:
            student_info_obj = StudentInfo.objects.get(student_id=student_id)
        except:
            student_info_obj = StudentInfo.objects.create(student_id=student_id, name=name)

        try:
            user_info = UserInfo.objects.get(year=yearobj, sem=sem, student_info=student_info_obj)
        except:
            user_info = None

        if user_info:
            prev_group = user_info.group.no
            if prev_group != groupno:
                try:
                    groupobj = Group.objects.get(no=groupno)
                except:
                    groupobj = None

                if groupobj:
                    user_info.group = groupobj
                    user_info.save()
                    msg = str(year) + '년 ' + str(sem) + '학기 해당 학생의 그룹 정보가 변경되었습니다: Group ' + str(prev_group) + ' --> Group ' + str(user_info.group.no)
                    messages.success(request, msg)
                else:
                    messages.warning(request, "해당 그룹이 존재하지 않습니다.")

        else:
            try:
                groupobj = Group.objects.get(no=groupno)
            except:
                groupobj = Group.objects.create(no=groupno)
            UserInfo.objects.create(year=yearobj, sem=sem, group=groupobj, student_info=student_info_obj)

            current = Current.objects.all().first()
            print(current.year.year, sem)
            if yearobj == current.year and int(sem) == current.sem:
                try:
                    user_profile = Profile.objects.get(student_info=student_info_obj)
                    user_profile.group = groupobj
                    user_profile.save()
                except:
                    pass
            else:
                print("else", yearobj, (yearobj == current.year), (sem == current.sem), (yearobj == current.year and sem == current.sem))

            messages.info(request, '해당 정보가 성공적으로 생성되었습니다.')
    else:
        pass

    return render(request, 'new_userinfo.html', ctx)


@staff_member_required
def delete_userinfo(request):
    ctx = {}
    if request.user.is_authenticated:
        username = request.user.username
        user = User.objects.get(username=username)
        ctx['userobj'] = user
        if user.is_staff is False:
            return redirect('main')
    else:
        return redirect('loginpage')

    if username:
        ctx['username'] = username

    current = Current.objects.all().first()
    ctx['years'] = Year.objects.all()

    groups = Group.objects.all()
    ctx['groups'] = groups

    if request.method == 'POST':
        year = request.POST['year']
        sem = request.POST['sem']
        group = request.POST['group']

        print(">>> POST")
        print(year)
        print(sem)
        print(group)

        yearobj = Year.objects.get(year=year)
        sem = sem

        if year != 'None' and sem != 'None' and group != 'None':
            ctx['chosen_year'] = year
            ctx['chosen_sem'] = sem
            ctx['chosen_group'] = group
            return redirect(reverse('delete_userinfo_confirm', args=(year, sem, group)))

    else:
        yearobj = current.year
        year = current.year.year
        sem = current.sem
        group = groups.first().no

        ctx['year'] = year
        ctx['sem'] = sem
        ctx['group'] = group

    return render(request, 'delete_userinfo.html', ctx)

@staff_member_required
def delete_userinfo_confirm(request, year, sem, group_no):
    ctx={}
    yearobj = Year.objects.get(year=year)
    groupobj = Group.objects.get(no=group_no)
    userinfo_list = UserInfo.objects.filter(year=yearobj, sem=sem, group=groupobj)
    ctx['userinfo_list'] = userinfo_list
    ctx['group_no'] = group_no

    if request.method == 'POST':
        userinfo_pk = request.POST['userinfo_pk']
        userinfo = UserInfo.objects.get(pk=userinfo_pk).delete()
        messages.success(request, '유저를 성공적으로 삭제했습니다. ', extra_tags='alert')
        return redirect(reverse('delete_userinfo'))

    return render(request, 'delete_userinfo_confirm.html', ctx)




@csrf_exempt
def export_page(request):
    ctx={}
    if request.user.is_authenticated:
        username = request.user.username
        ctx['username'] = request.user.username
    else:
        return redirect('loginpage')

    if username:
        user = User.objects.get(username=username)
        ctx['userobj'] = user
    else:
        return redirect('loginpage')

    if request.method == 'POST':
        criterion = int(request.POST['criterion'])
        year = request.POST['year']
        sem = request.POST['semester']

        try:
            yearobj = Year.objects.get(year=year)
        except Year.DoesNotExist:
            yearobj = None

        pass_stu_list = UserInfo.objects.filter(year=yearobj, sem=sem).values("group").distinct().annotate(
            total_posts = Count('group__data', distinct=True, filter=Q(group__data__year=yearobj)&Q(group__data__sem=sem)),
            no = F('group__no'),
            group_id = F('group'),
            student_id = F('group__userinfo__student_info__student_id'),
            name = F('group__userinfo__student_info__name'),
            # total_posts = Count('group__data', distinct=True, filter=Q(group__data__year=yearobj)&Q(group__data__sem=sem)),
            # no = F('group__no'),
            # student_id = F('group__userinfo__student_info__student_id'),
            # name = F('group__userinfo__student_info__name'),
            total_participation = Count('group__data', distinct=True, filter=Q(group__data__year=yearobj)&Q(group__data__sem=sem)&Q(group__data__participator__student_info__student_id=F('group__userinfo__student_info__student_id'))),
        ).order_by('no', 'student_id').filter(total_participation__gte=criterion)


        response = HttpResponse(content_type = 'text/csv')
        response['Content-Disposition'] = 'attachment; filename="histudy_pass_student.csv"'

        writer = csv.writer(response, delimiter=',')
        writer.writerow(['이름', '학번', '그룹번호', '그룹 총 스터디 횟수', '개인별 총 스터디 횟수', '개인별 스터디 참여시간(분)'])

        for stu in pass_stu_list:
            study = Data.objects.filter(year=yearobj, sem=sem, group_id=stu['group_id'], participator__student_info__student_id=stu['student_id']).distinct().aggregate(
                total_time = Sum('study_total_duration'), 
                total_participation = Count('id')
            )
            stu['total_time'] = study['total_time']
            stu['total_participation'] = study['total_participation']
            writer.writerow([stu['name'], stu['student_id'], stu['no'], stu['total_posts'], stu['total_participation'], stu['total_time']])

        # for stu in pass_stu_list:
        #     percent = float(stu['total_participation']) / float(stu['total_posts']) * 100
        #     percent = round(percent, 2)
        #     writer.writerow([stu['no'], stu['student_id'], stu['name'], percent])
        return response
    else:
        return render(request, 'export_page.html', ctx)

    return render(request, 'export_page.html', ctx)

@csrf_exempt
def export_all_page(request):
    ctx={}
    if request.user.is_authenticated:
        username = request.user.username
        ctx['username'] = request.user.username
    else:
        return redirect('loginpage')

    if username:
        user = User.objects.get(username=username)
        ctx['userobj'] = user
    else:
        return redirect('loginpage')

    if request.method == 'POST':
        year = request.POST['year']
        sem = request.POST['semester']

        try:
            yearobj = Year.objects.get(year=year)
        except Year.DoesNotExist:
            yearobj = None

        pass_stu_list = UserInfo.objects.filter(year=yearobj, sem=sem).values("group").distinct().annotate(
            total_posts = Count('group__data', distinct=True, filter=Q(group__data__year=yearobj)&Q(group__data__sem=sem)),
            no = F('group__no'),
            group_id = F('group'),
            student_id = F('group__userinfo__student_info__student_id'),
            name = F('group__userinfo__student_info__name'),
            # total_participation = Count('group__data', distinct=True, filter=Q(group__data__year=yearobj)&Q(group__data__sem=sem)&Q(group__data__participator__student_info__student_id=F('group__userinfo__student_info__student_id'))),
            # total_time = Count('group__data__study_total_duration', filter=Q(group__data__year=yearobj)&Q(group__data__sem=sem)&Q(group__data__participator__student_info__student_id=F('group__userinfo__student_info__student_id'))),
            # total_time = Count('group__data__study_total_duration', distinct=True, filter=Q(group__data__year=yearobj, group__data__sem=sem, group__data__participator__student_info__student_id=F('group__userinfo__student_info__student_id'))),
        ).order_by('no', 'student_id').exclude(no=0)

        for stu in pass_stu_list:
            study = Data.objects.filter(year=yearobj, sem=sem, group_id=stu['group_id'], participator__student_info__student_id=stu['student_id']).distinct().aggregate(
                total_time = Sum('study_total_duration'), 
                total_participation = Count('id')
            )
            stu['total_time'] = study['total_time']
            stu['total_participation'] = study['total_participation']

        # print(pass_stu_list)
        # for stu in pass_stu_list:
        #     total_time = stu['total_time']
        #     if total_time:
        #         print(stu)


        response = HttpResponse(content_type = 'text/csv')
        response['Content-Disposition'] = 'attachment; filename="histudy_all_student.csv"'
        
        writer = csv.writer(response, delimiter=',')
        writer.writerow(['이름', '학번', '그룹번호', '그룹 총 스터디 횟수', '개인별 총 스터디 횟수', '개인별 스터디 참여시간(분)'])
        
        for stu in pass_stu_list:
            writer.writerow([stu['name'], stu['student_id'], stu['no'], stu['total_posts'], stu['total_participation'], stu['total_time']])
        
        
        return response
    else:
        return render(request, 'export_all_page.html', ctx)

    return render(request, 'export_all_page.html', ctx)


@staff_member_required
def photoList(request, group, year, sem):
    # group is group.pk

    yearobj = Year.objects.get(year=year)
    picList = Data.objects.raw('SELECT * FROM photos_data WHERE group_id = %s AND year_id = %s AND sem = %s ORDER BY id DESC', [group, yearobj.pk, sem])
    group_pk = group
    if request.user.is_authenticated:
        username = request.user.username
        user = User.objects.get(username=username)
        if user.is_staff is False:
            return redirect('loginpage')
    else:
        return redirect('loginpage')

    groupno = Group.objects.get(pk=group)

    ctx = {
        'list' : picList,
        'user' : user,
        'year' : year,
        'sem' : sem,
        'group' : groupno.no,
        'group_pk' : group_pk,
    }

    if username:
        ctx['username'] = username

    return render(request, 'list.html', ctx)

import datetime
from django.db.models import Q
@staff_member_required
def userList(request):
    ctx={}
    if request.user.is_authenticated:
        username = request.user.username
        user = request.user
        if user.is_staff is False:
            return redirect('main')
    else:
        return redirect('loginpage')

    ctx['years'] = Year.objects.all()


    if request.method == 'POST':
        year = request.POST['year']
        sem = request.POST['sem']

        yearobj = Year.objects.get(year=year)
        sem = int(sem)

        ctx['year'] = year
        ctx['sem'] = sem

        if year != 'None' and sem != 'None':
            ctx['chosen_year'] = year
            ctx['chosen_sem'] = sem

    else:
        current = Current.objects.all().first()
        yearobj = current.year
        sem = current.sem
        ctx['year'] = yearobj.year
        ctx['sem'] = sem

    grouplist = UserInfo.objects.filter(year=yearobj, sem=sem).values("group").distinct().annotate(
        num_posts = Count('group__data', distinct=True, filter=Q(group__data__year=yearobj)&Q(group__data__sem=sem)),
        recent = Max('group__data__date', filter=Q(group__data__year=yearobj)&Q(group__data__sem=sem)), # 해당 학기로 바꿔야함 to fix
        #total_dur = Sum('group__data__study_total_duration', filter=Q(group__data__year=yearobj)&Q(group__data__sem=sem)),
        no = F('group__no'),
    ).order_by('-num_posts', 'recent', 'no').exclude(group__no=0)

    groupno = UserInfo.objects.filter(year=yearobj, sem=sem).values('group').distinct()
    total_duration = {}
    for group in groupno:
        gno = Group.objects.get(pk=group['group'])
        data = Data.objects.filter(year=yearobj, sem=sem, group=group['group']).aggregate(Sum('study_total_duration'))
        total_duration[group[str('group')]] = data['study_total_duration__sum']
    
    for group in grouplist:
        group['total_dur'] = total_duration[group['group']]
    
    ctx['grouplist'] = grouplist

    '''
    userlist = User.objects.filter(Q(is_staff=False) & Q(userinfo__year__year=year) & Q(userinfo__sem=sem)).annotate(
        num_posts = Count('data'),
        recent = Max('data__date'),
        total_dur = Sum('data__study_total_duration'),
    ).exclude(username='test').order_by('-num_posts', 'recent', 'id')


    ctx['list'] = userlist
    ctx['userobj'] = user
    if username:
        ctx['username'] = username
    '''

    return render(request, 'userlist.html', ctx)

def guideline(request):
    return render(request, 'histudy_guideline.html', {})

def rank(request):
    ctx = {}
    if request.user.is_authenticated:
        username = request.user.username
        user = User.objects.get(username=username)
        ctx['user'] = user
        ctx['username'] = username

    try:
        current = Current.objects.all().first()
        yearobj = current.year
        sem = current.sem
    except:
        year = current_year()
        sem = current_sem()
        try:
            yearobj = Year.objects.get(year=year)
        except Year.DoesNotExist:
            yearobj = None

    grouplist = UserInfo.objects.filter(year=yearobj, sem=sem).values('group').distinct().annotate(
        num_posts = Count('group__data', distinct=True, filter=Q(group__data__year=yearobj)&Q(group__data__sem=sem)),
        recent = Max('group__data__date', filter=Q(group__data__year=yearobj)&Q(group__data__sem=sem)), # 해당 학기로 바꿔야함 to fix
        total_dur = Sum('group__data__study_total_duration', distinct=True, filter=Q(group__data__year=yearobj)&Q(group__data__sem=sem)),
        no = F('group__no'),
    ).order_by('-num_posts', 'recent', 'no').exclude(group__no=0)

    # copied by JC to fix a bug in rank (2021-03-17)
    groupno = UserInfo.objects.filter(year=yearobj, sem=sem).values('group').distinct()
    total_duration = {}
    for group in groupno:
        gno = Group.objects.get(pk=group['group'])
        data = Data.objects.filter(year=yearobj, sem=sem, group=group['group']).aggregate(Sum('study_total_duration'))
        total_duration[group[str('group')]] = data['study_total_duration__sum']

    for group in grouplist:
        group['total_dur'] = total_duration[group['group']]

    # by JC

    # userlist = User.objects.filter(Q(is_staff=False) & Q(userinfo__year__year=year) & Q(userinfo__sem=sem)).annotate(
    #     num_posts = Count('data'),
    #     recent = Max('data__date'),
    #     total_dur = Sum('data__study_total_duration'),
    # ).exclude(username='test').order_by('-num_posts', 'recent', 'id')

    ctx['list'] = grouplist

    return render(request, 'rank.html', ctx)



def top3(request):
    ctx={}

    if request.user.is_authenticated:
        username = request.user.username
        user = User.objects.get(username=username)
        if user.is_staff is False:
            return redirect('main')
    else:
        return redirect('loginpage')

    current = Current.objects.all().first()
    ctx['years'] = Year.objects.all()

    if request.method == 'POST':
        year = request.POST['year']
        sem = request.POST['sem']
        ctx['year'] = year
        ctx['sem'] = sem

        yearobj = Year.objects.get(year=year)

        if year != 'None' and sem != 'None':
            ctx['chosen_year'] = year
            ctx['chosen_sem'] = sem

    else:
        year = current_year()
        sem = current_sem()
        yearobj = current.year
        sem = current.sem
        ctx['year'] = year
        ctx['sem'] = sem

    groupno = UserInfo.objects.filter(year=yearobj, sem=sem).values('group').distinct()
    tenth_date = {}
    for group in groupno:
        gno = Group.objects.get(pk=group['group'])
        if gno.no == 0:
            continue
        data = Data.objects.filter(year=yearobj, sem=sem, group=group['group'])
        if data.exists():
            if data.count() >= 10: #real
            #if data.count() >= 0: #debug
                tenth_date[group[str('group')]] = data[9].date #real
                #tenth_date[group[str('group')]] = datetime.datetime.now() #debug

    toplist = UserInfo.objects.filter(year=yearobj, sem=sem).values("group").distinct().annotate(
        num_posts = Count('group__data', distinct=True, filter=Q(group__data__year=yearobj)&Q(group__data__sem=sem)),
        no = F('group__no'),
    ).exclude(group__no=0).filter(num_posts__gte=10) #real
    #).exclude(group__no=0).filter(num_posts__gte=1) #debug

    for top in toplist:
        if top['group'] in tenth_date.keys():
            top['date'] = tenth_date[top['group']]

    finallist = sorted(toplist, key=itemgetter('date'), reverse=False)
    #toplist = toplist.order_by('date')
    #toplist = sorted(toplist, key=attrgetter('date'))

    #to fix - order by date
    '''
    toplist = User.objects.raw('SELECT id, username, num_posts, date FROM \
                                (SELECT auth_user.id, username, year, sem, \
	                            (SELECT count(*) FROM photos_data WHERE auth_user.username = photos_data.author) AS num_posts, \
	                            (SELECT date FROM photos_data WHERE auth_user.username = photos_data.author AND photos_data.idgroup = 10) AS date \
                                FROM auth_user INNER JOIN photos_userinfo ON auth_user.id = photos_userinfo.user_id INNER JOIN photos_year ON photos_userinfo.year_id = photos_year.id) AS D \
                                WHERE num_posts>9 AND username <> "test" AND year=%s AND sem=%s ORDER BY date LIMIT 3', [year, sem])
    '''

    ctx['list'] = finallist
    ctx['userobj'] = user
    if username:
        ctx['username'] = username

    return render(request, 'top3.html', ctx)


def announce(request):
    ctx={}
    if request.user.is_authenticated:
        username = request.user.username
        user = User.objects.get(username=username)
        ctx['userobj'] = user
        ctx['username'] = username
    else:
        return redirect('loginpage')

    announceList = Announcement.objects.all()
    ctx['list'] = announceList

    return render(request, 'announce.html', ctx)

@login_required(login_url=LOGIN_REDIRECT_URL)
def main(request):
    ctx={}

    try:
        current = Current.objects.all().first()
        yearobj = current.year
        sem = current.sem
    except:
        try:
            year = current_year()
            sem = current_sem()
            yearobj = Year.objects.get(year=year)
        except Year.DoesNotExist:
            yearobj = Year.objects.create(year=year)

        try:
            current = Current.objects.get(year=yearobj, sem=sem)
        except Current.DoesNotExist:
            current = Current.objects.create(year=yearobj, sem=sem)

    cur_year = yearobj
    cur_sem = sem

    if request.user.is_authenticated:
        username = request.user.username
        ctx['username'] = username
    else:
        return redirect('loginpage')

    if username:
        user = User.objects.get(username=username)
        ctx['userobj'] = user
        if user.is_staff is True:
            return redirect('userList')
    else:
        return redirect('loginpage')

    try:
        userinfoobj = UserInfo.objects.get(year=yearobj, sem=sem, student_info=request.user.profile.student_info)
        groupobj = user.profile.group
    except:
        return redirect(reverse('user_check'))

    dataList = Data.objects.filter(author__profile__group=groupobj, year=cur_year, sem=cur_sem).order_by('-id')

    ctx['posts'] = dataList
    ctx['userobj'] = user

    return render(request, 'main.html', ctx)

def confirm_delete_data(request, pk):
    # to fix - 그룹의 멤버들과 관리자만 삭제할 수 있게 한다
    ctx={}

    if request.user.is_authenticated:
        loginname = request.user.username
        pass
    else:
        return redirect('loginpage')

    item = Data.objects.get(id=pk)
    username = item.author
    user = User.objects.get(username=username)

    if request.user.is_staff:
        pass
    elif item.group == request.user.profile.group:
        pass
    else:
        messages.warning(request, 'Invalid Access.', extra_tags='alert')
        return redirect('main')

    Data.objects.filter(id=pk).delete()
    return redirect('main')

def confirm_delete_announce(request, pk):
    ctx={}

    if request.user.is_authenticated:
        loginname = request.user.username
        pass
    else:
        return redirect('loginpage')

    item = Announcement.objects.get(id=pk)
    username = item.author
    user = User.objects.get(username=username)

    Announcement.objects.filter(id=pk).delete()
    messages.success(request, '공지가 삭제되었습니다.', extra_tags='alert')
    return redirect('announce')


# User Login Customization

def trim_string(string1):
    return string1.replace(' ','')

@csrf_exempt
def loginpage(request):
    ctx={}
    if request.method == 'POST':
        username = request.POST['username']
        password =  request.POST['password']

        username = trim_string(username)
        password = trim_string(password)

        user = authenticate(username=username, password=password)

        ctx['user_id'] = username

        if user is not None:
            post = User.objects.filter(username=username)

            if post:
                login(request, user)
                username = request.POST['username']
                response = HttpResponseRedirect(reverse('main'))
                messages.success(request, '환영합니다.', extra_tags='alert')
                return response
            else:
                messages.warning(request, '다시 로그인 해주세요.', extra_tags='alert')
                return render(request, 'login.html', ctx)
        else:
            messages.warning(request, '다시 로그인 해주세요.', extra_tags='alert')

    return render(request, 'login.html', ctx)


@login_required(login_url=LOGIN_REDIRECT_URL)
def group_profile(request, group_pk):
    ctx={}

    group = Group.objects.get(pk=group_pk)
    ctx['group'] = group

    try:
        current = Current.objects.all().first()
        yearobj = current.year
        sem = current.sem
    except Year.DoesNotExist:
        year = current_year()
        yearobj = Year.objects.get(year=year)
        sem = current_sem()
    ctx['year'] = yearobj
    ctx['sem'] = sem

    if yearobj:
        member_list = UserInfo.objects.filter(year=yearobj, sem=sem, group=group).annotate(
            num_posts = Count('data', filter=Q(data__year=yearobj, data__sem=sem)),
            total_time = Sum('data__study_total_duration', filter=Q(data__year=yearobj, data__sem=sem))
        )

        ctx['member_list'] = member_list

    return render(request, 'group_profile.html', ctx)


@login_required(login_url=LOGIN_REDIRECT_URL)
def profile(request):
    ctx={}

    # Tag.objects.filter(person__yourcriterahere=whatever [, morecriteria]).annotate(cnt=Count('person')).order_by('-cnt')[0]
    current = Current.objects.all().first()
    yearobj = current.year
    sem = current.sem
    try:
        userinfoobj = UserInfo.objects.get(year=yearobj, sem=sem, student_info=request.user.profile.student_info)
    except:
        return redirect(reverse('user_check'))
    try:
        user = User.objects.get(pk=request.user.pk)

        # User를 기준으로 하면 가입한 사람만 뜨고, UserInfo를 기준으로 하면 가입하지 않은 사람도 뜬다.
        member_list = UserInfo.objects.filter(year=yearobj, sem=sem, group=userinfoobj.group).annotate(
            num_posts = Count('data', filter=Q(data__year=yearobj, data__sem=sem)),
            total_time = Sum('data__study_total_duration', filter=Q(data__year=yearobj, data__sem=sem))
        )

        ctx['member_list'] = member_list
    except User.DoesNotExist:
        return redirect(reverse('loginpage'))

    return render(request, 'profile.html', ctx)

@staff_member_required
def staff_profile(request):
    ctx={}

    if request.user.is_authenticated:
        username = request.user.username
        user = User.objects.get(username=username)
        ctx['userobj'] = user
    else:
        return redirect('loginpage')

    if username:
        ctx['username'] = username

    ctx['current'] = Current.objects.all()[0]

    return render(request, 'staff_profile.html', ctx)

@staff_member_required
def grid(request):
    ctx = {}
    if request.user.is_authenticated:
        username = request.user.username
        user = User.objects.get(username=username)
        ctx['userobj'] = user
        if user.is_staff is False:
            return redirect('main')
    else:
        return redirect('loginpage')

    if username:
        ctx['username'] = username

    current = Current.objects.all().first()
    ctx['years'] = Year.objects.all()

    if request.method == 'POST':
        year = request.POST['year']
        sem = request.POST['sem']

        yearobj = Year.objects.get(year=year)
        sem = sem

        if year != 'None' and sem != 'None':
            ctx['chosen_year'] = year
            ctx['chosen_sem'] = sem

    else:
        yearobj = current.year
        year = current.year.year
        sem = current.sem
        ctx['year'] = year
        ctx['sem'] = sem


    '''
    ctx['data'] = Data.objects.raw('SELECT * FROM photos_data INNER JOIN \
        (SELECT MAX(id) as id FROM photos_data GROUP BY author) \
            last_updates ON last_updates.id = photos_data.id INNER JOIN photos_userinfo ON photos_data.user_id = photos_userinfo.user_id INNER JOIN photos_year ON photos_userinfo.year_id = photos_year.id\
                WHERE author <> "kate" AND author <> "test" AND author IS NOT NULL AND year=%s AND sem =%s ORDER BY date DESC', [year, sem])
    '''
    '''
    data_ids = Data.objects.filter(year=yearobj, sem=sem).annotate(
        latest_date=Max('date')
    ).values_list('id', flat=True)

    print(data_ids)
    '''

    model_max_set = Data.objects.filter(year=yearobj, sem=sem).values('group').annotate(
        latest_date = Max('date')
    ).order_by().exclude(group__no=0)

    q_statement = Q()
    for pair in model_max_set:
        q_statement |= (Q(group__exact=pair['group']) & Q(date=pair['latest_date']))

    if(len(q_statement)==0):
        data = Data.objects.none()
    else:
        data = Data.objects.filter(q_statement)
    ctx['data'] = data

    return render(request, 'grid.html', ctx)

def logout_view(request):
    try:
        logout(request)
        response = HttpResponseRedirect(reverse('loginpage'))
        return response
    except:
        pass
    return render(request, 'home.html', {})


# def signup(request):
#     ctx = {}
#
#     if request.user.is_authenticated:
#         username = request.user.username
#         user = User.objects.get(username=username)
#         ctx['userobj'] = user
#         if user.is_staff is False:
#             return redirect('main')
#     else:
#         return redirect('loginpage')
#
#     ctx['username'] = username
#     if request.method == 'POST':
#         if request.POST["password1"] == request.POST["password2"]:
#             user = User.objects.create_user(
#                 username=request.POST["username"],
#                 password=request.POST["password1"]
#             )
#
#             this_year = current_year()
#             try:
#                 year = Year.objects.get(year = this_year)
#             except Year.DoesNotExist :
#                 year = None
#
#             if not year:
#                 year = Year(year=this_year)
#                 year.save()
#                 user.userinfo.year = year
#                 user.userinfo.sem = current_sem()
#             else:
#                 user.userinfo.year = year
#                 user.userinfo.sem = current_sem()
#
#             user.save()
#             messages.success(request, '유저가 성공적으로 추가되었습니다.', extra_tags='alert')
#             return redirect("staff_profile")
#
#         else:
#             messages.warning(request, '유저를 만드는데 실패하였습니다.', extra_tags='alert')
#         return render(request, 'signup.html', ctx)
#
#     return render(request, 'signup.html', ctx)


@login_required(login_url=LOGIN_REDIRECT_URL)
@transaction.atomic
def save_profile(request, pk):
    user = User.objects.get(pk=pk)

    if user.profile.phone and user.profile.student_id:
        return redirect(reverse('main'))

    if request.method == 'POST':
        profile = user.profile
        try:
            student_info = StudentInfo.objects.get(student_id=request.POST['student_id'])
        except:
            pass #to fix --> inquiry page with message
        profile.student_info = student_info
        profile.phone = "010" + str(request.POST['phone1']) + str(request.POST['phone2'])
        profile.save()
        return redirect(reverse('main'))

    return render(request, 'save_profile.html')



# UserInfo가 없을 때 관리자에게 문의하는 곳
@login_required(login_url=LOGIN_REDIRECT_URL)
@transaction.atomic
def create_userinfo(request, pk):
    messages.info(request, '학우님의 Group을 찾을 수 없습니다. 관리자에게 문의해주세요')
    user = User.objects.get(pk=request.user.pk)
    print(request.user.username)
    print(request.user.last_name)
    try:
        user = User.objects.get(pk=pk)
    except:
        return redirect(reverse('loginpage'))

    if request.method == 'POST':
        student_id = request.POST['student_id']
        email = request.POST['email']
        print(student_id)
        print(email)

    return render(request, 'create_userinfo.html')

def no_group_notice(request):
    return render(request, 'no_group_notice.html')

def no_student_id(request, pk):
    messages.info(request, '학우님의 학번 정보를 찾을 수 없습니다. 관리자에게 문의해주세요')
    user = User.objects.get(pk=request.user.pk)

    try:
        user = User.objects.get(pk=pk)
    except:
        return redirect(reverse('loginpage'))

    if request.method == 'POST':
        student_id = request.POST['student_id']
        stu_phone_num = "010" + str(request.POST['phone1']) + str(request.POST['phone2'])
        email = request.POST['email']
        username = user.last_name

        try:
            current = Current.objects.all().first()
            yearobj = current.year
            sem = current.sem
        except:
            year = current_year()
            try:
                yearobj = Year.object.get(year=year)
            except:
                yearobj = Year.object.create(year=year)
            sem = current_sem()

        try:
            student_info_obj = StudentInfo.objects.get(student_id=student_id)
        except StudentInfo.DoesNotExist:
            student_info_obj = StudentInfo.objects.create(student_id=student_id, name=username)

        try:
            user_info = UserInfo.objects.get(year=yearobj, sem=sem, student_info=student_info_obj)
        except UserInfo.DoesNotExist:
            # user info 가 저장안된 유저는 문의 페이지로! (profile아직 생성안됨)
            return redirect(reverse('no_group_notice'))

        try:
            user_profile = user.profile
            if not user_profile.phone:
                user_profile.phone = stu_phone_num
        except Profile.DoesNotExist:
            user_profile = Profile.objects.create(user=user, name=username, email=email, student_info=student_info_obj, phone=stu_phone_num)
            if user_info:
                user_profile.group = user_info.group

            user_profile.save()
            return redirect(reverse('main'))

    return render(request, 'no_student_id.html')

def user_check(request):
    if not request.user.is_authenticated:
        return redirect('loginpage')

    if request.user.email.endswith('@handong.edu'):
        try:
            user = User.objects.get(pk=request.user.pk)
            user.email = request.user.email

            # 학교 이메일이 학번으로 시작한다고 가정
            email = request.user.email
            email = email.split('@')
            std_id = email[0]

            if not std_id.isnumeric():
                return HttpResponseRedirect(reverse('no_student_id', args=(user.pk,)))

            username = user.last_name
            email = user.email

            try:
                current = Current.objects.all().first()
                yearobj = current.year
                sem = current.sem
            except:
                year = current_year()
                try:
                    yearobj = Year.object.get(year=year)
                except:
                    yearobj = Year.object.create(year=year)
                sem = current_sem()

            try:
                student_info_obj = StudentInfo.objects.get(student_id=std_id)
            except StudentInfo.DoesNotExist:
                student_info_obj = StudentInfo.objects.create(student_id=std_id, name=username)

            try:
                user_info = UserInfo.objects.get(year=yearobj, sem=sem, student_info=student_info_obj)
            except UserInfo.DoesNotExist:
                # user info 가 저장안된 유저는 문의 페이지로! (profile아직 생성안됨)
                return redirect(reverse('no_group_notice'))

            try:
                user_profile = user.profile
                if not user_profile.group == user_info.group:
                    user_profile.group = user_info.group
                    user_profile.save()
            except Profile.DoesNotExist:
                user_profile = Profile.objects.create(user=user, name=username, email=email)
                if user_info:
                    user_profile.group = user_info.group

                user_profile.save()
                return HttpResponseRedirect(reverse('save_profile', args=(user.pk,)))

        except(KeyError, User.DoesNotExist):
            return HttpResponseRedirect(reverse('loginpage'))

        return HttpResponseRedirect(reverse('main'))
    else:
        messages.info(request, '한동 이메일로 로그인해주세요.')
        User.objects.filter(pk=request.user.pk).delete()
        return HttpResponseRedirect(reverse('loginpage'))

@staff_member_required
def announce_write(request):
    ctx = {}
    if request.user.is_authenticated:
        username = request.user.username
        ctx['username'] = username
        user = User.objects.get(username = username)
        ctx['userobj'] = user
        if user.is_staff is False:
            return redirect('announce')
    else:
        return redirect('loginpage')

    if request.method == "GET":
        form = AnnouncementForm()
    elif request.method == "POST":
        form = AnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            obj.author = username
            obj.save()
            messages.success(request, '공지가 추가되었습니다.', extra_tags='alert')
            return redirect("announce")

    ctx['form'] = form

    return render(request, 'announce_write.html', ctx)

def announce_detail(request, pk):
    post = get_object_or_404(Announcement, pk=pk)

    ctx = {
        'post': post,
    }

    if request.user.is_authenticated:
        username = request.user.username
        user = User.objects.get(username = username)
        ctx['userobj'] = user
        ctx['username'] = username
    else:
        return redirect('loginpage')

    return render(request, 'announce_content.html', ctx)


def change_password(request):
    ctx = {}

    if request.user.is_authenticated:
        username = request.user.username
        user = User.objects.get(username=username)
        ctx['userobj'] = user
    else:
        return redirect('loginpage')

    ctx['username'] = username
    if request.method == 'POST':
        old_password = request.POST["old_password"]
        is_pw_correct = authenticate(username=username, password=old_password)
        if is_pw_correct is not None:
            password1 = request.POST["password1"]
            password2 = request.POST["password2"]

            if password1 == password2:
                user.set_password(password1)
                user.save()
                messages.success(request, '비밀번호가 변경 되었습니다.', extra_tags='alert')
                login(request, user)
                return redirect("profile")

            else:
                messages.warning(request, '바꾸는 비밀번호가 일치해야합니다.', extra_tags='alert')

            return redirect("change_password")
        else:
            messages.warning(request, '현재 비밀번호를 확인해주세요.', extra_tags='alert')
            return render(request, 'change_password.html', ctx)

    return render(request, 'change_password.html', ctx)


def add_member(request):
    ctx={}

    if request.user.is_authenticated:
        username = request.user.username
        ctx['username'] = username
    else:
        return redirect('loginpage')

    if username:
        user = User.objects.get(username=username)
        ctx['userobj'] = user

    if request.method == "GET":
        form = MemberForm()
    elif request.method == "POST":
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            obj.author = username
            obj.user = user
            obj.save()
            messages.success(request, '멤버가 추가되었습니다.', extra_tags='alert')
            return redirect("profile")
        else:
            messages.warning(request, '학번을 확인해주세요.', extra_tags='alert')

    ctx['form'] = form

    return render(request, 'member.html', ctx)

def confirm_delete_member(request, pk):
    item = Member.objects.get(id=pk)
    Member.objects.filter(id=pk).delete()
    return redirect('profile')


def confirm_delete_user(request, pk):
    user = User.objects.get(id=pk)
    User.objects.filter(id=pk).delete()
    return redirect('userList')


# For verification popup
def popup(request):
    ctx = {}

    if request.user.is_authenticated:
        username = request.user.username
        user = User.objects.get(username=username)
        group = user.profile.group
        orig, created = Verification.objects.get_or_create(group=group)

        if orig:
            verification = orig
        else:
            verification = created

        now_time = timezone.localtime()


        if verification.code_when_saved is None:
            verification.code_when_saved = now_time
            verify_code = random.choice(possible)
            verification.code = verify_code
            verification.save()
            ctx['code'] = verify_code


        save_time = verification.code_when_saved

        time_diff = now_time - save_time

        if (time_diff.seconds)/60 >= 10:
            verify_code = random.choice(possible)
            verification.code = verify_code
            verification.code_when_saved = now_time
            verification.save()
            ctx['code'] = verify_code
        else:
            if verification.code is None:
                verify_code = random.choice(possible)
                verification.code = verify_code
                verification.code_when_saved = now_time
                verification.save()
                ctx['code'] = verify_code
            else:
                ctx['code'] = verification.code

        return render(request, 'popup.html', ctx)
    else:
        return redirect("main")

def inquiry(request):
    ctx = {}

    if request.user.is_authenticated:
        username = request.user.username
        user = User.objects.get(username=username)
        ctx['userobj'] = user
        ctx['username'] = username

    return render(request, 'inquiry.html', ctx)


def img_download_page(request):
    ctx={}

    if request.user.is_authenticated:
        username = request.user.username
        user = User.objects.get(username=username)
        ctx['userobj'] = user
        if user.is_staff is False:
            return redirect('main')
    else:
        return redirect('loginpage')

    years = Year.objects.all()
    ctx['years'] = years

    if request.method == 'POST':
        year = request.POST['year']
        sem = request.POST['semester']

        year = int(year)
        sem = int(sem)

        if year != 'None' and sem != 'None':
            return redirect('img_download', year, sem)
        else:
            messages.warning(request, '연도와 학기정보를 정확하게 입력해주세요.', extra_tags='alert')


    return render(request, 'img_download_page.html', ctx)

from django.conf import settings
import zipfile
from wsgiref.util import FileWrapper
import os

def img_download(request, year, sem):
    home = os.path.expanduser('~')
    location = os.path.join(home, 'Downloads')
    location += '/'

    ctx={}
    if request.user.is_authenticated:
        username = request.user.username
        user = User.objects.get(username=username)
        ctx['userobj'] = user
        if user.is_staff is False:
            return redirect('main')
    else:
        return redirect('loginpage')


    yearobj = Year.objects.get(year=year)
    user_list = User.objects.filter(profile__student_info__userinfo__year=yearobj, profile__student_info__userinfo__sem=sem)

    group_list = Group.objects.all().exclude(no=0)

    export_zip = zipfile.ZipFile("/home/chickadee/HGUstudy/histudy_img.zip", 'w')
    
    
    for group in group_list:
        cnt=1        
        data_list = Data.objects.filter(year=yearobj, sem=sem, group=group)

        for data in data_list:
            file_name = 'group'+ str(group.no) + '_' + str(cnt) + '.png'
            product_image_url = data.image.url

            image_path = settings.MEDIA_ROOT+ product_image_url[13:]
            image_name = product_image_url; # Get your file name here.

            export_zip.write(image_path, file_name)
            cnt += 1

    export_zip.close()

    wrapper = FileWrapper(open('/home/chickadee/HGUstudy/histudy_img.zip', 'rb'))
    content_type = 'application/zip'
    content_disposition = 'attachment; filename=histudy_img.zip'

    response = HttpResponse(wrapper, content_type=content_type)
    response['Content-Disposition'] = content_disposition

    messages.success(request, '이미지 다운로드를 완료하였습니다.', extra_tags='alert')


    return response


@csrf_exempt
# made by Group5 - Sumi(21700520@handong.edu) to add new feature 'register' (2021-06-04)
def register_form(request):
    
    ctx = {}

    if request.method == 'POST':
        # time stamp ?

        check_notice = request.POST['check_notice']
        student_id = request.POST['student_id']
        name = request.POST['name']
        gender = request.POST['gender']
        phone = request.POST['phone']
        study_type = request.POST['study_type']
        want_member = request.POST['want_member']
        
        class1_code = request.POST['class1_code']
        class1_name = request.POST['class1_name']
        class1_prof = request.POST['class1_prof']
        
        class2_code = request.POST['class2_code']
        class2_name = request.POST['class2_name']
        class2_prof = request.POST['class2_prof']

        class3_code = request.POST['class3_code']
        class3_name = request.POST['class3_name']
        class3_prof = request.POST['class3_prof']

        demand = request.POST['demand']
        english_ok = request.POST['english_ok']
        club_study = request.POST['club_study']
        do_club = request.POST['do_club']
        club_name = request.POST['club_name']
        info_agree = request.POST['info_agree']
        
        # 이미 해당 학번의 신청 정보가 있을 경우 받아옴
        try:
            answer = Answer.objects.get(student_id=student_id)
        except:
            answer = None

        # 이미 정보가 있으면 update ==> 이거 되는지 확인해봐야 함
        if answer:
            Answer.objects.update_or_create(check_notice=check_notice, student_id=student_id, name=name, gender=gender, 
            phone=phone, study_type=study_type, want_member=want_member, class1_code=class1_code, class1_name=class1_name, class1_prof=class1_prof,
            class2_code=class2_code, class2_name=class2_name, class2_prof=class2_prof, class3_code=class3_code, class3_name=class3_name, class3_prof=class3_prof,
            demand=demand, english_ok=english_ok, club_study=club_study, do_club=do_club, club_name=club_name, info_agree=info_agree)

            msg = student_id + name + '님의 스터디 신청 수정이 완료되었습니다'
            messages.success(request, msg)

        # 없으면 create
        else:
            Answer.objects.create(check_notice=check_notice, student_id=student_id, name=name, gender=gender, 
            phone=phone, study_type=study_type, want_member=want_member, class1_code=class1_code, class1_name=class1_name, class1_prof=class1_prof,
            class2_code=class2_code, class2_name=class2_name, class2_prof=class2_prof, class3_code=class3_code, class3_name=class3_name, class3_prof=class3_prof,
            demand=demand, english_ok=english_ok, club_study=club_study, do_club=do_club, club_name=club_name, info_agree=info_agree)

            msg = student_id + name + '님의 스터디 신청이 완료되었습니다'
            messages.success(request, msg)

    else: 
        pass
        
    return render(request, 'register_form.html', ctx)

# by Group5 - Sumi(21700520@handong.edu)
