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
    """ helper function: same as querySetToList, filter some field"""
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
    projectQS = Project.objects.raw(
               "SELECT pid, pname as name, \
                       uname as creator,          \
                       ptime as createtime       \
                FROM project join user on (puid = uid)")
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
    return querySetToListFilter(userQS, 'uid')
  

def queryAssigneeOfIssue(issue_id):
    userQS = User.objects.raw("SELECT user.uid, uname                     \
                               FROM assign JOIN user on (auid = user.uid) \
                               WHERE iid = %s", [issue_id])
    return querySetToListFilter(userQS, 'uid')
    

def queryNextStatus(issue_id):
    statusQS = Status.objects.raw(
            "SELECT s2.sid, s2.sname                                              \
             FROM status s1 JOIN statustrans JOIN status s2 JOIN issue            \
                  ON (s1.sid = statustrans.ssid AND s2.sid = statustrans.tsid AND \
                      issue.currentstatus = s1.sid)                               \
             WHERE iid=%s", [issue_id])
    return querySetToListFilter(statusQS, 'sid')


def queryStatusOfProject(project_id):
    statusQS = Status.objects.raw(
            "SELECT sid, sname \
             FROM status       \
             WHERE spid = %s", [project_id])
    return querySetToListFilter(statusQS, 'sid')


def queryIssueHistory(issue_id):
    statusQS = Status.objects.raw(
        "SELECT s1.sid, s1.sname, s2.sname, uname, supdatetime               \
         FROM  status s1 JOIN changestatus JOIN status s2 JOIN user          \
               ON (s1.sid = changestatus.ssid AND s2.sid = changestatus.tsid \
                   AND changestatus.uid = user.uid)                          \
         WHERE iid = %s", [issue_id])
    return querySetToListFilter(statusQS, 'sid')


def queryIssueWithKeyword(project_id, keyword):
    keyword = '%' + keyword + '%'
    issueQS = Issue.objects.raw(
            "SELECT iid, title, sname as status,             \
                    itime as createtime, disname as reporter \
             FROM issue join status join user on        \
                  (currentstatus = sid and iuid = uid)       \
             WHERE title LIKE %s AND ipid = %s", [keyword, project_id])
    return querySetToList(issueQS)
                                 





# Insert
def insertChangeStatus(user_id, issue_id, from_status_id, to_status_id):
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO changestatus \
                        VALUES (%s, %s, %s, %s, NOW())",
                        [user_id, issue_id, from_status_id, to_status_id])


def insertUser(username, password, email, display_name):
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO user(uname, password, email, disname) \
                        VALUES(%s, %s, %s, %s)",
                        [username, password, email, display_name])


def insertProject(project_name, project_description, creator_id):
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO project(pname, pdescription, puid, ptime) \
                        VALUES(%s, %s, %s, NOW())",
                        [project_name, project_description, creator_id])
        cursor.execute("INSERT INTO status(sname, sdescription, spid) \
                        VALUES('OPEN', 'Initial State', LAST_INSERT_ID())")

def insertIssue(issue_title, issue_description, open_status_id, creator_id, project_id):
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO issue(title, idescription, currentstatus, iuid, itime, ipid) \
                        VALUES(%s, %s, %s, %s, NOW(), %s)", [issue_title, issue_description,
                                                             open_status_id, creator_id, project_id])


def insertLead(uid, pid):
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO `lead` \
                        VALUES(%s, %s)", [uid, pid]);


def insertAssign(assigner_id, assignee_id, issue_id):
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO assign \
                        VALUES(%s, %s, %s, NOW())",
                        [assigner_id,assignee_id, issue_id])


def insertStatus(status_name, status_description, project_id):
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO status(sname, sdescription, spid) \
                        VALUES(%s, %s, %s)",
                        [status_name, status_description, project_id])


def insertStatusTrans(from_sid, to_sid):
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO statustrans \
                        VALUES(%s, %s)", [from_sid, to_sid])





# Update
def updateIssueStatus(issue_id, to_status_id):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE issue         \
                        SET currentstatus=%s \
                        WHERE iid = %s", [to_status_id, issue_id])
    

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
    
