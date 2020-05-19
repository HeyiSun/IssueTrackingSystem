from django.db import connection
from issuetracker.models import *

def querySetToList(raw_qs):
    """ helper function: convert querySet to two lists: list of field name & list of data"""
    columns = raw_qs.columns
    res = []
    for row in raw_qs:
        res.append(tuple(getattr(row, col) for col in columns))
    return (columns, res)

def querySetToListFilter(raw_qs, filter_columns):
    columns = raw_qs.columns
    columns = [item for item in columns if item not in filter_columns]
    res = []

    for row in raw_qs:
        res.append(tuple(getattr(row, col) for col in columns))
    return (columns, res)



# query functions for objects
def queryUserObj(username):
    userQS = User.objects.raw("SELECT *  \
                               FROM user \
                               WHERE BINARY UNAME = %s", [username])
    return userQS[0] if len(userQS) != 0 else None


def queryIssueObj(issue_id):
    issueQS = Issue.objects.raw("SELECT *   \
                                 FROM issue \
                                 WHERE iid = %s", [issue_id])
    return issueQS[0] if len(issueQS) != 0 else None
    

def queryProjectObj(project_id):
    projectQS = Project.objects.raw("SELECT *     \
                                     FROM project \
                                     WHERE pid = %s", [project_id])
    return projectQS[0] if len(projectQS) != 0 else None


def queryStatusObj(statusname, project_id):
    statusQS = Status.objects.raw("SELECT *     \
                                   FROM status  \
                                   WHERE sname = %s and spid = %s", [statusname, project_id])
    return statusQS[0] if len(statusQS) != 0 else None




# query functions which returns bool
def queryUserIsLeadOfIssue(username, issue_id):
    leadQS = User.objects.raw("SELECT user.uid                                               \
                               FROM user JOIN `lead` JOIN project JOIN issue ON              \
                                    (user.uid = `lead`.uid AND project.pid = issue.ipid      \
                                    AND lead.pid = project.pid)                              \
                               WHERE uname = %s AND iid = %s", [username, issue_id])
    return len(leadQS) != 0


def queryUserIsLeadOfProject(username, project_id):
    leadQS = User.objects.raw("SELECT user.uid                                  \
                               FROM user JOIN `lead` ON (user.uid = `lead`.uid) \
                               WHERE uname = %s AND pid = %s", [username, project_id])
    return len(leadQS) != 0


def queryUserIsAssignee(username, issue_id):
    assigneeQS = User.objects.raw("SELECT user.uid                                    \
                                   FROM assign JOIN user on (assign.auid = user.uid)  \
                                   WHERE uname = %s AND iid = %s", [username, issue_id])
    return len(assigneeQS) != 0


def queryStatusTransIsExisted(from_sid, to_sid):
    with connection.cursor() as cursor:
         num = cursor.execute("SELECT *         \
                               FROM statustrans \
                               WHERE ssid = %s AND tsid = %s", [from_sid, to_sid])
    return num != 0

# "SELECT *                                                    \
#  FROM status s1 JOIN statustrans JOIN status s2 JOIN issue          \
#       ON (s1.sid = statustrans.ssid AND s2.sid = statustrans.tsid   \
#           AND issue.currentstatus = s1.sid)                         \
#  WHERE iid = %s and s1.sname = %s and s2.sname = %s"






# query functions for data
def queryUserInfo(username):
    userQS = User.objects.raw("SELECT uid, uname, email, disname \
                               FROM user                    \
                               WHERE uname = %s", [username])
    return querySetToListFilter(userQS, ['uid'])


def queryProjectAll():
    projectQS = Project.objects.raw("\
                SELECT pid, pname as name, \
                       uname as creator,          \
                       ptime as createtime       \
                FROM project join user on (puid = uid)");
    return querySetToList(projectQS)


def queryIssueInProject(project_id):
    issueQS = Issue.objects.raw("SELECT iid, title, sname as status,             \
                                        itime as createtime, disname as reporter \
                                 FROM issue join status join user on             \
                                      (currentstatus = sid and iuid = uid)       \
                                 WHERE ipid = %s", [project_id])
    return querySetToList(issueQS)
    

def queryIssueWithId(issue_id):
    issueQS = Issue.objects.raw("SELECT iid, title, sname as status,             \
                                        itime as createtime, disname as reporter \
                                 FROM issue join status join user on             \
                                      (currentstatus = sid and iuid = uid)       \
                                 WHERE iid = %s", [issue_id])
    return querySetToList(issueQS)


def queryLeadersOfProject(project_id):
    userQS = User.objects.raw("SELECT uid, uname             \
                               FROM `lead` NATURAL JOIN user \
                               WHERE pid = %s", [project_id])
    return querySetToListFilter(userQS, 'uid');
  

def queryAssigneeOfIssue(issue_id):
    userQS = User.objects.raw("SELECT user.uid, uname                     \
                               FROM assign JOIN user on (auid = user.uid) \
                               WHERE iid = %s", [issue_id])
    return querySetToListFilter(userQS, 'uid');
    



# def dictfetchall(cursor):
#     "Return all rows from a cursor as a dict"
#     columns = [col[0] for col in cursor.description]
#     return [
#         dict(zip(columns, row))
#         for row in cursor.fetchall()
#     ]
# 
# def dictfetchone(cursor):
#     "Return one rows from a cursor as a dict"
#     columns = [col[0] for col in cursor.description]
#     return dict(zip(columns, cursor.fetchone))
    
