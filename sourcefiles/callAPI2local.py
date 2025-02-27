#if __name__ ==  '__main__':
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import json_normalize
import os
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash import ctx
from dash.dependencies import Input, Output 
import plotly.express as px
import pandas as pd
import pandasql as ps
from pandasql import sqldf
import os
import numpy as np
from flask import send_from_directory
from flask import (Flask, render_template, request, redirect, session)
from datetime import timedelta
import matplotlib.pyplot as plt
from dash.exceptions import PreventUpdate
import src.utils.transactions as transactions
import src.visualization.simplegraph as simplegraph
import src.visualization.networkgraph as networkgraph
import src.utils.sqlqueries as sqlqueries
import src.algorithms.DecisionTree as DecisionTree
import src.utils.functions as functions
import os.path as Path
import dash_auth

import urllib.parse


df_interaction = pd.DataFrame({
            'Source':[],
            'Target':[],
            }, dtype=object)
df_discussionparticipation = pd.DataFrame()
df_pageviews = pd.DataFrame()
df_analyticsassignments = pd.DataFrame()
df_participation = pd.DataFrame()
df_quizsubmissions = pd.DataFrame()
"""assgn = {}
optstatus = {}
quizzes = {}
discussions = {} 
course = {}"""

VALID_USERNAME_PASSWORD_PAIRS = {
    'hello': 'world'
}


    

    

df_courses = pd.read_csv(os.path.join(os.path.dirname(__file__) +'/Datasets/courseID.csv'), delimiter=";")
# ======= extract data and create DataFrames =======

for i, course in df_courses.iterrows():
    if not np.isnan(course["CourseId"]):
        #course = df[df.CourseId == courseId]
        #courseId = int(courseId)
        print("Working on courseId {}".format(course['CourseId']))
        #df_studentsummaries = transactions.get_studentsummaries(course)
        #print("df student summaries ", df_studentsummaries)
        # ======= DataFrame Discussions and Interaction =======
        if os.path.exists(os.path.join(os.path.dirname(__file__) +'/Datasets/df_discussions_'+ str(course["CourseId"]) +'.csv')) == True:
            df_discussions = pd.read_csv(os.path.join(os.path.dirname(__file__) +'/Datasets/df_discussions_'+ str(course["CourseId"]) +'.csv'), delimiter=";")
            for x, row in df_discussions.iterrows():
                df_interaction.loc[len(df_interaction.index)] = [str(row["EntryUserId"]), str(row["ReplyUserId"])]
            #print(os.path.exists(os.path.join(os.path.dirname(__file__) +'/Datasets/participation_'+ str(course["CourseId"]) +'.csv')))
            #df_interaction = pd.read_csv(os.path.join(os.path.dirname(__file__) +'/Datasets/interaction_'+ str(course["CourseId"]) +'.csv'), delimiter=";")
            df_discussionparticipation = pd.read_csv(os.path.join(os.path.dirname(__file__) +'/Datasets/discussionparticipation_'+ str(course["CourseId"]) +'.csv'), delimiter=";")
        #else: 
        ####df_interaction, df_discussionparticipation = transactions.get_interactions_discussionview(course)
        #print("df_interaction  ", df_interaction)
        # ======= DataFrame Assignments =======
        #df_assignments = transactions.get_assignments(course)
        #print("df_assignments  ", df_assignments)
        # ======= DataFrame Pageview =======
        if os.path.exists(os.path.join(os.path.dirname(__file__) +'/Datasets/df_pageviews_'+ str(course["CourseId"]) +'.csv')) == True:
            df_pageviews = pd.read_csv(os.path.join(os.path.dirname(__file__) +'/Datasets/df_pageviews_'+ str(course["CourseId"]) +'.csv'), delimiter=";")
        #else:  """
        ####df_pageviews = transactions.get_pageviews(course)
        # ======= DataFrame Analytics Assignments =======
        if os.path.exists(os.path.join(os.path.dirname(__file__) +'/Datasets/analyticsassignments_'+ str(course["CourseId"]) +'.csv')) == True:
        #    #print(os.path.exists(os.path.join(os.path.dirname(__file__) +'/Datasets/participation.csv')))
            df_analyticsassignments = pd.read_csv(os.path.join(os.path.dirname(__file__) +'/Datasets/analyticsassignments_'+ str(course["CourseId"]) +'.csv'), delimiter=";")
        #else:  """
        ####df_analyticsassignments = transactions.get_analyticsassignments(course)
        
        # ======= DataFrame Participations =======
        if os.path.exists(os.path.join(os.path.dirname(__file__) +'/Datasets/participation_'+ str(course["CourseId"]) +'.csv')) == True:
        #    #print(os.path.exists(os.path.join(os.path.dirname(__file__) +'/Datasets/participation.csv')))
            df_participation = pd.read_csv(os.path.join(os.path.dirname(__file__) +'/Datasets/participation_'+ str(course["CourseId"]) +'.csv'), delimiter=";")
        #else: """ 
        ####df_participation = transactions.get_participations(course)
        # ======= DataFrame StudentActivities =======
        ####df_useractivities = transactions.get_useractivities(course)
        # ======= DataFrame Quiz Submission =======
        #""" if os.path.exists(os.path.join(os.path.dirname(__file__) +'/Datasets/quizsubmissions.csv')) == True:
        #    df_quizsubmissions = pd.read_csv(os.path.join(os.path.dirname(__file__) +'/Datasets/quizsubmissions.csv'), delimiter=";")
        #else: """ 
        ####df_quizsubmissions = transactions.get_quizsubmissions(course)
        #print("df_quizsubmissions  ", df_quizsubmissions)

        #print("df_participation  ", df_participation)
            
    

#def create_dash(server, df_interaction,df_discussionparticipation,df_pageviews,df_analyticsassignments,df_participation):
    # ======= Init =======
mysql = lambda q: sqldf(q, globals())

# ======= Import the stylesheets =======
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# ============= Launch the application ==============
#app =  dash.Dash(server=server, routes_pathname_prefix="/dash/", external_stylesheets=external_stylesheets) # 
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


assgn = [{'label' : i, 'value' : j} for i, j in zip(df_analyticsassignments.iloc[:,6].unique(), df_analyticsassignments.iloc[:,5].unique())] 
print("dd value ", assgn)
optstatus = [{'label' : i, 'value' : j} for i, j in zip(df_analyticsassignments.iloc[:,9].unique(), df_analyticsassignments.iloc[:,9].unique())] 
print("dd optstatus ", optstatus)
discussions = [{'label' : i, 'value' : j} for i, j in zip(df_discussionparticipation.iloc[:,6].unique(), df_discussionparticipation.iloc[:,5].unique())] 
df_temp = df_analyticsassignments[df_analyticsassignments.IsQuiz==1]
quizzes = [{'label' : i, 'value' : j} for i, j in zip(df_temp.iloc[:,6].unique(), df_temp.iloc[:,5].unique())]  

# ======= defines all dcc and htmls =======
app.layout = html.Div(className="cover",
                children =[
                    dcc.Location(id='url', refresh=False),
                    html.Div(
                            className="titleArea",
                            children=[
                                html.H5(
                                    children='Teacher-facing Dashboard',
                                    style={
                                        'textAlign': 'center',
                                        }
                                    ),
                                html.Div(id ="courseid",
                                    style={
                                        'textAlign': 'center',
                                        }
                                )
                            ]
                    ),
                    dcc.Tabs(id='tabs', value='tabs', className='tabs-container',
                            children=[
                                dcc.Tab(label='Tab one', value='tab1', ),
                                dcc.Tab(label='Tab two', value='tab2',),
                    ]),
                    html.Div(id='div1',
                        children = [
                            dcc.Store(id='stored_course'),
                            #dcc.Store(id='stored_analyticsassignments'),
                            #dcc.Store(id='stored_interaction'),
                            #dcc.Store(id='stored_discussionparticipation'),
                            #dcc.Store(id='stored_pageviews'),
                            dcc.Store(id='stored_prediction'),
                            html.Div(className='block',
                                    children = [html.Div(className = 'control',
                                                        children = [
                                                            html.Button('Retrieve new data', id='retrieve_val', style={'width':'fit-content'}),
                                                            #dcc.Dropdown(id = 'ddapi', 
                                                            #            options=['Analytics', 'Assignments'], 
                                                            #            multi = True,
                                                            #            placeholder="Select APIs",
                                                            #            style={'height': '16px', 'width': '250px', 'font-size': '12px'}),
                                                ]),
                                                html.Div(id="filterbetweenassignments",
                                                        children=[html.Div(className='control',
                                                                            children = [html.Label("Filter students submitted first assignment but not second assignment")]), 
                                                                html.Div(className='control',
                                                                            children = [
                                                                                dcc.Dropdown(id = 'ddassgn1',
                                                                                            options = assgn, 
                                                                                            placeholder="Select first assignment/quiz",
                                                                                            style={'height': '15px', 'width': '230px', 'font-size': '12px'}),
                                                                                dcc.Dropdown(id = 'ddassgn2',
                                                                                            options = assgn, 
                                                                                            placeholder="Select second assignment/quiz",
                                                                                            style={'height': '15px', 'width': '230px', 'font-size': '12px'}),
                                                                                dcc.Dropdown(id = 'ddstatus',
                                                                                            options = optstatus, 
                                                                                            placeholder="Select status of assignment/quiz",
                                                                                            style={'height': '15px', 'width': '250px', 'font-size': '12px'}),
                                                                                html.Button("Download CSV", id="btn_csv"),
                                                                                dcc.Download(id="download-dataframe-csv"),
                                                                    ]),
                                                                    html.Div(className='control',
                                                                            children = [dash_table.DataTable(id='tblStudentAssgn', 
                                                                                                    data=[],
                                                                                                    columns = [],
                                                                                                    filter_action = 'native',
                                                                                                    page_size = 10,
                                                                                                    style_data={"backgroundColor":"white", 
                                                                                                                "whiteSpace": 'normal',
                                                                                                                "width": 'fit-content', 
                                                                                                                "overflow": 'hidden',
                                                                                                                "textOverflow":"ellipsis"},
                                                                            
                                                                            )]
                                                                    ),
                                                ])
                                
                            ]),
                            html.Div(className='block',
                                    children = [
                                        html.Div( 
                                                className='graph',
                                                children=[
                                                    html.Div(id='instructionbarparallel'),
                                                    html.Div(dcc.Graph(id='bar_assignments',))
                                                ],   
                                        ),
                                        html.Div( 
                                                className='graph',
                                                children=[
                                                    html.Div(dcc.Graph(id='parallel_assignments',
                                                                    config={
                                                                            'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
                                                                        },
                                                    ))
                                                ],   
                                        ),
                            ]),
                            html.Div(className='block',
                                    children = [
                                                html.Div( 
                                                        className='graph',
                                                        children=[
                                                            html.Div(dcc.Graph(id='bar_quiz'))
                                                        ],   
                                                ),
                                                html.Div( 
                                                        className='graph',
                                                        children=[
                                                            html.Div(dcc.Graph(id='parallel_quiz'))
                                                        ],   
                                                ),
                            ]),
                            html.Div(className='block',
                                    children = [
                                                html.Div( 
                                                        className='graph',
                                                        children=[
                                                            html.Div(dcc.Graph(id='courseaccess') )
                                                        ],   
                                                ),
                            ]),
                            html.Div( 
                                    className='graph',
                                    id='userviews', 
                                    children=[
                                        html.Div(dcc.Graph(figure={'data':[]}, responsive=True), style={'display': 'none'}) 
                                    ],   
                            ),
                            html.Div( 
                                    className='graph',
                                    id='userparticipation', 
                                    children=[
                                        html.Div(dcc.Graph(figure={'data':[]}, responsive=True), style={'display': 'none'})      
                                    ],   
                            ),
                            html.Div(className='block_row',
                                    children = [html.Div(className='block_row',
                                                        children = [html.Label("Predict the final case based on the first discussion forum, the first quiz, and the number of posts."),
                                                                    html.Div(id='accuracy'),]),
                                                #html.Div(className='control',
                                                #        style={'margin-bottom':'20px'},
                                                #        children = [
                                                #            dcc.Dropdown(id = 'dddiscussion',
                                                #                        options = discussions, 
                                                #                        placeholder="Select first forum for prediction",
                                                #                        style={'height': '15px', 'width': '230px', 'font-size': '12px'}),
                                                #            dcc.Dropdown(id = 'ddquiz',
                                                #                        options = quizzes, 
                                                #                        placeholder="Select first quiz for prediction",
                                                #                        style={'height': '15px', 'width': '230px', 'font-size': '12px'}),
                                                #            dcc.Dropdown(id = 'ddtarget',
                                                #                        options = assgn, 
                                                #                        placeholder="Select target for prediction",
                                                #                        style={'height': '15px', 'width': '230px', 'font-size': '12px'}),                        
                                                #]),
                                                html.Div( 
                                                        className='graph',
                                                        #id='predict', 
                                                        children=[html.Div(id='notePredictData'),
                                                            #html.Div(dcc.Graph(figure={'data':[]}, responsive=True), style={'display': 'none'})
                                                            dash_table.DataTable(id='tblPredict', 
                                                                            data=[],
                                                                            columns = [],
                                                                            filter_action = 'native',
                                                                            page_size = 10,
                                                                            style_data={"backgroundColor":"white", 
                                                                                        "whiteSpace": 'normal',
                                                                                        "width": 'fit-content', 
                                                                                        "overflow": 'hidden',
                                                                                        "textOverflow":"ellipsis"},),
                                                            html.Div(id='noteIndividualCourseAccess'),
                                                            html.Div( 
                                                                    className='graph',
                                                                    children=[
                                                                        html.Div(dcc.Graph(id='individual_courseaccess') )
                                                                    ],   
                                                            ),
                                                        ],   
                                                ),
                            ]),
                            html.Div(className='block',
                                    children = [
                                                html.Div( 
                                                        className='graph',
                                                        children=[html.Div(id='noteNetwork'),
                                                            html.Div(dcc.Graph(id='networkgraph'))    
                                                        ],   
                                                ),
                            ]),
                            html.Div(className='block',
                                    children = [
                                                
                                                html.Div( 
                                                        className='graph',
                                                        children=[
                                                            html.Div(id='instructionnetworkparallel'),
                                                            html.Div(dcc.Graph(id='parallel_assignments_individuals',))    
                                                        ],   
                                                ),
                            ]),
                            html.Div( 
                                    children = [
                                                html.Div(className='graph',
                                                            children = [html.Div(id='notiInteraction'),
                                                                        dash_table.DataTable(id='tblPostReply', 
                                                                                            data=[],
                                                                                            columns = [],
                                                                                            filter_action = 'native',
                                                                                            page_size = 10,
                                                                                            style_data={"backgroundColor":"white", 
                                                                                                        "whiteSpace": 'normal',
                                                                                                        "width": 'fit-content', 
                                                                                                        "overflow": 'hidden',
                                                                                                        "textOverflow":"ellipsis"},                                             
                                                            )]
                                                ),]
                            ),
                        
                    ]),
                    html.Div(id='div2',
                        children = [

                    ]),
                ])

# ======= defines callbacks =======
"""@app.callback(#Output('courseid', 'children'), 
              #Output('stored_analyticsassignments', 'data'),
              #Output('stored_discussionparticipation','data'),
              Output('ddassgn1','options'),
              Output('ddassgn2','options'),
              Output('ddstatus','options'),
              #Output('stored_course','data'),
              Input('url', 'search'),
              )
def display_page(pathname):
    global course
    parsed = urllib.parse.urlparse(pathname)
    parsed_dict = urllib.parse.parse_qs(parsed.query)
    print("vo parse dict")
    print("url test ", os.path.join(os.path.dirname(__file__)))
    course = {'CourseId': int(parsed_dict['courseid'][0]), 'CourseCode':'LD1002', 'CourseName':'Miljöpsykologi och beteendedesign '}
    print("course ", course)
    #if os.path.exists(os.path.join(os.path.dirname(__file__) +'/Datasets/analyticsassignments_'+ str(course["CourseId"]) +'.csv')) == True and os.path.exists(os.path.join(os.path.dirname(__file__) +'/Datasets/discussionparticipation.csv')) == True:
    #    df_analyticsassignments = pd.read_csv(os.path.join(os.path.dirname(__file__) +'/Datasets/analyticsassignments_'+ str(course["CourseId"]) +'.csv'), delimiter=";")
    #    df_discussionparticipation = pd.read_csv(os.path.join(os.path.dirname(__file__) +'/Datasets/discussionparticipation_'+ str(course["CourseId"]) +'.csv'), delimiter=";")
    #else: 
    #    df_analyticsassignments, df_discussionparticipation = functions.call_APIs(course)
    assgn, optstatus, quizzes, discussions = functions.load_data(df_analyticsassignments, df_discussionparticipation)
    return assgn, assgn, optstatus, """

@app.callback(
    Output('div1','style'),
    [Input('tabs','value'),
    ])
def update_div1_visible(tab_val):
    print ("course info : ", course)
    if tab_val=='tab1':
        return {'display':'block'}
    else:
        return {'display':'none'}

@app.callback(
    Output('div2','style'),
    [Input('tabs','value'),
    ])
def update_div2_visible(tab_val):
    if tab_val=='tab2':
        return {'display':'block'}
    else:
        return {'display':'none'}
#for HV
""" @app.callback(
        Output('userviews', 'children'),
        Input('color', 'value')
        )
def showParallelPlot_Assignments(color):
    if len(df_useractivities.index) != 0:
        df = df_useractivities[['StudentId', 'Type', 'Title']]
        return simplegraph.showParallelPlot_Assignments(df) 
    
@app.callback(
        Output('userparticipation', 'children'),
        Input('color', 'value')
        )
def showParallelPlot_Quiz(color):
    if len(df_participation.index) != 0:
        df = df_participation[['StudentId', 'Type', 'Title']]
        return simplegraph.showParallelPlot_Assignments(df) """
    
    
#for Marcus course
@app.callback(
        Output('bar_assignments', 'figure'),
        Output('instructionbarparallel', 'children'),
        Output('bar_quiz', 'figure'),
        #Output('stored_analyticsassignments', 'data'),
        Input("retrieve_val", "n_clicks"), 
        )
def showBarGraph(n_clicks):
    #print("vo day course ..................", course)
    """if n_clicks is not None: 
        df_analyticsassignments = transactions.get_analyticsassignments(course)
    else:
        if os.path.exists(os.path.join(os.path.dirname(__file__) +'/Datasets/analyticsassignments_'+ str(course["CourseId"]) +'.csv')) == True:
            df_analyticsassignments = pd.read_csv(os.path.join(os.path.dirname(__file__) +'/Datasets/analyticsassignments_'+ str(course["CourseId"]) +'.csv'), delimiter=";")
        else: 
            df_analyticsassignments = transactions.get_analyticsassignments(course)"""
    if os.path.exists(os.path.join(os.path.dirname(__file__) +'/Datasets/analyticsassignments_'+ str(course["CourseId"]) +'.csv')) == True:
            df_analyticsassignments = pd.read_csv(os.path.join(os.path.dirname(__file__) +'/Datasets/analyticsassignments_'+ str(course["CourseId"]) +'.csv'), delimiter=";")
    print("df analytics checking...............", df_analyticsassignments)
    df_analyticsassignments = df_analyticsassignments.query("StudentName != 'Test student'")
    if len(df_analyticsassignments.index) != 0:
        print("khong vo day")
        df_participation_otherassignments = sqlqueries.sql_studentparticipation(df_analyticsassignments[df_analyticsassignments.IsQuiz==0]) 
        df_participation_quiz = sqlqueries.sql_studentparticipation(df_analyticsassignments[df_analyticsassignments.IsQuiz==1]) 
        text = "You can click on bar to view the details in the parallel graph beside."
        return simplegraph.showBarGraph(df_participation_otherassignments), text, simplegraph.showBarGraph(df_participation_quiz)#, df_analyticsassignments.to_dict('records')
    #raise PreventUpdate

#for HV
""" @app.callback(
        Output('bar_assignments', 'children'),
        Input('color', 'value')
        )
def showBarGraph(color):
    if len(df_participation.index) != 0:
        df = df_participation[['StudentId', 'Type', 'Title']]
        df = sqlqueries.sql_studentparticipation(df) 
        return simplegraph.showBarGraph_HV(df) """


#for API assignments, not analytics assignment
""" @app.callback(
        Output('individualquizgraph', 'children'),
        Input('color', 'value')
        )
def showParallelPlot_Quiz(color):
    if len(df_quizsubmissions.index) != 0:
        df_quiz = sqlqueries.sql_quizsubmissions(df_quizsubmissions)
        df_quiz['Attempts'] = df_quiz['Attempts'].fillna(0)
        df_quiz['Grade']= df_quiz['Grade'].fillna(0)
        print("df quize ", df_quiz)
        return simplegraph.showParallelPlot_Quiz(df_quiz)  """
    
@app.callback(
        Output('courseaccess', 'figure'),
        #Output('stored_pageviews', 'data'),
        #Input('stored_analyticsassignments', 'data'),
        #Input('stored_analyticsassignments', 'modified_timestamp'),
        Input("retrieve_val", "n_clicks"), 
        )
def showLineGraph_courseaccess( n_clicks):
    #print("time ", updatedtime)
    #if n_clicks is not None: 
    #    df_pageviews = transactions.get_pageviews(course)
    #    """ if data is not None:
    #        df_analyticsassignments = pd.DataFrame.from_dict(data) """
    #    if os.path.exists(os.path.join(os.path.dirname(__file__) +'/Datasets/analyticsassignments_'+ str(course["CourseId"]) +'.csv')) == True:
    #        df_analyticsassignments = pd.read_csv(os.path.join(os.path.dirname(__file__) +'/Datasets/analyticsassignments_'+ str(course["CourseId"]) +'.csv'), delimiter=";")
    #    else:
    #        df_analyticsassignments = transactions.get_analyticsassignments(course)
    #else:
    #    """ if data is not None:
    #        df_analyticsassignments = pd.DataFrame.from_dict(data)
    #    else: """
    #    if os.path.exists(os.path.join(os.path.dirname(__file__) +'/Datasets/analyticsassignments_'+ str(course["CourseId"]) +'.csv')) == True:
    #        df_analyticsassignments = pd.read_csv(os.path.join(os.path.dirname(__file__) +'/Datasets/analyticsassignments_'+ str(course["CourseId"]) +'.csv'), delimiter=";")
    #    else: 
    #        df_analyticsassignments = transactions.get_analyticsassignments(course)
    #    if os.path.exists(os.path.join(os.path.dirname(__file__) +'/Datasets/df_pageviews_'+ str(course["CourseId"]) +'.csv')) == True:
    #        df_pageviews = pd.read_csv(os.path.join(os.path.dirname(__file__) +'/Datasets/df_pageviews_'+ str(course["CourseId"]) +'.csv'), delimiter=";")
    #    else: 
    #        df_pageviews = transactions.get_pageviews(course)
    if len(df_pageviews.index) != 0:
        df_courseaccess = sqlqueries.sql_accessbydate(df_pageviews)
        if len(df_analyticsassignments.index) != 0:
            return simplegraph.showLineGraph_courseaccess(df_courseaccess, df_analyticsassignments)#, df_pageviews.to_dict('records')
        else:
            return simplegraph.showLineGraph_courseaccess(df_courseaccess, pd.DataFrame())#, df_pageviews.to_dict('records')
    #raise PreventUpdate

@app.callback(
        Output('networkgraph', 'figure'),
        Output('noteNetwork', 'children'),
        Output('notiInteraction','children'),
        Output('instructionnetworkparallel','children'),
        #Output('stored_interaction','data'),
        #Output('stored_discussionparticipation','data'),
        Input("retrieve_val", "n_clicks"), 
)
def showNetworkGraph(n_clicks):
    noti=''
    noteNetwork=''
    instructionnetworkparallel=''
    """if n_clicks is not None: 
        df_interaction, df_discussionparticipation = transactions.get_interactions_discussionview(course)
    else: 
        if os.path.exists(os.path.join(os.path.dirname(__file__) +'/Datasets/interaction_'+ str(course["CourseId"]) +'.csv')) == True:
            #print(os.path.exists(os.path.join(os.path.dirname(__file__) +'/Datasets/participation.csv')))
            df_interaction = pd.read_csv(os.path.join(os.path.dirname(__file__) +'/Datasets/interaction_'+ str(course["CourseId"]) +'.csv'), delimiter=";")
            df_discussionparticipation = pd.read_csv(os.path.join(os.path.dirname(__file__) +'/Datasets/discussionparticipation_'+ str(course["CourseId"]) +'.csv'), delimiter=";")
        else:
            df_interaction, df_discussionparticipation = transactions.get_interactions_discussionview(course)"""
    
    noti = "The students highlighted have no one commented on their posts."
    noteNetwork = "Regarding the isolated nodes (students), teachers may consider being more explicit in the instruction for discussion forums that students comment on those having no reply. "
    instructionnetworkparallel = "You can choose the select tool and select nodes in the network graph to view the details in the below graph and table."
    return networkgraph.networkGraph(df_interaction, False), noteNetwork, noti, instructionnetworkparallel#, df_interaction.to_dict('records'), df_discussionparticipation.to_dict('records')
#raise PreventUpdate

# clusters from df_quizsubmissions 
""" @app.callback(
        Output('clustergraph', 'children'),
        Input('color', 'value')
        )
def showScatterGraph_cluster(color):
    if len(df_quizsubmissions.index) != 0:
        return simplegraph.showScatterGraph_cluster(df_quizsubmissions)  """

#prediction from first discussion (participation and number of posts), first quiz
#future development: allow choosing variables for prediction
@app.callback(
        #Output('clustergraph', 'children'),
        Output('tblPredict','data'),
        Output('tblPredict','columns'),
        Output('tblPredict','style_data_conditional'),
        Output('accuracy','children'),
        Output('notePredictData','children'),
        Output('noteIndividualCourseAccess', 'children'),
        Output('stored_prediction','data'),
        #Input('dddiscussion','value'),
        #Input('ddquiz','value'),
        #Input('ddtarget','value'),
        Input("retrieve_val", "n_clicks"), 
        #Input('stored_analyticsassignments', 'data'),
        #Input('stored_interaction','data'),
        #Input('stored_discussionparticipation','data'),
        )
def showPrediction(n_clicks):
    data = []
    columns = []
    text_accuracy = ""
    style_data_conditional=[]
    notePredictData = ""
    noteIndividualCourseAccess = 'You can click on the Prediction table to see how regular a student accesses the course page in the graph below.'
    """ if stored_discussionparticipation != None:
        df_discussionparticipation = pd.DataFrame.from_dict(stored_discussionparticipation)
        df_interaction = pd.DataFrame.from_dict(stored_interaction) """
    """if os.path.exists(os.path.join(os.path.dirname(__file__) +'/Datasets/interaction_'+ str(course["CourseId"]) +'.csv')) == True:
            #print(os.path.exists(os.path.join(os.path.dirname(__file__) +'/Datasets/participation.csv')))
            df_interaction = pd.read_csv(os.path.join(os.path.dirname(__file__) +'/Datasets/interaction_'+ str(course["CourseId"]) +'.csv'), delimiter=";")
            df_discussionparticipation = pd.read_csv(os.path.join(os.path.dirname(__file__) +'/Datasets/discussionparticipation_'+ str(course["CourseId"]) +'.csv'), delimiter=";")
    else: 
        df_interaction, df_discussionparticipation = transactions.get_interactions_discussionview(course)"""
    
    """ if stored_analyticsassignments != None: 
        df_analyticsassignments = pd.DataFrame.from_dict(stored_analyticsassignments) """
    """if os.path.exists(os.path.join(os.path.dirname(__file__) +'/Datasets/analyticsassignments_'+ str(course["CourseId"]) +'.csv')) == True:
            df_analyticsassignments = pd.read_csv(os.path.join(os.path.dirname(__file__) +'/Datasets/analyticsassignments_'+ str(course["CourseId"]) +'.csv'), delimiter=";")
    else:
        df_analyticsassignments = transactions.get_analyticsassignments(course)"""
    
    discussionId = df_discussionparticipation[df_discussionparticipation['Title'].str.contains('Inledande')]['AssignmentId'].iloc[0]
    quizId = df_analyticsassignments[df_analyticsassignments['Title'].str.contains('Quiz 1')]['AssignmentId'].iloc[0]
    targetId = df_analyticsassignments[df_analyticsassignments['Title'].str.contains('Slutuppgift')]['AssignmentId'].iloc[0]
    print("dd test.............", type(discussionId), type(quizId))
    if discussionId != None and quizId != None and targetId != None:
        print("dd test.............", discussionId)
       
        df = sqlqueries.sql_dsforprediction(df_discussionparticipation, discussionId, df_interaction, df_analyticsassignments, quizId, targetId)
        #df.to_csv(os.path.join(Path.abspath(Path.join(__file__ ,".."))+'/Datasets/df_train_47147.csv'), sep=';', index=False, encoding='utf-8' )
        df.info()
        df = df.drop(columns=['StudentName'])
        if len(df.index) != 0: 
            result, accuracy = DecisionTree.buildDecisionTree(df)
            """ if len(df_quizsubmissions.index) != 0:
            return simplegraph.showScatterGraph_cluster(df_quizsubmissions)  """
            columns=[{"name": i, "id": i} for i in result.columns] 
            data=result.to_dict('records')
            style_data_conditional=[{
                                        'if': {
                                            'filter_query': '{PredictedValue} = 0', # comparing columns to each other
                                            'column_id': 'PredictedValue'
                                        },
                                        'backgroundColor': 'tomato',
                                        'color': 'white'
                                    },]
            text_accuracy = 'Accuracy: %.2f' % round(accuracy*100, 2) +'%'
            notePredictData = "Except the column Posts, the value 0 means Not participate, 1 means Participate. The highlighted students might not submit the last assignment."
    return data, columns, style_data_conditional, text_accuracy, notePredictData, noteIndividualCourseAccess, data

@app.callback(
        Output('parallel_quiz', 'figure'),
        Input('bar_quiz', 'clickData'),
        Input("retrieve_val", "n_clicks"), 
        #Input('stored_analyticsassignments', 'data'),
)
def updateParallelQuiz(clickData, n_clicks):
    """ if stored_analyticsassignments != None: 
        df_analyticsassignments = pd.DataFrame.from_dict(stored_analyticsassignments)
    else: """
    """if os.path.exists(os.path.join(os.path.dirname(__file__) +'/Datasets/analyticsassignments_'+ str(course["CourseId"]) +'.csv')) == True:
        df_analyticsassignments = pd.read_csv(os.path.join(os.path.dirname(__file__) +'/Datasets/analyticsassignments_'+ str(course["CourseId"]) +'.csv'), delimiter=";")
    else: 
        df_analyticsassignments = transactions.get_analyticsassignments(course)"""
    
    if clickData != None:
        #print("click data ", clickData['points']['customdata'])
        if len(df_analyticsassignments.index) != 0:
            for item in clickData['points']:
                df = sqlqueries.sql_filterbybarchart(df_analyticsassignments[df_analyticsassignments.IsQuiz==1], item['x'], item['customdata'][0]) 
                df = df[['StudentId', 'Title', 'Status']]
                fig = simplegraph.showParallelPlot_AnalyticsQuiz(df)
            return fig
    else: 
        if len(df_analyticsassignments.index) != 0:
            df = df_analyticsassignments[df_analyticsassignments.IsQuiz==1]
            #show student name
            #df = df[['StudentId', 'StudentName', 'Title', 'Status']]
            #not show student name
            df = df[['StudentId', 'Title', 'Status']]
            fig = simplegraph.showParallelPlot_AnalyticsQuiz(df)
            return fig
    #raise PreventUpdate
        
@app.callback(
        Output('parallel_assignments', 'figure'),
        Input('bar_assignments', 'clickData'),
        Input("retrieve_val", "n_clicks"), 
        #Input('stored_analyticsassignments', 'data'),
)
def updateParallelQuiz(clickData, n_clicks):
    """ if stored_analyticsassignments != None: 
        df_analyticsassignments = pd.DataFrame.from_dict(stored_analyticsassignments)
    else: """
    """if os.path.exists(os.path.join(os.path.dirname(__file__) +'/Datasets/analyticsassignments_'+ str(course["CourseId"]) +'.csv')) == True:
            df_analyticsassignments = pd.read_csv(os.path.join(os.path.dirname(__file__) +'/Datasets/analyticsassignments_'+ str(course["CourseId"]) +'.csv'), delimiter=";")
    else: 
        df_analyticsassignments = transactions.get_analyticsassignments(course)"""

    if clickData != None:
        #print("click data ", clickData['points']['customdata'])
        if len(df_analyticsassignments.index) != 0:
            for item in clickData['points']:
                df = sqlqueries.sql_filterbybarchart(df_analyticsassignments[df_analyticsassignments.IsQuiz==0], item['x'], item['customdata'][0]) 
                df = df[['StudentId', 'Title', 'Status']]
                fig = simplegraph.showParallelPlot_AnalyticsQuiz(df)
            return fig
    else: 
        if len(df_analyticsassignments.index) != 0:
            df = df_analyticsassignments[df_analyticsassignments.IsQuiz==0]
            #show student name
            #df = df[['StudentId', 'StudentName', 'Title', 'Status']]
            #not show student name
            df = df[['StudentId', 'Title', 'Status']]
            fig = simplegraph.showParallelPlot_AnalyticsQuiz(df)
            return fig
    #raise PreventUpdate

@app.callback(
    Output('tblStudentAssgn','data'),
    Output('tblStudentAssgn','columns'),
    Output("download-dataframe-csv", "data"),
    Input('ddassgn1','value'),
    Input('ddassgn2','value'),
    Input('ddstatus','value'),
    Input("retrieve_val", "n_clicks"), 
    #Input('stored_analyticsassignments', 'data'),
    Input("btn_csv", "n_clicks"),
)
def showTblStuddentAssgn(assgn1, assgn2, status, retrieve_btn, download_btn):
    data = []
    columns = []
    df = pd.DataFrame()
    """if stored_analyticsassignments != None: 
        df_analyticsassignments = pd.DataFrame.from_dict(stored_analyticsassignments)
    else: """
    """if os.path.exists(os.path.join(os.path.dirname(__file__) +'/Datasets/analyticsassignments_'+ str(course["CourseId"]) +'.csv')) == True:
            df_analyticsassignments = pd.read_csv(os.path.join(os.path.dirname(__file__) +'/Datasets/analyticsassignments_'+ str(course["CourseId"]) +'.csv'), delimiter=";")
    else: 
        df_analyticsassignments = transactions.get_analyticsassignments(course)"""
    
    if (assgn1 != None) and (assgn2 != None) and (status != None):
        print("assgn 1 ", assgn1)
        print("assgn 2 ", assgn2)
        print("status ", status)
        if len(df_analyticsassignments.index) != 0:
            df = sqlqueries.sql_filterbetweenassignments(df_analyticsassignments, assgn1, assgn2, status)
            #show student name
            #df = df[["StudentId", "StudentName", "Title", "Status"]]
            #not show student name
            df = df[["StudentId", "Title", "Status"]]
            columns=[{"name": i, "id": i} for i in df.columns] 
            data=df.to_dict('records')
    if download_btn is not None:
        return data, columns, dcc.send_data_frame(df.to_csv, "unsubmitted_students.csv")
    else:
        return data, columns, None
        
@app.callback(
        Output('parallel_assignments_individuals', 'figure'),
        Output('tblPostReply','data'),
        Output('tblPostReply','columns'),
        Output('tblPostReply','style_data_conditional'),
        Input('networkgraph', 'selectedData'),
        Input("retrieve_val", "n_clicks"), 
        #Input('stored_analyticsassignments', 'data'),
        #Input('stored_interaction','data'),
    )
def showParallelIndividuals(selectedData, n_clicks):
    data = []
    columns = []
    style_data_conditional=[]
    df_tbl = pd.DataFrame()
    fig = simplegraph.showParallelPlot_AnalyticsQuiz(pd.DataFrame())  
    
    """ if stored_interaction != None:
        df_interaction = pd.DataFrame.from_dict(stored_interaction) """
    """if os.path.exists(os.path.join(os.path.dirname(__file__) +'/Datasets/interaction_'+ str(course["CourseId"]) +'.csv')) == True:
        df_interaction = pd.read_csv(os.path.join(os.path.dirname(__file__) +'/Datasets/interaction_'+ str(course["CourseId"]) +'.csv'), delimiter=";")
    else: 
        df_interaction, df_discussionparticipation = transactions.get_interactions_discussionview(course)"""
    
    """ if stored_analyticsassignments != None: 
        df_analyticsassignments = pd.DataFrame.from_dict(stored_analyticsassignments)
    else: """
    """if os.path.exists(os.path.join(os.path.dirname(__file__) +'/Datasets/analyticsassignments_'+ str(course["CourseId"]) +'.csv')) == True:
            df_analyticsassignments = pd.read_csv(os.path.join(os.path.dirname(__file__) +'/Datasets/analyticsassignments_'+ str(course["CourseId"]) +'.csv'), delimiter=";")
    else: 
        df_analyticsassignments = transactions.get_analyticsassignments(course)"""

    if selectedData != None:
        students = []
        for item in selectedData['points']:
            students.append(item['text'])
        print("students ", students)
        if len(df_analyticsassignments.index) != 0:    
            print("selected data ", selectedData)
            df = sqlqueries.sql_filterstudentsbynetwork(df_analyticsassignments, students) 
            fig = simplegraph.showParallelPlot_AnalyticsQuiz(df)              
            fig.update_layout(height=600, width=1200,)
        if len(df_interaction.index) != 0:
            df_tbl = sqlqueries.sql_filtertblcountpostbynetwork(df_interaction, students)
    else: 
        if len(df_interaction.index) != 0:
            df_tbl = sqlqueries.sql_countposts(df_interaction)

    df_tbl = df_tbl.fillna(0)
    columns=[{"name": i, "id": i} for i in df_tbl.columns] 
    data=df_tbl.to_dict('records')
    style_data_conditional=[{
                                'if': {
                                    'filter_query': '{Replies} = 0', # comparing columns to each other
                                    'column_id': 'Replies'
                                },
                                'backgroundColor': 'tomato',
                                'color': 'white'
                            },]  
    return fig, data, columns, style_data_conditional

@app.callback(
        Output('individual_courseaccess', 'figure'),
        Input('tblPredict', 'selected_cells'),
        #Input('stored_pageviews', 'data'),
        Input('stored_prediction','data'),
        Input("retrieve_val", "n_clicks"), 
    )
def showIndividualCourseAccess(selectedData, stored_prediction, n_clicks):
    print("selected row ", selectedData)
    students = []
    df_prediction = pd.DataFrame.from_dict(stored_prediction)
    #print("store prediction .............. ", df_prediction)
    if os.path.exists(os.path.join(os.path.dirname(__file__) +'/Datasets/df_pageviews_'+ str(course["CourseId"]) +'.csv')) == True:
            df_pageviews = pd.read_csv(os.path.join(os.path.dirname(__file__) +'/Datasets/df_pageviews_'+ str(course["CourseId"]) +'.csv'), delimiter=";")
    if selectedData != None:
        rows = []
        for item in selectedData:
            rows.append(item['row'])
        for x, item in df_prediction.iterrows():
            for i in rows:
                if x == i:    
                    students.append(item['StudentId'])
        rslt_df = df_pageviews[df_pageviews['StudentId'].isin(students)]
        print("checking........", rslt_df)
        fig = simplegraph.showLineGraph_individualcourseaccess(rslt_df)
        
        return fig
    raise PreventUpdate      
        

if __name__ == '__main__':
    app.run_server(debug = True)

    
   