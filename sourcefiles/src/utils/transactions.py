import pandas as pd
import src.utils.APIs as apis
import src.utils.functions as functions
import os
import os.path as Path

# ======= urlStudentSummaries =======
df_studentsummaries = pd.DataFrame({
            'CourseId':[],
            'CourseCode':[],
            'CourseName':[],
            'StudentId':[],
            'Page_Views':[], 
            'Participations':[],
            'breakdown_total':[],
            'breakdown_on_time':[], 
            'breakdown_late': [],
            'breakdown_missing': [], 
            'breakdown_floating': []   
        }, dtype = object)

 # ======= urlDiscussions =======
""" df_discussions = pd.DataFrame({
            'CourseId':[],
            'CourseCode':[],
            'CourseName':[],
            'TopicId':[],
            'Title':[],
            #'TopicUserId':[],
            #'TopicUserName':[],
            'EntryId':[],
            'EntryUserId':[],
            'EntryUserName':[],
            'ReplyId':[],
            'ReplyUserId':[],
            'ReplyUserName':[],
            'Message':[],
        }, dtype=object) """

# ======= extra DataFrame Interaction from UrlDiscussions =======
""" df_interaction = pd.DataFrame({
            'Source':[],
            'Target':[],
            }, dtype=object) """

# ======= urlDiscussionView ======= # only participants without status
""" df_discussionsparticipation = pd.DataFrame({
            'CourseId':[],
            'CourseCode':[],
            'CourseName':[],
            'StudentId':[],
            'StudentName':[],
            'AssignmentId':[],
            'Title':[],
        }, dtype=object) """

# ======= urlAnalyticsAssignments =======
""" df_analyticsassignments = pd.DataFrame({
            'CourseId':[],
            'CourseCode':[],
            'CourseName':[],
            'StudentId':[],
            'StudentName':[],
            'AssignmentId':[],
            'Title':[],
            'DueAt':[],
            'SubmittedAt':[],
            'Status':[],
            'IsQuiz':[],
        }, dtype=object) """
df_analyticsquiz = pd.DataFrame()
df_analyticsotherassignments = pd.DataFrame()

# ======= urlAssignmentSubmissions - filter Quiz =======
df_quizsubmissions = pd.DataFrame({
            'CourseId':[],
            'CourseCode':[],
            'CourseName':[],
            'StudentId':[],
            'AssignmentId':[],
            'Title':[],
            'Late':[],
            'Missing': [],
            'Grade': [],
            'Attempts': []
        }, dtype=object)

# ======= urlAssignmentSubmissions - filter others ======= #unused
df_assignmentsubmissions = pd.DataFrame({
            'CourseId':[],
            'CourseCode':[],
            'CourseName':[],
            'StudentId':[],
            'AssignmentId':[],
            'Title':[],
            'Grade':[],
        }, dtype=object)

# ======= urlActivities =======
df_participation = pd.DataFrame({
            'CourseId':[],
            'CourseCode':[],
            'CourseName':[],
            'StudentId':[],
            'Sis_User_Id':[],
            'Date':[],
            'Url':[],
            'Type': [],
            'ItemId': [],
            'Title': [],
        }, dtype=object)

# ======= urlActivities =======
""" df_pageviews = pd.DataFrame({
            'CourseId':[],
            'CourseCode':[],
            'CourseName':[],
            'StudentId':[],
            'Sis_User_Id':[],
            'AccessedDate':[],
            'ViewCount':[]
        }, dtype=object) """




# ======= DataFrame StudentSummaries =======
def get_studentsummaries(course):
    studentsummaries = apis.getStudentSummaries(course["CourseId"])
    #print("next   ", studentsummaries)
    for i in range(len(studentsummaries)):
        df_studentsummaries.loc[len(df_studentsummaries.index)] = [course["CourseId"], course["CourseCode"], course["CourseName"], 
                                                                    studentsummaries[i]["id"], studentsummaries[i]["page_views"],
                                                                    studentsummaries[i]["participations"], studentsummaries[i]["tardiness_breakdown"]["total"], 
                                                                    studentsummaries[i]["tardiness_breakdown"]["on_time"], 
                                                                    studentsummaries[i]["tardiness_breakdown"]["late"], studentsummaries[i]["tardiness_breakdown"]["missing"],
                                                                    studentsummaries[i]["tardiness_breakdown"]["floating"]]
    #print("summaries ", df_studentsummaries)
    return df_studentsummaries

# ======= DataFrame Discussions =======
def get_discussions(course):
    df_discussions = pd.DataFrame({
            'CourseId':[],
            'CourseCode':[],
            'CourseName':[],
            'TopicId':[],
            'Title':[],
            #'TopicUserId':[],
            #'TopicUserName':[],
            'EntryId':[],
            'EntryUserId':[],
            'EntryUserName':[],
            'ReplyId':[],
            'ReplyUserId':[],
            'ReplyUserName':[],
            'Message':[],
        }, dtype=object)
    topics = apis.getDiscussions(course["CourseId"])
    #print("result ", topics[0]["id"])
    for i in range(len(topics)):
        df_discussions.loc[len(df_discussions.index)] = [course["CourseId"], course["CourseCode"], course["CourseName"], 
                                                         topics[i]["id"], topics[i]["title"], 
                                                        #topics[i]["author"]["id"], topics[i]["author"]["display_name"], 
                                                        "", "", "", "", "", "", topics[i]["message"]]
        #print ("discussions ", df_discussions)
        entries = apis.getEntries(course["CourseId"], topics[i]["id"])
        for j in range(len(entries)):
            #print("entry list  ", entries[j]["id"])
            df_discussions.loc[len(df_discussions.index)] = [course["CourseId"], course["CourseCode"], course["CourseName"], 
                                                             topics[i]["id"], topics[i]["title"],  #topics[i]["author"]["id"], topics[i]["author"]["display_name"], 
                                                        entries[j]["id"], entries[j]["user_id"], entries[j]["user_name"],
                                                        "", "", "", entries[j]["message"]]
            replies = apis.getEntryReplies(course["CourseId"], topics[i]["id"], entries[j]["id"])
            #print("replies: ", replies)
            for z in range(len(replies)):
                df_discussions.loc[len(df_discussions.index)] = [course["CourseId"], course["CourseCode"], course["CourseName"], 
                                                                 topics[i]["id"], topics[i]["title"],
                                                            #topics[i]["author"]["id"], topics[i]["author"]["display_name"], 
                                                            entries[j]["id"], entries[j]["user_id"], 
                                                            entries[j]["user_name"], replies[z]["id"], 
                                                            replies[z]["user_id"], replies[z]["user_name"], replies[z]["message"]]
    df_discussions.to_csv(os.path.join(Path.abspath(Path.join(__file__ ,"../../.."))+'/Datasets/df_discussions_'+ str(course["CourseId"]) +'.csv'), sep=';', index=False, encoding='utf-8', header=True, mode='w')
    return df_discussions

# ======= DataFrame Interaction and Discussion View =======
def get_interactions_discussionview(course):
    df_interaction = pd.DataFrame({
            'Source':[],
            'Target':[],
            }, dtype=object)
    df_discussionsparticipation = pd.DataFrame({
            'CourseId':[],
            'CourseCode':[],
            'CourseName':[],
            'StudentId':[],
            'StudentName':[],
            'AssignmentId':[],
            'Title':[],
        }, dtype=object)
    df_discussions = get_discussions(course)
    for x, row in df_discussions.iterrows():
        #df_interaction.loc[len(df_interaction.index)] = [str(row["TopicUserName"]), str(row["EntryUserName"])]
        df_interaction.loc[len(df_interaction.index)] = [str(row["EntryUserName"]), str(row["ReplyUserName"])]
        #df_interaction.loc[len(df_interaction.index)] = [str(row["EntryUserId"]), str(row["ReplyUserId"])]
    df_temp =df_discussions[['TopicId', 'Title']]
    df_temp = df_temp.drop_duplicates()
    print("df unique ", df_temp)
    for x, row in df_temp.iterrows():
        print("df x ", row['TopicId'])
        participants = apis.getDiscussionView(course["CourseId"], row['TopicId'])
        #print("participants ", participants)
        for i in range(len(participants['participants'])):
            print("node con ", participants['participants'][i]['id'])
            df_discussionsparticipation.loc[len(df_discussionsparticipation.index)] = [course["CourseId"], course["CourseCode"], course["CourseName"], 
                                                                                    participants['participants'][i]['id'], participants['participants'][i]['display_name'], 
                                                                                    row['TopicId'], row['Title']]
    df_interaction.to_csv(os.path.join(Path.abspath(Path.join(__file__ ,"../../.."))+'/Datasets/interaction_'+ str(course["CourseId"]) +'.csv'), sep=';', index=False, encoding='utf-8', header=True, mode='w')
    df_discussionsparticipation.to_csv(os.path.join(Path.abspath(Path.join(__file__ ,"../../.."))+'/Datasets/discussionparticipation_'+ str(course["CourseId"]) +'.csv'), sep=';', index=False, encoding='utf-8', header=True, mode='w')

    return df_interaction, df_discussionsparticipation

# ======= DataFrame Students =======
def get_students(course):
    students = apis.getStudents(course["CourseId"])
    return students

# ======= DataFrame Analytics Assignments =======
def get_analyticsassignments(course):
    df_analyticsassignments = pd.DataFrame({
            'CourseId':[],
            'CourseCode':[],
            'CourseName':[],
            'StudentId':[],
            'StudentName':[],
            'AssignmentId':[],
            'Title':[],
            'DueAt':[],
            'SubmittedAt':[],
            'Status':[],
            'IsQuiz':[],
        }, dtype=object)
    students = get_students(course)
    for i in range(len(students)):
        assignments = apis.getAnalyticsAssignments(course["CourseId"], students[i]["id"])
        for j in range(len(assignments)):
            if assignments[j]["title"].find('Quiz') >= 0:
                df_analyticsassignments.loc[len(df_analyticsassignments.index)] = [course["CourseId"], course["CourseCode"], 
                                                        course["CourseName"], students[i]["id"], students[i]["name"], 
                                                        assignments[j]["assignment_id"], assignments[j]["title"], assignments[j]['due_at'],
                                                        assignments[j]['submission']['submitted_at'], assignments[j]['status'], 1]
            else:
                df_analyticsassignments.loc[len(df_analyticsassignments.index)] = [course["CourseId"], course["CourseCode"], 
                                                        course["CourseName"], students[i]["id"], students[i]["name"], 
                                                        assignments[j]["assignment_id"], assignments[j]["title"], assignments[j]['due_at'],
                                                        assignments[j]['submission']['submitted_at'], assignments[j]['status'], 0]
            
    df_analyticsassignments.to_csv(os.path.join(Path.abspath(Path.join(__file__ ,"../../.."))+'/Datasets/analyticsassignments_'+ str(course["CourseId"]) +'.csv'), sep=';', index=False, encoding='utf-8', header=True, mode='w')
    return df_analyticsassignments

# ======= DataFrame List of Assignments =======
def get_listofassignments(course):
    listofassignments = apis.getListofAssignments(course["CourseId"])
    return listofassignments

# ======= DataFrame Quiz Submissions ======= khong dung
def get_quizsubmissions(course):
    #print("vo day ", course["CourseId"])
    listofassignments = get_listofassignments(course)
    #print("list of assignments ", listofassignments)
    for i in range(len(listofassignments)):
        #print("vo 2")
        assignmentsubmissions = apis.getAssignmentSubmissions(course["CourseId"], listofassignments[i]["id"])
        #print("assignmentsubmissions ", assignmentsubmissions)
        for j in range(len(assignmentsubmissions)):
            if listofassignments[i]["name"].find('Quiz') >= 0:
                df_quizsubmissions.loc[len(df_quizsubmissions.index)] = [course["CourseId"], course["CourseCode"], 
                                                        course["CourseName"], assignmentsubmissions[j]["user_id"], listofassignments[i]["id"], 
                                                        listofassignments[i]["name"], assignmentsubmissions[j]["late"],
                                                        assignmentsubmissions[j]["missing"], assignmentsubmissions[j]["grade"],
                                                        assignmentsubmissions[j]["attempt"]]
    df_quizsubmissions.to_csv(os.path.join(Path.abspath(Path.join(__file__ ,"../../.."))+'/Datasets/quizsubmissions_'+ str(course["CourseId"]) +'.csv'), sep=';', index=False, encoding='utf-8', header=True, mode='w')
    return df_quizsubmissions


# ======= DataFrame Participation =======
def get_participations(course):
    students = get_students(course)
    if len(df_participation.index) == 0:
        for i in range(len(students)):
            pageViews = apis.getActivities(course["CourseId"], students[i]["id"])
            if len(pageViews["participations"]) != 0:
                participations = pd.DataFrame.from_dict(pageViews["participations"])
                #print("pageViews  ", students[i]["id"], '     ', pageViews)
                #print("type participations ", type(participations))
                if len(participations.index) != 0:
                    #print("student id ", students[i]['id'])
                    for x, row in participations.iterrows():
                        #print("test ", participations["created_at"][x])
                        #print(str(row["url"]))
                        if str(row["url"]).find('assignment') >= 0:
                            participation_type = "Assignment"
                            find_assignmentId = functions.findString("assignments", str(row["url"]))
                            an_assignment = apis.getAnAssignment(course["CourseId"], find_assignmentId)
                            df_participation.loc[len(df_participation.index)] = [course["CourseId"], course["CourseCode"],
                                                                            course["CourseName"], students[i]["id"], students[i]["sis_user_id"],
                                                                            row["created_at"], row["url"], participation_type, find_assignmentId, an_assignment["name"]]
                        elif str(row["url"]).find('topics') >= 0:
                            participation_type = "Discussion"
                            find_discussionId = functions.findString("topics", str(row["url"]))
                            a_topic = apis.getATopic(course["CourseId"], find_discussionId)
                            df_participation.loc[len(df_participation.index)] = [course["CourseId"], course["CourseCode"],
                                                                            course["CourseName"], students[i]["id"], students[i]["sis_user_id"],
                                                                            row["created_at"], row["url"], participation_type, find_discussionId, a_topic["title"]]
                        elif str(row["url"]).find('quiz') >= 0:
                            participation_type = "Quiz"
                            find_quizId = functions.findString("quizzes", str(row["url"]))
                            a_quiz = apis.getAQuiz(course["CourseId"], find_quizId)
                            df_participation.loc[len(df_participation.index)] = [course["CourseId"], course["CourseCode"],
                                                                            course["CourseName"], students[i]["id"], students[i]["sis_user_id"],
                                                                            row["created_at"], row["url"], participation_type, find_quizId, a_quiz["title"]]
                        elif str(row["url"]).find('file') >= 0:
                            participation_type = "File"
                            find_fileId = functions.findString("files", str(row["url"]))
                            a_file = apis.getAFile(find_fileId)
                            df_participation.loc[len(df_participation.index)] = [course["CourseId"], course["CourseCode"],
                                                                            course["CourseName"], students[i]["id"], students[i]["sis_user_id"],
                                                                            row["created_at"], row["url"], participation_type, find_fileId, a_file["display_name"]]
                    
        df_participation.to_csv(os.path.join(Path.abspath(Path.join(__file__ ,"../../.."))+'/Datasets/participation_'+ str(course["CourseId"]) +'.csv'), sep=';', index=False, encoding='utf-8', header=True, mode='w')
    return df_participation

# ======= DataFrame PageView =======
def get_pageviews(course):
    df_pageviews = pd.DataFrame({
            'CourseId':[],
            'CourseCode':[],
            'CourseName':[],
            'StudentId':[],
            'Sis_User_Id':[],
            'AccessedDate':[],
            'ViewCount':[]
        }, dtype=object)
    students = get_students(course)
    for i in range(len(students)):
        pageViews = apis.getActivities(course["CourseId"], students[i]["id"])
        for k in range(len(pageViews)):
            df_subpageviews = pd.DataFrame([(k, val) for k, val in pageViews["page_views"].items()], columns=['date', 'pageview'])
            for x in range(len(df_subpageviews)):
                df_pageviews.loc[len(df_pageviews.index)] = [course["CourseId"], course["CourseCode"],
                                                            course["CourseName"], students[i]["id"], students[i]["sis_user_id"],
                                                            df_subpageviews["date"][x], df_subpageviews["pageview"][x]]
    df_pageviews.to_csv(os.path.join(Path.abspath(Path.join(__file__ ,"../../.."))+'/Datasets/df_pageviews_'+ str(course["CourseId"]) +'.csv'), sep=';', index=False, encoding='utf-8', header=True, mode='w')
    return df_pageviews

# ======= DataFrame User Activities =======
def get_useractivities(course):
    # ======= urlPageView =======
    df_useractivity = pd.DataFrame({
                'StudentId':[],
                'StudentName':[],
                'Sis_User_Id':[],
                'Url':[],
                'Asset_Type':[], 
                'Interaction_Seconds':[],
                'Created_At':[],
                'Participated':[],
                'Type': [],
                'ItemId':[],
                'Title': [],    
            }, dtype = object)
    students = get_students(course)
    for i in range(len(students)):
        useractivities = apis.getPageView(students[i]["id"])
        print("user activities ", useractivities, type(useractivities))
        # print("user activities ", useractivities[0]["status"])
        if isinstance(useractivities, list) == True: # not useractivities.get("status", "unauthorized"): 
            #print("url ", useractivities[0]["url"])
            for l in range(len(useractivities)):
                text_index = str(useractivities[l]["url"]).find(str(course["CourseId"]))
                if text_index >= 0:
                    if str(useractivities[l]["url"]).find('assignment') >= 0:
                        activity_type = "Assignment"
                        print("assignment .......", str(useractivities[l]["url"]))
                        find_assignmentId = functions.findString("assignments", str(useractivities[l]["url"]))
                        
                        """print ("id 1 : ", find_assignmentId) """
                        if find_assignmentId != '':
                            an_assignment = apis.getAnAssignment(course["CourseId"], find_assignmentId)
                            print("assignment .......", an_assignment)
                            if not an_assignment.get("errors"):
                                df_useractivity.loc[len(df_useractivity.index)] = [students[i]["id"], students[i]["name"], students[i]["sis_user_id"], useractivities[l]["url"],
                                                                        useractivities[l]["asset_type"], useractivities[l]["interaction_seconds"], 
                                                                        useractivities[l]["created_at"], useractivities[l]["participated"], activity_type, find_assignmentId,an_assignment["name"]]
                    elif str(useractivities[l]["url"]).find('topics') >= 0:
                        activity_type = "Discussion"
                        find_discussionId = functions.findString("topics", str(useractivities[l]["url"]))
                        """ print("url ", useractivities[l]["url"])
                        print ("id 2 : ", find_discussionId) """
                        if find_discussionId != '':
                            a_topic = apis.getATopic(course["CourseId"], find_discussionId)
                            df_useractivity.loc[len(df_useractivity.index)] = [students[i]["id"], students[i]["name"], students[i]["sis_user_id"], useractivities[l]["url"],
                                                                    useractivities[l]["asset_type"], useractivities[l]["interaction_seconds"], 
                                                                    useractivities[l]["created_at"], useractivities[l]["participated"], activity_type, find_discussionId ,a_topic["title"]]
                    elif str(useractivities[l]["url"]).find('quiz') >= 0:
                        activity_type = "Quiz"
                        find_quizId = functions.findString("quizzes", str(useractivities[l]["url"]))
                        """ print("url ", useractivities[l]["url"])
                        print ("id 3 : ", find_quizId) """
                        if find_quizId != '':
                            a_quiz = apis.getAQuiz(course["CourseId"], find_quizId)
                            df_useractivity.loc[len(df_useractivity.index)] = [students[i]["id"], students[i]["name"], students[i]["sis_user_id"], useractivities[l]["url"],
                                                                    useractivities[l]["asset_type"], useractivities[l]["interaction_seconds"], 
                                                                    useractivities[l]["created_at"], useractivities[l]["participated"], activity_type, find_quizId, a_quiz["title"]]
                    elif str(useractivities[l]["url"]).find('file') >= 0:
                        activity_type = "File"
                        find_fileId = functions.findString("files", str(useractivities[l]["url"]))
                        """ print("url ", useractivities[l]["url"])
                        print ("id 4 : ", find_fileId) """
                        if find_fileId != '':
                            a_file = apis.getAFile(find_fileId)
                            df_useractivity.loc[len(df_useractivity.index)] = [students[i]["id"], students[i]["name"], students[i]["sis_user_id"], useractivities[l]["url"],
                                                                    useractivities[l]["asset_type"], useractivities[l]["interaction_seconds"], 
                                                                    useractivities[l]["created_at"], useractivities[l]["participated"], activity_type, find_fileId, a_file["display_name"]]
                    elif str(useractivities[l]["url"]).find('pages') >= 0:
                        activity_type = "Pages"
                        find_pagename = functions.findString_pages("pages", str(useractivities[l]["url"]))
                        if find_pagename != '':
                            df_useractivity.loc[len(df_useractivity.index)] = [students[i]["id"], students[i]["name"], students[i]["sis_user_id"], useractivities[l]["url"],
                                                                    useractivities[l]["asset_type"], useractivities[l]["interaction_seconds"], 
                                                                    useractivities[l]["created_at"], useractivities[l]["participated"], useractivities[l]["controller"], find_pagename, find_pagename]
                    elif str(useractivities[l]["url"]).find('syllabus') >= 0:
                        activity_type = "Syllabus"
                        df_useractivity.loc[len(df_useractivity.index)] = [students[i]["id"], students[i]["name"], students[i]["sis_user_id"], useractivities[l]["url"],
                                                                useractivities[l]["asset_type"], useractivities[l]["interaction_seconds"], 
                                                                useractivities[l]["created_at"], useractivities[l]["participated"], useractivities[l]["controller"], 'NA', useractivities[l]["action"]]
                    else: #including calendar, announcements, syllabus, conversations, grades
                        df_useractivity.loc[len(df_useractivity.index)] = [students[i]["id"], students[i]["name"], students[i]["sis_user_id"], useractivities[l]["url"],
                                                                useractivities[l]["asset_type"], useractivities[l]["interaction_seconds"], 
                                                                useractivities[l]["created_at"], useractivities[l]["participated"], useractivities[l]["controller"], 'NA', useractivities[l]["action"]] 
                        print("url ", useractivities[l]["url"])
    df_useractivity.to_csv(os.path.join(Path.abspath(Path.join(__file__ ,"../../.."))+'/Datasets/useractivity_'+ str(course["CourseId"]) +'.csv'), sep=';', index=False, encoding='utf-8', header=True, mode='w')
    return df_useractivity


