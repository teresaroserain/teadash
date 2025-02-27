import networkx as nx
import src.visualization.networkgraph as networkgraph
import dash 
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
import json, sys
from pandas import json_normalize
import os
import src.utils.APIs as apis
import plotly.graph_objects as go

df_courses = pd.read_csv(os.path.join(os.path.dirname(__file__) +'/Datasets/courseID.csv'), delimiter=";")


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

df_interaction = pd.DataFrame({
                'Source':[],
                'Target':[],
                }, dtype=object)

for courseId in df_courses["CourseId"]:
    if not np.isnan(courseId):
        course = df_courses[df_courses.CourseId == courseId]
        courseId = int(courseId)
        #print("Working on courseId {}".format(courseId))
        try: 
            topics = apis.getDiscussions(courseId)
            #print("result ", topics[0]["id"])
            for i in range(len(topics)):
                df_discussions.loc[len(df_discussions.index)] = [courseId, course["CourseCode"].values[0], 
                                                                course["CourseName"].values[0], topics[i]["id"], 
                                                                topics[i]["title"], 
                                                                #topics[i]["author"]["id"], topics[i]["author"]["display_name"], 
                                                                "", "", "", "", "", "", topics[i]["message"]]
                print ("discussions ", df_discussions)
                entries = apis.getEntries(courseId, topics[i]["id"])
                for j in range(len(entries)):
                    #print("entry list  ", entries[j]["id"])
                    df_discussions.loc[len(df_discussions.index)] = [courseId, course["CourseCode"].values[0], 
                                                                course["CourseName"].values[0], topics[i]["id"], 
                                                                topics[i]["title"],  #topics[i]["author"]["id"], topics[i]["author"]["display_name"], 
                                                                entries[j]["id"], entries[j]["user_id"], entries[j]["user_name"],
                                                                "", "", "", entries[j]["message"]]
                    replies = apis.getEntryReplies(courseId, topics[i]["id"], entries[j]["id"])
                    #print("replies: ", replies)
                    for z in range(len(replies)):
                        df_discussions.loc[len(df_discussions.index)] = [courseId, course["CourseCode"].values[0], 
                                                                    course["CourseName"].values[0], topics[i]["id"], topics[i]["title"],
                                                                    #topics[i]["author"]["id"], topics[i]["author"]["display_name"], 
                                                                    entries[j]["id"], entries[j]["user_id"], 
                                                                    entries[j]["user_name"], replies[z]["id"], 
                                                                    replies[z]["user_id"], replies[z]["user_name"], replies[z]["message"]]
        except:
            #print(repr(topics))
            print(sys.exc_info())

    print("df_discussions ", df_discussions)

for x, row in df_discussions.iterrows():
    #df_interaction.loc[len(df_interaction.index)] = [str(row["TopicUserName"]), str(row["EntryUserName"])]
    df_interaction.loc[len(df_interaction.index)] = [str(row["EntryUserName"]), str(row["ReplyUserName"])]
        

print("interaction ", df_interaction)

app = dash.Dash()

app.layout = html.Div(className="cover",
                    children =[
                        html.Div( 
                                className='chart',
                                id='chart',
                                children=[
                                    html.Div(dcc.Graph(id='mainArea', figure={'data': []}), style={'display': 'none'})
                                ],   
                        ),
                        dcc.RadioItems(id = 'color', 
                                   options=[{'label': 'Red', 'value': '#ff0000'}, 
                                            {'label': 'Blue', 'value': '0000ff'}], value='Red'),
                    ])


@app.callback(
            Output('chart', 'children'),
            Input('color', 'value')
            )
def myfun(color):
    return networkgraph.networkGraph(df_interaction, False) 

if __name__ == '__main__':
    app.run_server(debug = True)
