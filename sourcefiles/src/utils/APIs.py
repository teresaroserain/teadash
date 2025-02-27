from requests_oauthlib import OAuth2Session
import requests
import json, sys
from requests_html import HTMLSession
from uri_template import URITemplate, expand


# ===============call API and create dataframes==========================
AUTH_TOKEN = 'token'
token = {
    'access_token': 'token',
    'token_type': 'Bearer',
    'expires_in': '99999',     # initially 3600, need to be updated by you
}

headers = {
            'Authorization': f'Bearer {AUTH_TOKEN}',
            'Accept': 'application/json'
            }

baseUrl = "https://.../api/v1" 

def test2(url, param1):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'}
        url = baseUrl + url
        print("url 1 ", url)
       
        t = URITemplate(url)
        #t = t.expand(param=param1)
        print(t.expand(param=param1))
       
        response = requests.get(t.expand(param=param1), headers= headers)
        print(response.raise_for_status())
        print(response.status_code)
        rr = json.loads(response.content)
        print("context ", rr)
    except:
        print(repr(response))
        print(sys.exc_info())

""" def test(url, param1):
    try:
        #url = baseUrl + url
        session = HTMLSession()
        r = session.get(URL, headers={...}, timeout=10)
        r.html.render()

        print("para ", param1)
        headers = { 
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Content-Type':'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Connection': 'keep-alive',
                    'Origin': 'https://canvas.kth.se/api/v1',
                    "Host": "https://canvas.kth.se/api/v1",
                    "Referer": "https://canvas.kth.se/api/v1",
                    }
        #params = {'param': param1}
        url = baseUrl+'/courses/{}/quizzes'.format(param1)
        print("url ", url)
        response = requests.request('GET', url, headers=headers)
        response.raise_for_status()  # raises exception when not a 2xx response
        if response.status_code != 204:
            return response.json()
    except:
        print(repr(response))
        print(sys.exc_info()) """



def open_connection_param(url, param1):
    try:
        url = baseUrl + url
        client = OAuth2Session(token=token)
        response = client.get(url.format(param1))
    except:
        print(repr(response))
        print(sys.exc_info())
    return json.loads(response.text)
        
def open_connection_2params(url, param1, param2):
    try:
        url = baseUrl + url
        client = OAuth2Session(token=token)
        response = client.get(url.format(param1, param2))
        print("url ", url.format(param1, param2))
    except:
        print(repr(response))
        print(sys.exc_info())
    return json.loads(response.text)

def open_connection_3params(url, param1, param2, param3):
    try:
        url = baseUrl + url
        client = OAuth2Session(token=token)
        response = client.get(url.format(param1, param2, param3))
    except:
        print(repr(response))
        print(sys.exc_info())
    return json.loads(response.text)

urlAnalyticsAssignments = "/courses/{}/analytics/users/{}/assignments" #courseId, userId
urlListofAssignments = "/courses/{}/assignments" #courseId
urlAssignmentSubmissions = "/courses/{}/assignments/{}/submissions" #courseId, assignmentId
urlStudents =  "/courses/{}/students" #courseId
urlActivities = "/courses/{}/analytics/users/{}/activity" #courseId, userId
urlPageView = "/users/{}/page_views" #user_id
urlStudentSummaries = "/courses/{}/analytics/student_summaries" #param: courseId, return tardiness_breakdown, on time, missing, late
urlDiscussions = "/courses/{}/discussion_topics"
urlDiscussionView = "/courses/{}/discussion_topics/{}/view" #courseId, discussionId
urlEntries = "/courses/{}/discussion_topics/{}/entries"
urlEntryRelies = "/courses/{}/discussion_topics/{}/entries/{}/replies"
urlGetAnAssignment = "/courses/{}/assignments/{}" #courseId, assignmentId
urlGetATopic = "/courses/{}/discussion_topics/{}" #courseId, topicId
urlGetAFile = "/files/{}" #fileId
urlGetAQuiz = "/courses/{}/quizzes/{}" #courseId, quizId
urlGetAModule = "/courses/{}/modules/{}" # courseId, moduleItemId, unused
urlGetAllQuizzes = "/courses/{}/quizzes" # courseId, unused
urlGetQuizSubmission = "/courses/{}/quizzes/{}/submissions" # courseId, quizId, replaced by urlAssignmentSubmissions, unused


def getAnalyticsAssignments(courseId, studentId):
    return open_connection_2params(urlAnalyticsAssignments, courseId, studentId)

def getListofAssignments(courseId):
    return open_connection_param(urlListofAssignments, courseId)

def getAssignmentSubmissions(courseId, assignmentId):
    return open_connection_2params(urlAssignmentSubmissions, courseId, assignmentId)

def getStudents(courseId):
    return open_connection_param(urlStudents, courseId)

def getActivities(courseId, studentId):
    return open_connection_2params(urlActivities, courseId, studentId)

def getPageView(studentId):
    return open_connection_param(urlPageView, studentId)
    
def getStudentSummaries(courseId):
    return open_connection_param(urlStudentSummaries, courseId)

def getDiscussions (courseId):
    return open_connection_param(urlDiscussions, courseId)

def getDiscussionView (courseId, topicId):
    return open_connection_2params(urlDiscussionView, courseId, topicId)

def getEntries(courseId, topicId):
    return open_connection_2params(urlEntries, courseId, topicId)

def getEntryReplies(courseId, topicId, entryId):
    return open_connection_3params(urlEntryRelies, courseId, topicId, entryId)

def getAnAssignment(courseId, assignmentId):
    return open_connection_2params(urlGetAnAssignment, courseId, assignmentId)

def getATopic(courseId, discussionId):
    return open_connection_2params(urlGetATopic, courseId, discussionId)

def getAFile(fileId):
    return open_connection_param(urlGetAFile, fileId)

def getAQuiz(courseId, quizId):
    return open_connection_2params(urlGetAQuiz, courseId, quizId)

def getAModuleItem(courseId, moduleItemId):
    return open_connection_2params(urlGetAModule, courseId, moduleItemId)

def getAllQuizzes(courseId):
    return open_connection_param(urlGetAllQuizzes, courseId)

def getQuizSubmission(courseId, quizId):
    return open_connection_2params(urlGetQuizSubmission, courseId, quizId)
    
