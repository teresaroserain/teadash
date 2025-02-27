import pandas as pd
from pandasql import sqldf
import os.path as Path
import os

# ======= Init =======
mysql = lambda q: sqldf(q, globals())

def sql_studentparticipation(df_analyticsassignments):
    df = pd.DataFrame(sqldf("SELECT Title, Status, count(distinct StudentId) as 'CountStudent', count(distinct StudentId)*100.0/(SELECT COUNT(DISTINCT StudentId) FROM df_analyticsassignments) as 'RateStudent' from df_analyticsassignments group by Title, Status"))
    return df

def sql_studentparticipationHV(df_analyticsassignments):
    df = pd.DataFrame(sqldf("SELECT Title, count(distinct StudentId) as 'CountStudent', count(distinct StudentId)*100.0/(SELECT COUNT(DISTINCT StudentId) FROM df_analyticsassignments) as 'RateStudent' from df_analyticsassignments group by Title"))
    return df

def sql_filterbybarchart(df_analyticsassignments, title, status):
    df = pd.DataFrame(sqldf("SELECT StudentId, StudentName, Title, Status from df_analyticsassignments WHERE Title = '" + title + "' and Status = '" + status +"'"))
    return df

def sql_filterbetweenassignments(df_analyticsassignments, assign1Id, assign2Id, status):
    df = pd.DataFrame(sqldf("SELECT DISTINCT(StudentId), StudentName, Title, Status FROM (SELECT * FROM df_analyticsassignments WHERE AssignmentId = '" + str(assign1Id) + "' and Status = '" + status +"' and StudentId NOT IN (SELECT StudentId FROM df_analyticsassignments WHERE AssignmentId = '" + str(assign2Id) + "' and Status = '" + status + "'))"))
    return df

def sql_filterstudentsbynetwork(df_analyticsassignments, students):
    #print("sql ", 'SELECT * FROM df_analyticsassignments WHERE StudentId IN (' + ",".join((str(n) for n in students)) + ')')
    #Show student name
    #df = pd.DataFrame(sqldf("SELECT Title, StudentName, Status FROM df_analyticsassignments WHERE StudentName IN (%s)" % ('"'+'", "'.join(students)+'"')))
    
    #Show Student Id
    df = pd.DataFrame(sqldf("SELECT Title, StudentId, Status FROM df_analyticsassignments WHERE StudentId IN (%s)" % ('"'+'", "'.join(students)+'"')))

    return df

def sql_countposts(df_interaction):
    df1 = pd.DataFrame(sqldf("SELECT DISTINCT(StudentName) FROM (SELECT temp1.Source as StudentName FROM (SELECT Source FROM df_interaction) as temp1 LEFT JOIN (SELECT Target FROM df_interaction) as temp2 ON temp1.Source = temp2.Target UNION ALL SELECT temp2.Target as StudentName FROM (SELECT Target FROM df_interaction) as temp2 LEFT JOIN (SELECT Source FROM df_interaction) as temp1 ON temp2.Target = temp1.Source) WHERE StudentName <> 'None' and StudentName <> 'Test student'"))
    print("check post df1 ", df1)
    df2 = pd.DataFrame(sqldf("SELECT DISTINCT df1.StudentName, COUNT(A.Source) AS Entries FROM df_interaction A JOIN df1 ON A.Source = df1.StudentName GROUP BY df1.StudentName"))
    print("check post df2 ", df2)
    df3 = pd.DataFrame(sqldf("SELECT DISTINCT df1.StudentName, COUNT(A.Target) AS Replies FROM df_interaction A JOIN df1 ON A.Target = df1.StudentName GROUP BY df1.StudentName"))
    print("check post df3 ", df3)
    temp1 = pd.DataFrame(sqldf("SELECT df1.StudentName, df2.Entries FROM df1 LEFT JOIN df2 USING(StudentName) UNION ALL SELECT df1.StudentName, df2.Entries FROM df2 LEFT JOIN df1 USING(StudentName) WHERE df1.StudentName IS NULL ")) #and df1.StudentName <> 'Test student'
    temp2 = pd.DataFrame(sqldf("SELECT df1.StudentName, df3.Replies FROM df1 LEFT JOIN df3 USING(StudentName) UNION ALL SELECT df1.StudentName, df3.Replies FROM df3 LEFT JOIN df1 USING(StudentName) WHERE df1.StudentName IS NULL ")) #and df1.StudentName <> 'Test student'
    df4 = pd.DataFrame(sqldf("SELECT temp1.StudentName, temp1.Entries, temp2.Replies FROM temp1 LEFT JOIN temp2 USING (StudentName) UNION ALL SELECT temp1.StudentName, temp1.Entries, temp2.Replies FROM temp2 LEFT JOIN temp1 USING (StudentName) WHERE temp1.StudentName IS NULL ")) #and temp1.StudentName <> 'Test student' and temp2.StudentName <> 'Test student'
    df4 = df4.fillna(0)
    print("check post df4 ", df4)
    return df4 

def sql_filtertblcountpostbynetwork(df_interaction, students):
    df = sql_countposts(df_interaction)
    #print("sql ", 'SELECT * FROM df_analyticsassignments WHERE StudentId IN (' + ",".join((str(n) for n in students)) + ')')
    df1 = pd.DataFrame(sqldf("SELECT * FROM df WHERE StudentName IN (%s)" % ('"'+'", "'.join(students)+'"')))
    return df1


def sql_dsforprediction(df_discussionparticipation, discussionId, df_interaction, df_analyticsassignments, quizId, targetId):
    df1 = pd.DataFrame(sqldf("SELECT StudentId, StudentName, '1' as 'ParticipatedDiscussion' FROM df_discussionparticipation WHERE AssignmentId = '" + str(discussionId) +"'"))
    #df1.to_csv(os.path.join(Path.abspath(Path.join(__file__ ,"../../.."))+'/Datasets/df1.csv'), sep=';', index=False, encoding='utf-8' )
    df2 = sql_countposts(df_interaction)
    df3 = pd.DataFrame(sqldf("SELECT StudentName, (Entries + Replies) as 'Posts' FROM df2"))
    df_tempt = df_analyticsassignments[df_analyticsassignments.IsQuiz==1]
    df4 = pd.DataFrame(sqldf("SELECT StudentId, StudentName, '1' AS 'ParticipatedQuiz' FROM df_tempt WHERE AssignmentId = '" + str(quizId) + "' AND Status = 'on_time' OR Status = 'late'"))
    df5 = pd.DataFrame(sqldf("SELECT StudentId, StudentName, CASE WHEN Status = 'on_time' THEN 1 WHEN Status = 'late' THEN 1 WHEN Status = 'floating' THEN 0 ELSE 0 END AS 'ParticipateInTarget' FROM df_analyticsassignments WHERE AssignmentId = '" + str(targetId) + "'"))
    df6 = pd.DataFrame(sqldf("SELECT DISTINCT(StudentId), StudentName FROM df_analyticsassignments"))   

    # =========== replace full outer join ============
    df7 = pd.DataFrame(sqldf("SELECT df6.StudentId, df6.StudentName, df1.ParticipatedDiscussion FROM df6 LEFT JOIN df1 USING(StudentId) UNION ALL SELECT df6.StudentId, df6.StudentName, df1.ParticipatedDiscussion FROM df1 LEFT JOIN df6 USING(StudentId) WHERE df6.StudentId IS NULL")) 
    df8 = pd.DataFrame(sqldf("SELECT df6.StudentId, df6.StudentName, df4.ParticipatedQuiz FROM df6 LEFT JOIN df4 USING(StudentId) UNION ALL SELECT df6.StudentId, df6.StudentName, df4.ParticipatedQuiz FROM df4 LEFT JOIN df6 USING(StudentId) WHERE df6.StudentId IS NULL"))
    df9 = pd.DataFrame(sqldf("SELECT df6.StudentId, df6.StudentName, df5.ParticipateInTarget FROM df6 LEFT JOIN df5 USING(StudentId) UNION ALL SELECT df6.StudentId, df6.StudentName, df5.ParticipateInTarget FROM df5 LEFT JOIN df6 USING(StudentId) WHERE df6.StudentId IS NULL"))
    df10 = pd.DataFrame(sqldf("SELECT df6.StudentId, df6.StudentName, df3.Posts FROM df6 LEFT JOIN df3 USING(StudentName) UNION ALL SELECT df6.StudentId, df6.StudentName, df3.Posts FROM df3 LEFT JOIN df6 USING(StudentName) WHERE df6.StudentId IS NULL"))

    df11 = pd.DataFrame(sqldf("SELECT df10.StudentId, df10.StudentName, df10.Posts, df7.ParticipatedDiscussion FROM df10 LEFT JOIN df7 USING(StudentId) UNION ALL SELECT df10.StudentId, df10.StudentName, df10.Posts, df7.ParticipatedDiscussion FROM df7 LEFT JOIN df10 USING(StudentId) WHERE df10.StudentId IS NULL"))
    df12 = pd.DataFrame(sqldf("SELECT df8.StudentId, df8.StudentName, df8.ParticipatedQuiz, df9.ParticipateInTarget FROM df8 LEFT JOIN df9 USING(StudentId) UNION ALL SELECT df8.StudentId, df8.StudentName, df8.ParticipatedQuiz, df9.ParticipateInTarget FROM df9 LEFT JOIN df8 USING(StudentId) WHERE df8.StudentId IS NULL"))
    df = pd.DataFrame(sqldf("SELECT DISTINCT(StudentId), StudentName, ParticipatedDiscussion, Posts, ParticipatedQuiz, ParticipateInTarget FROM (SELECT df11.StudentId, df11.StudentName, df11.ParticipatedDiscussion, df11.Posts, df12.ParticipatedQuiz, df12.ParticipateInTarget FROM df11 LEFT JOIN df12 USING(StudentId) UNION ALL SELECT df11.StudentId, df11.StudentName, df11.ParticipatedDiscussion, df11.Posts, df12.ParticipatedQuiz, df12.ParticipateInTarget FROM df12 LEFT JOIN df11 USING(StudentId) WHERE df11.StudentId IS NULL and df11.StudentName <> 'Test student') WHERE StudentName <> '0'"))
    df = df.fillna(0)
    return df

def sql_quizsubmissions(df_quizsubmissions): #unused
    df_quiz = pd.DataFrame(sqldf("SELECT StudentId, Title, Attempts, Grade, CASE WHEN (Late is True AND Missing is False) THEN CASE WHEN (Late is True and Missing is True) THEN 'Late Missing' ELSE 'Late' END ELSE CASE WHEN (Late is False AND Missing is True) THEN 'Missing' ELSE 'Not late not missing' END END AS 'Status' from df_quizsubmissions"))
    return df_quiz

def sql_accessbydate(df_pageviews): 
    df_accessbydate = pd.DataFrame(sqldf("SELECT DATE(AccessedDate) as 'Date', sum(ViewCount) as 'SumView', count(distinct StudentId) as 'CountStudent' from df_pageviews group by Date")) 
    return df_accessbydate

def sql_accessbyhour(df_pageviews): #unused
    df_accessbyhour = pd.DataFrame(sqldf("SELECT DATE(AccessedDate) as 'Date', sum(ViewCount) as 'SumView', count(distinct StudentId) as 'CountStudent' from df_pageviews group by Date")) 
    return df_accessbyhour

def sql_accessbyweekday(df_pageviews): #unused
    df_accessbyweekday = pd.DataFrame(sqldf("SELECT DATE(AccessedDate) as 'Date', sum(ViewCount) as 'SumView', count(distinct StudentId) as 'CountStudent' from df_pageviews group by Date")) 
    return df_accessbyweekday