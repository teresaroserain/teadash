import re
import src.utils.transactions as transactions

def findString(searchString, text):
    pos = re.search(searchString, text)
    if pos != None:
        find_quizId = text[pos.end()+1:]
        """  print("id ", find_quizId) """
        pos = find_quizId.find("/")
        """  print("pos ", pos) """
        return find_quizId[:pos] if pos != -1 else find_quizId[:len(find_quizId)+1]

def findString_pages(searchString, text):
    pos = re.search(searchString, text)
    if pos != None:
        find_quizId = text[pos.end()+1:]
        """  print("id ", find_quizId) """
        pos = find_quizId.find("?")
        """  print("pos ", pos) """
        return find_quizId[:pos] if pos != -1 else find_quizId[:len(find_quizId)+1]
    

def call_APIs(course):
    print("call API....")
    if course != None:
        print("Working on courseId {}".format(course['CourseId']))
        df_interaction, df_discussionparticipation = transactions.get_interactions_discussionview(course)
        #df_pageviews = transactions.get_pageviews(course)
        df_analyticsassignments = transactions.get_analyticsassignments(course)
        #df_participation = transactions.get_participations(course)
        load_data(df_analyticsassignments, df_discussionparticipation)
        #return df_interaction,df_discussionparticipation,df_pageviews,df_analyticsassignments,df_participation
        return df_analyticsassignments, df_discussionparticipation
    else:
        print("khong vo dung")
        return None
            

def load_data(df_analyticsassignments, df_discussionparticipation):
    """ global assgn
    global optstatus
    global quizzes 
    global discussions  """
    print("vo load data ")
    assgn = [{'label' : i, 'value' : j} for i, j in zip(df_analyticsassignments.iloc[:,6].unique(), df_analyticsassignments.iloc[:,5].unique())] 
    print("dd value ", assgn)
    optstatus = [{'label' : i, 'value' : j} for i, j in zip(df_analyticsassignments.iloc[:,9].unique(), df_analyticsassignments.iloc[:,9].unique())] 
    print("dd optstatus ", optstatus)
    discussions = [{'label' : i, 'value' : j} for i, j in zip(df_discussionparticipation.iloc[:,6].unique(), df_discussionparticipation.iloc[:,5].unique())] 
    df_temp = df_analyticsassignments[df_analyticsassignments.IsQuiz==1]
    quizzes = [{'label' : i, 'value' : j} for i, j in zip(df_temp.iloc[:,6].unique(), df_temp.iloc[:,5].unique())] 
    return assgn, optstatus, quizzes, discussions