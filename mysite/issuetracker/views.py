from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from django.urls import reverse
from issuetracker.models import *
from issuetracker.query import *
import datetime 
# TODO(heyi): check input length (and password security)


# may exist a homepage
def index(request):
    return render(request, 'login.html')
    # return render(request, 'index.html')


def login(request):
    if not request.POST.get('username', '') or \
       not request.POST.get('password', ''):
        return render(request, 'login.html')

    username = request.POST['username']
    password = request.POST['password']
    user = queryUserObj(username)

    if user is None:
        return notExist(request, "Username")

    if password == user.password:
        request.session['username'] = user.uname
        return redirect(reverse('project_display'))
    else:
        return debug(request, "Your username and password didn't match.")


def logout(request):
    request.session.pop('username', None)
    return render(request, 'login.html')
    # return HttpResponse("You successfully logged out.")


def projectDisplay(request):
    if request.session.get('username') is None:
        return notLogin(request)

    project_columns, project_results = queryProjectAll()
    
    return render(request, 'project_display.html',
                      {'table_query_results' : project_results,
                       'table_column_names' : project_columns,
                       'table_link' : '/project/?project_id='})


def projectInfo(request):
    if request.session.get('username') is None:
        return notLogin(request)

    if not request.GET.get('project_id', ''):
        return render(request, 'project_info.html')

    project_id = request.GET['project_id']

    project_obj = queryProjectObj(project_id)
    project_description = project_obj.pdescription
    project_name = project_obj.pname
    issue_columns, issue_results = queryIssueInProject(project_id)
    _, lead_results = queryLeadersOfProject(project_id)
    _, all_status = queryStatusOfProject(project_id)

    return render(request, 'project_info.html',
                  {'table_query_results' : issue_results,
                   'table_column_names' : issue_columns,
                   'table_link' : '/issue/?issue_id=',
                   'list_title' : 'Leader',
                   'list_link' : '/user/?username=',
                   'list_results' : lead_results,
                   'name' : project_name,
                   'description' : project_description,
                   'project_id' : project_id,
                   'all_status' : all_status})


def issueInfo(request):
    if request.session.get('username') is None:
        return notLogin(request)

    if not request.GET.get('issue_id', ''):
        return render(request, 'issue_info.html')

    issue_id = request.GET['issue_id']

    issue_obj = queryIssueObj(issue_id)
    issue_description = issue_obj.idescription
    issue_status = issue_obj.currentstatus.sname
    issue_name = issue_obj.title
    issue_columns, issue_results = queryIssueWithId(issue_id)
    _, assign_results = queryAssigneeOfIssue(issue_id)
    _, status_results = queryNextStatus(issue_id)

    return render(request, 'issue_info.html',
                  {'list_title' : 'Assignee',
                   'list_link' : '/user/?username=',
                   'list_results' : assign_results,
                   'description' : issue_description,
                   'name' : issue_name,
                   'dropdown_title' : 'Status',
                   'dropdown_results' : status_results,
                   'dropdown_button' : issue_status})


def user(request):
    if request.session.get('username') is None:
        return notLogin(request)

    if not request.GET.get('username', ''):
        username = request.session.get('username')
    else:
        username = request.GET['username']
        # return render(request, 'user.html')
        # TODO(heyi): return empty(request, 'uname')

    columns, results = queryUserInfo(username)

    return render(request, 'user.html',
                  {'table_query_results' : results,
                   'table_column_names' : columns})


def leaderAdd(request):
    if request.session.get('username') is None:
        return notLogin(request)

    if not request.GET.get('project_id', '') or \
       not request.GET.get('new_leader_username', ''):
        return empty(request, 'Project id')

    username = request.session.get('username')
    project_id = request.GET.get('project_id')
    new_leader_username = request.GET.get('new_leader_username')
    
    if queryProjectObj(project_id) is None:
        return notExist(request, "Project id " + project_id)

    if not queryUserIsLeadOfProject(username, project_id):
        return unauthorized(request)

    new_leader = queryUserObj(new_leader_username)
    if new_leader is None:
        return notExist(request, "User " + new_leader_username)

    if queryUserIsLeadOfProject(new_leader_username, project_id):
        return alreadyExist(request, "This leader")

    insertLead(new_leader.uid, project_id)
    return redirect('{}?project_id={}'.format(reverse('project_info'), project_id))


def issueAssign(request):
    if request.session.get('username') is None:
        return notLogin(request)

    if not request.GET.get('assignee_username', ''):
        return empty(request, 'assignee username')

    username = request.session.get('username')
    issue_id = request.GET.get('issue_id')
    assignee_username = request.GET.get('assignee_username')
    user_id  = queryUserObj(username).uid

    if queryIssueObj(issue_id) is None:
        return notExist(request, "Issue " + issue_id)

    if not queryUserIsLeadOfIssue(username, issue_id):
        return unauthorized(request)

    assignee = queryUserObj(assignee_username)
    if assignee is None:
        return notExist(request, "User " + assignee_username)

    if queryUserIsAssignee(assignee_username, issue_id):
        return alreadyExist(request, "This assignee")

    insertAssign(user_id, assignee.uid, issue_id)
    return redirect('{}?issue_id={}'.format(reverse('issue_info'), issue_id))


def statusChange(request):
    if request.session.get('username') is None:
        return notLogin(request)

    if not request.GET.get('issue_id', ''):
        return empty(request, 'issue id')

    if not request.GET.get('to_status_name', ''):
        return empty(request, 'from/to status')

    username = request.session.get('username')
    issue_id = request.GET.get('issue_id')
    user_id = queryUserObj(username).uid
    to_status_name = request.GET.get('to_status_name')

    issue = queryIssueObj(issue_id)
    if issue is None:
        return notExist(request, "Issue " + issue_id)

    if not queryUserIsLeadOfIssue(username, issue_id) and \
       not queryUserIsAssignee(username, issue_id):
        print("11111")
        return unauthorized(request)

    from_status = issue.currentstatus
    to_status = queryStatusObj(to_status_name, issue.ipid.pid)
    from_status_name = from_status.sname

    if to_status is None:
        return notExist(request, 'Status ' + to_status_name)

    if not queryStatusTransIsExisted(from_status.sid, to_status.sid):
        return debug(request, "Invalid status transition from " +\
                              from_status_name + " to " + to_status_name)
    
    insertChangeStatus(user_id, issue_id, from_status.sid, to_status.sid)
    updateIssueStatus(issue_id, to_status.sid)
    return redirect('{}?issue_id={}'.format(reverse('issue_info'), issue_id))


def userAdd(request):
    if not request.POST.get('username', '') or \
       not request.POST.get('password', '') or \
       not request.POST.get('email', '') or \
       not request.POST.get('display_name', ''):
        return render(request, 'user_add.html')

    username = request.POST.get('username')
    password = request.POST.get('password')
    display_name  = request.POST.get('display_name')
    email  = request.POST.get('email')

    if queryUserObj(username) is not None:
        return alreadyExist(request, 'This username')

    insertUser(username, password, email, display_name)
    return HttpResponse('Successfully add user')



def projectAdd(request):
    if request.session.get('username', '') is None:
        return notLogin(request)
    # Not sure if project name can be empty
    if not request.GET.get('project_name', ''):
        return render(request, "project_add.html")

    username = request.session.get('username')
    project_name = request.GET.get("project_name")
    project_description = request.GET.get("project_description")
    creator_id = queryUserObj(username).uid

    insertProject(project_name, project_description, creator_id)

    return redirect(reverse('project_display'))



def issueAdd(request):
    if request.session.get('username') is None:
        return notLogin(request)

    if not request.GET.get('project_id', ''):
        return empty(request, 'Project id')

    project_id = request.GET.get("project_id")
    # Not sure if issue title name can be empty
    if not request.GET.get('issue_title', '') or \
       not request.GET.get('issue_description', ''):
        return render(request, "issue_add.html",
                      {"project_id" : project_id})

    username = request.session.get('username')
    issue_title = request.GET.get("issue_title")
    issue_description = request.GET.get("issue_description")
    creator_id = queryUserObj(username).uid

    open_status = queryStatusObj('OPEN', project_id)
    if open_status is None:
        return debug(request, "The project's OPEN status is not set properly")

    insertIssue(issue_title, issue_description, open_status.sid, creator_id, project_id)
    return redirect('{}?project_id={}'.format(reverse('project_info'), project_id))



def statusAdd(request):
    if request.session.get('username') is None:
        return notLogin(request)

    if not request.GET.get('project_id', ''):
        return empty(request, 'Project id')
    if not request.GET.get('status_name', ''):
        return empty(request, 'Status name')

    username = request.session.get('username')
    status_name = request.GET.get('status_name')
    status_description = request.GET.get('status_description', "")
    project_id = request.GET.get('project_id')

    if queryProjectObj(project_id) is None:
        return notExist(request, "Project id " + project_id)

    if not queryUserIsLeadOfProject(username, project_id):
        return unauthorized(request)

    if queryStatusObj(status_name, project_id) is not None:
        return alreadyExist(request, 'Status ' + status_name)

    insertStatus(status_name, status_description, project_id)
    return redirect('{}?project_id={}'.format(reverse('project_info'), project_id))


def statustransAdd(request):
    if request.session.get('username') is None:
        return notLogin(request)

    if not request.GET.get('project_id', ''):
         return empty(request, 'Project id')

    if not request.GET.get('from_status_name', '') or \
       not request.GET.get('to_status_name', ''):
         return empty(request, 'Status name')

    username = request.session.get('username')
    project_id = request.GET.get('project_id')
    from_status_name = request.GET.get('from_status_name')
    to_status_name = request.GET.get('to_status_name')

    if queryProjectObj(project_id) is None:
        return notExist(request, "Project id " + project_id)

    if not queryUserIsLeadOfProject(username, project_id):
        return unauthorized(request)
    
    from_status = queryStatusObj(from_status_name, project_id)
    to_status = queryStatusObj(to_status_name, project_id)
    if from_status is None or to_status is None:
        return notExist(request, 'Status ' + from_status_name + \
                                 ' or ' + to_status_name)

    if queryStatusTransIsExisted(from_status.sid, to_status.sid):
        return alreadyExist(request, "Transition from " + from_status_name + \
                                     " to " + to_status_name)

    insertStatusTrans(from_status.sid, to_status.sid)
    return redirect('{}?project_id={}'.format(reverse('project_info'), project_id))





# Error handle functions
def notLogin(request):
    return render(request, 'login.html')


def empty(request, string):
    return debug(request, string + ' can\'t be empty.')


def alreadyExist(request, string):
    return debug(request, string + " has already been existed.")


def notExist(request, string):
    return debug(request, string + " doesn't exist.")


def unauthorized(request):
    return debug(request, 'You don\'t have the authorization of this operation.')


def debug(request, debug_str):
    return render(request, 'debug.html', {'debug_msg' : debug_str})

