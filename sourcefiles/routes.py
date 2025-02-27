from flask import render_template, request
from sourcefiles.callAPI2 import app

@app.server.route('/TEADASH?courseid=<courseid>')
def login(courseid):
    print("vo day roi", courseid)
    """ df_courses = pd.DataFrame({
        'CourseId':[],
        'CourseCode':[],
        'CourseName':[], 
    }, dtype = object) """
    #df_courses.loc[len(df_courses.index)] = [int(courseid), '', '']
    
    """ if (request.method == 'POST'):
        username = request.form.get('username')
        password = request.form.get('password')
    if username == user['username'] and password == user['password']:
        session['user'] = username """
    #df_interaction,df_discussionparticipation,df_pageviews,df_analyticsassignments,df_participation = call_APIs(course)
    #a = create_dash(server, df_interaction,df_discussionparticipation,df_pageviews,df_analyticsassignments,df_participation)
    return app.index

@app.server.route('/')
def home():
    return "hello"
