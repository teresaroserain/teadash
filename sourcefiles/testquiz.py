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
import src.utils.transactions as transactions

df_courses = pd.read_csv(os.path.join(os.path.dirname(__file__) +'/Datasets/courseID.csv'), delimiter=";")


for i, course in df_courses.iterrows():
    print("Working on course ", course["CourseId"])
    if not np.isnan(course["CourseId"]): #check if courseId is a number
        #course = df_courses[df_courses.CourseId == row["CourseId"]]
        #print("Working on courseId {}".format(course))
        try: 
            df_quizsubmissions = transactions.get_quizsubmissions(course)
            print("df_quizsubmissions  ", df_quizsubmissions)
               
        except:
            #print(repr(topics))
            print(sys.exc_info())
