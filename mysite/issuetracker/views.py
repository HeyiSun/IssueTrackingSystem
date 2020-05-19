from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
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
        return projectDisplay(request)
        # TODO(heyi): return projectDisplay(request)
    else:
        return debug(request, "Your username and password didn't match.")


def logout(request):
    request.session.pop('username', None)
    return HttpResponse("You successfully logged out.")


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

    project_description = queryProjectObj(project_id).pdescription
    issue_columns, issue_results = queryIssueInProject(project_id)
    _, lead_results = queryLeadersOfProject(project_id);

    return render(request, 'project_info.html',
                  {'table_query_results' : issue_results,
                   'table_column_names' : issue_columns,
                   'table_link' : '/issue/?issue_id=',
                   'list_title' : 'Leader',
                   'list_link' : '/user/?username=',
                   'list_results' : lead_results,
                   'description' : project_description})


def issueInfo(request):
    if request.session.get('username') is None:
        return notLogin(request)

    if not request.GET.get('issue_id', ''):
        return render(request, 'issue_info.html')

    issue_id = request.GET['issue_id']

    issue_description = queryIssueObj(issue_id).idescription
    issue_columns, issue_results = queryIssueWithId(issue_id)
    _, assign_results = queryAssigneeOfIssue(issue_id);

    return render(request, 'issue_info.html',
                  {'list_title' : 'Assignee',
                   'list_link' : '/user/?username=',
                   'list_results' : assign_results,
                   'description' : issue_description})


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
        return render(request, 'leader_add.html')
        # TODO(heyi): return empty(request, 'Project id')

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
    # TODO(heyi): update lead
    # (new_leader.uid, project_id)
    return debug(request, 'Successfully add leader')


def issueAssign(request):
    if request.session.get('username') is None:
        return notLogin(request)

    if not request.GET.get('issue_id', '') or \
       not request.GET.get('assignee_username', ''):
        return render(request, 'issue_assign.html')
        # TODO(heyi):return empty(request, 'project Id')

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
    # TODO(heyi): update assign
    # (user_id, assignee.uid, issue_id, time)
    return debug(request, 'Successfully assign issue')


def statusChange(request):
    if request.session.get('username') is None:
        return notLogin(request)

    if not request.GET.get('issue_id', ''):
        return render(request, 'status_change.html')
        # TODO(heyi): return empty(request, 'issue id')
    if not request.GET.get('from_status_name', '') or \
       not request.GET.get('to_status_name', ''):
        return render(request, 'status_change.html')
        # TODO(heyi): return empty(request, 'from/to status')
    username = request.session.get('username')
    issue_id = request.GET.get('issue_id')
    from_status_name = request.GET.get('from_status_name')
    to_status_name = request.GET.get('to_status_name')
    user_id = queryUserObj(username).uid

    issue = queryIssueObj(issue_id)
    if issue is None:
        return notExist(request, "Issue " + issue_id)

    if not queryUserIsLeadOfIssue(username, issue_id) and \
       not queryUserIsAssignee(username, issue_id):
        return unauthorized(request)

    from_status = queryStatusObj(from_status_name, issue.ipid.pid)
    to_status = queryStatusObj(to_status_name, issue.ipid.pid)
    print(from_status, to_status)
    if from_status is None or to_status is None:
        return notExist(request, 'Status ' + from_status_name + \
                                 ' or ' + to_status_name)
    if issue.currentstatus.sid != from_status.sid:
        return debug(request, "From state is not issue's current state.")

    if not queryStatusTransIsExisted(from_status.sid, to_status.sid):
        return debug(request, "Invalid status transition from " +\
                              from_status_name + " to " + to_status_name)
    
    # TODO(heyi): Update status, add the transition to status change
    # (user_id, issue.iid, from_status.sid, to_status.sid)
    return HttpResponse('Successfully change status')


def userAdd(request):
    if not request.GET.get('username', ''):
        return render(request, 'user_add.html')
        # TODO(heyi): return empty(request, 'Username')
    if not request.GET.get('password', ''):
        return render(request, 'user_add.html')
        # TODO(heyi): return empty(request, 'Password')
    username = request.GET.get('username')
    password = request.GET.get('password')
    display_name  = request.GET.get('display_name')
    email  = request.GET.get('email')

    if queryUserObj(username) is not None:
        return alreadyExist(request, 'This username')

    # TODO(heyi): Add user
    return HttpResponse('Successfully add user')



def projectAdd(request):
    if request.session.get('username', '') is None:
        return notLogin(request)
    # Not sure if project name can be empty
    if not request.GET.get('project_name', ''):
        return render(request, "project_add.html")
        # TODO(heyi): return empty(request, 'Project name')
    username = request.session.get('username')
    project_name = request.GET.get("project_name")
    project_description = request.GET.get("project_description")
    creator_id = queryUserObj(username).uid
    # TODO(heyi): Add project
    # TODO(heyi): Add 'OPEN' status
    return HttpResponse("Successfully add project.")



def issueAdd(request):
    if request.session.get('username') is None:
        return notLogin(request)
    # Not sure if issue title name can be empty
    if not request.GET.get('issue_title', ''):
        return render(request, "issue_add.html")
        # TODO(heyi): return empty(request, 'Issue title')
    if not request.GET.get('project_id', ''):
        return render(request, "issue_add.html")
        # TODO(heyi): return empty(request, 'Project id')
    username = request.session.get('username')
    issue_title = request.GET.get("issue_title")
    issue_description = request.GET.get("issue_description")
    project_id = request.GET.get("project_id")
    creator_id = queryUserObj(username).uid

    open_status = queryStatusObj('OPEN', project_id)
    if open_status is None:
        return debug(request, "The project's OPEN status is not set properly")
    # TODO(heyi): Add Issue
    # (issue_title, issue_description, open_status.sid, creator_id, time, project_id)
    return HttpResponse('Successfully add issue')




def statusAdd(request):
    if request.session.get('username') is None:
        return notLogin(request)
    if not request.GET.get('project_id', ''):
        return render(request, "status_add.html")
        # TODO(heyi): return empty(request, 'Project id')
    if not request.GET.get('status_name', ''):
        return render(request, "status_add.html")
        # TODO(heyi): return empty(request, 'Status name')
    username = request.session.get('username')
    status_name = request.GET.get('status_name')
    status_description = request.GET.get('status_description')
    project_id = request.GET.get('project_id')

    if queryProjectObj(project_id) is None:
        return notExist(request, "Project id " + project_id)

    if not queryUserIsLeadOfProject(username, project_id):
        return unauthorized(request)

    if queryStatusObj(status_name, project_id) is not None:
        return alreadyExist(request, 'Status ' + status_name)
    # Add status
    # (status_name, status_description, project_id)
    return HttpResponse('Successfully add status')


def statustransAdd(request):
    if request.session.get('username') is None:
        return notLogin(request)
    if not request.GET.get('project_id', ''):
        return render(request, "statustrans_add.html")
        # TODO(heyi): return empty(request, 'Project id')
    if not request.GET.get('from_status_name', '') or \
       not request.GET.get('to_status_name', ''):
        return render(request, "statustrans_add.html")
        # TODO(heyi): return empty(request, 'Status name')
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
    # TODO(heyi): Add status transition
    # (from_status.sid, to_status.sid)
    return HttpResponse('Successfully add status transition')

#def injection(request):
#    if request.session.get('username') is None:
#        return notLogin(request)
#
#    if not request.GET.get('issue_id', ''):
#        return render(request, 'issue_display.html')
#
#    columns = None
#    results = None
#    if not request.GET.get('issue_id', ''):
#        project_id = request.GET['project_id']
#        columns, results = queryIssueInProject(project_id)
#    else:
#        issue_id = request.GET['issue_id']
#        columns, results = queryIssueWithId(issue_id)
#
#    return render(request, 'issue_display.html',
#                  {'table_query_results' : results,
#                   'table_column_names' : columns})




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

