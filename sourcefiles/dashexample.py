# ======= Import the libraries =======
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
import plotly.graph_objects as go
from flask import send_from_directory
from datetime import timedelta
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.cluster import KMeans
from sklearn.metrics import davies_bouldin_score
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from dash.exceptions import PreventUpdate
from datetime import datetime, date


# ======= Init =======
#format_data = "%Y-%m-%d %H:%M:%S"

mysql = lambda q: sqldf(q, globals())

# ======= Import the stylesheets =======
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# ============= Launch the application ==============
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#app = dash.Dash(__name__)
#app.head = [html.Link(rel='stylesheet', href='./Datasets/cssFile.css')]

# ======= Import and preprocessing the datasets =======
# ======= Pageview dataset =======
df_pageview = pd.read_csv(os.path.join(os.path.dirname(__file__), 'Datasets/pageview.csv'), delimiter=";")
df_pageview['AccessedDate'] = pd.to_datetime(df_pageview['AccessedDate'])#, format=format_data)
#df_pageview['StudentId'] = df_pageview['StudentId'].apply(str)
print(df_pageview)

# ======= Assignment dataset =======
df_submission = pd.read_csv(os.path.join(os.path.dirname(__file__), 'Datasets/assignment.csv'), delimiter=";")
df_submission['DueAt'] = pd.to_datetime(df_submission['DueAt'])#, format=format_data)
df_submission['SubmittedAt'] = pd.to_datetime(df_submission['SubmittedAt'])#, format=format_data)
df_submission['StudentId'] = df_submission['StudentId'].astype(str)
df_submission['AssignmentId'] = df_submission['AssignmentId'].apply(str)

#======= Pageview dataset by Date for cluster =======
df_pageview['Date'] = df_pageview['AccessedDate'].dt.date
df_pageview['Hour'] = df_pageview['AccessedDate'].dt.hour
df_pageview['StudentId'] = df_pageview['StudentId'].astype(int)
df_pageview['Year'] = df_pageview['AccessedDate'].dt.year
df_pageview['Month'] = df_pageview['AccessedDate'].dt.month
df_pageview['Day'] = df_pageview['AccessedDate'].dt.day
df_pageview['Week'] = df_pageview['AccessedDate'].dt.isocalendar().week.astype(int)
df_pageview['Weekday'] = df_pageview['AccessedDate'].dt.dayofweek
df_pageview['WeekdayName'] = df_pageview['AccessedDate'].dt.day_name()
df_pageview['Minute'] = df_pageview['AccessedDate'].dt.minute
df_pageview['Second'] = df_pageview['AccessedDate'].dt.second
#df_pageview['Result'] = df_pageview['Result'].map({'Incomplete': 0, 'Completed': 1})
data_date = pd.DataFrame(mysql("SELECT Date, CourseId, sum(ViewCount) as 'SumView', count(distinct StudentId) as 'CountStudent', Result from df_pageview group by Date, CourseId")) 
data_hour = pd.DataFrame(mysql("SELECT Hour, CourseId, sum(ViewCount) as 'SumView', count(distinct StudentId) as 'CountStudent', Result from df_pageview group by Hour, CourseId")) 
data_weekday = pd.DataFrame(mysql("SELECT Weekday, CourseId, WeekdayName, count(distinct StudentId) as 'CountStudent', Result from df_pageview group by Weekday, CourseId")) 
print("data weekday ", data_weekday)
# ======= Create sub-datasets for charts =======
df_finalResult = pd.DataFrame(mysql("Select CourseId, round(avg(case when Result='Completed' then 100.0 else 0.0 end),2) as 'Completed', round(avg(case when Result='Incomplete' then 100.0 else 0.0 end),2) as 'Incomplete' from df_submission group by CourseId"))
df_submission_count = pd.DataFrame(mysql("SELECT CourseId, COUNT(CASE WHEN SubmittedAt is not null THEN 1 ELSE NULL END) AS 'Submitted',COUNT(CASE WHEN SubmittedAt is null THEN 1 ELSE NULL END) AS 'NotSubmit', translatedTitle FROM df_submission group by AssignmentId"))
df_submission_percent = pd.DataFrame(mysql("Select CourseId, round(avg(case when SubmittedAt is not null then 100.0 else 0.0 end),2) as 'Submitted', round(avg(case when SubmittedAt is null then 100.0 else 0.0 end),2) as 'NotSubmit', translatedTitle from df_submission group by AssignmentId"))
print("final result beginning: ", df_finalResult)
# ======= Create sub-dataset for dropdown list =======
df_courseSelection = pd.DataFrame(mysql("Select distinct(CourseId), CourseName from df_pageview"))
conditions = [
    (df_courseSelection['CourseId'] == "A1_1"),
    (df_courseSelection['CourseId'] == "A1_2"),
    (df_courseSelection['CourseId'] == "B2_1"),
    (df_courseSelection['CourseId'] == "B2_2"),
    (df_courseSelection['CourseId'] == "B2_3"),
    (df_courseSelection['CourseId'] == "C3_1"),
    (df_courseSelection['CourseId'] == "C3_2"),
    (df_courseSelection['CourseId'] == "D4_1"),
    (df_courseSelection['CourseId'] == "D4_2"),
    (df_courseSelection['CourseId'] == "E5_1")
    ]
# create a list of the values we want to assign for each condition
values = ['VT19', 'VT21', 'VT19', 'VT20', 'VT21', 'VT20', 'VT21', 'VT20', 'VT21', 'HT19']

# create a new column and use np.select to assign values to it using our lists as arguments
df_courseSelection['CourseTime'] = np.select(conditions, values)
df_courseSelection["Period"] = df_courseSelection[["CourseName", "CourseTime"]].apply("-".join, axis=1)
#print(df_courseSelection)

opts1 = [{'label' : i, 'value' : j} for i, j in zip(df_courseSelection.iloc[:,3], df_courseSelection.iloc[:,0])] 

# ======= defines all dcc and htmls =======
app.layout = html.Div( 
    className="cover",
    children =[
        html.Div(
            className="titleArea",
            children=[
                html.H5(
                    children='Visualization of Employed Adult Learner Learning',
                    style={
                        'textAlign': 'center',
                        }
                    ),

                html.Div(
                    children='''
                        Work-integrated Learning Courses
                    ''',
                    style={
                        'textAlign': 'center',
                        'color': 'grey',
                        'font-size': '16px'
                        }
                    )
            ]
        ),
        dcc.Tabs(
            id="tabs",
            value='tabs',
            className='tab-bar',
            children=[
                dcc.Tab(
                    id = 'tab_overview',
                    label='Overview of one course',
                    value='tab-1',
                    className='tab-layout',
                    children = [
                        html.Div(
                            className='selectionArea',
                            children=[
                                html.Label(["Select course:", 
                                dcc.Dropdown(
                                    id = 'ddcourse', 
                                    options = opts1, 
                                    placeholder='Select a course',
                                    style={'height': 'fit-content', 'width': '200px', 'font-size': '12px'})]),
                                
                            ],
                            style={'font-size':'12px'}
                        ),
                        html.Div( 
                            className='displayArea',
                            children=[
                                html.Div(
                                    className='chart',
                                    children=[
                                        html.Div([
                                            html.Div(
                                                className='plus',
                                                children=[
                                                    html.Label(["Cluster following: ", 
                                                    dcc.Dropdown(id = 'ddcluster', 
                                                                options=['Day', 'Hour', 'Weekday'], 
                                                                value = 'Day',
                                                                style={'height': '13px', 'width': '200px', 'font-size': '12px'}),
                                                    ])]
                                            ),
                                            dcc.Graph(id='cluster_date_fig', figure = {},
                                                        clickData=None, hoverData=None, # I assigned None for tutorial purposes. By defualt, these are None, unless you specify otherwise.
                                                        config={
                                                            'staticPlot': False,     # True, False
                                                            'scrollZoom': True,      # True, False
                                                            'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
                                                            'showTips': False,       # True, False
                                                            'displayModeBar': True,  # True, False, 'hover'
                                                            'watermark': False,
                                                        },
                                            )]
                                        )
                                    ],
                                ),
                                html.Div(
                                    className='chart',
                                    children=[
                                        html.Div(
                                            className='plus',
                                            children=[
                                                html.Label(["Visualize following: ", 
                                                dcc.Dropdown(id = 'ddparallel', options=['Date', 'Time', 'Week - Weekday'], 
                                                value = 'Date',
                                                style={'height': '13px', 'width': '200px', 'font-size': '12px'}),
                                                ])]
                                        ),
                                        html.Div(dcc.Graph(id='paralell_fig', figure = {}))
                                    ],   
                                ),
                                html.Div(
                                    className='chart',
                                    children=[
                                        html.Div(
                                            className='plus',
                                            children=[
                                                html.Label(["Submission pattern: ", 
                                                dcc.RadioItems(id = 'ribar', options=['Count', 'Percentage'], value = 'Count', inline=True)])]
                                        ),
                                        html.Div(dcc.Graph(id='bar_fig', figure = {}))
                                    ],   
                                ),
                            ],   
                        ),
                        html.Div( 
                            className='displayArea',
                            children=[dcc.Store(id='cluster_data'),
                                    html.Div(
                                        className = "plus",
                                        children = [
                                            html.Label("Information of clusters", style={'font-size':'12px', 'margin-bottom': '10px'}),
                                            html.Div(dash_table.DataTable(id='tableCluster', 
                                                                        data=[],
                                                                        columns = [],
                                                                        filter_action = 'native',
                                                                        page_size = 10,
                                                                        style_data={"backgroundColor":"white", 
                                                                                    "whiteSpace": 'normal',
                                                                                    "width": '150px', 'minWidth': '150px', 'maxWidth': '150px',
                                                                                    "overflow": 'hidden',
                                                                                    "textOverflow":"ellipsis"},
                                                                    
                                                                        ))
                                        ]
                                    )
                            ],
                          
                        )
                    ]
                ),
                dcc.Tab(
                    id='tab_comparison',
                    label='Comparison between courses',
                    value='tab-2',
                    className='tab-layout',
                    children=[
                        html.Div(
                            className='selectionArea',
                            children=[
                                html.Label(["Select 3 courses:", 
                                    dcc.Dropdown(
                                        id = 'ddcourses', 
                                        options = opts1, 
                                        placeholder='Select courses',
                                        multi=True,
                                        style={'height': '13px', 'width': '300px', 'font-size': '12px'})]),    
                                html.Label(["Select pattern:", 
                                    dcc.Dropdown(
                                        id = 'ddpattern', 
                                        options=['Access', 'Submission'],
                                        placeholder='Select a pattern',
                                        value = 'Submission',
                                        style={'height': '13px', 'width': '200px', 'font-size': '12px'})]),  
                                html.Label(["Select visualization type:", 
                                    dcc.Dropdown(
                                        id = 'ddtype', 
                                        options=['Count', 'Percentage'],
                                        placeholder='Select a visualization type',
                                        value = 'Count',
                                        style={'height': '13px', 'width': '200px', 'font-size': '12px'})]),          
                            ],
                            style={'font-size':'12px', 'height':'80px'}
                        ),
                        html.Div( 
                            className='dynamicDisplayArea',
                            id = 'dynamicDisplayArea',
                                children=[
                                    html.Div(
                                        className='chart',
                                        children=[
                                            html.Div(dcc.Graph(id='mainArea', figure={'data': []}), style={'display': 'none'})
                                        ],
                                    )
                                ],   
                        ),
                        html.Div( 
                            className='dynamicDisplayArea',
                            id = 'dynamicPieCharts',
                                children=[
                                    html.Div(
                                        className='chart',
                                        children=[
                                            html.Div(dcc.Graph(id='resultArea', figure={'data': []}), style={'display': 'none'})
                                        ],
                                    )
                                ],   
                        ),
                    ]    
                ),
            ],
            style={"text-align": "center", "padding":"0", 'font-size': '14px'}
        )
    ],
)

# ======= defines callback to the cluster scatter chart =======
@app.callback(
    Output('cluster_date_fig', 'figure'),
    Output('cluster_data', 'data'),
    Input('ddcourse', 'value'),
    Input('ddcluster', 'value'),
)
def update_scattergraph(course_selected, cluster_pattern):
    cluster_date_fig = go.Figure()
    print("pattern ", cluster_pattern)
    if cluster_pattern == "Day" and course_selected != None:
        sub_data_date = data_date[data_date.CourseId==course_selected]
        sub_data_date['Date'] = pd.to_datetime(sub_data_date['Date'])
        sub_data_date = sub_data_date[['Date', 'SumView', 'CountStudent']]
        sub_data_date['SumView'] = pd.to_numeric(sub_data_date['SumView'])
        sub_data_date['CountStudent'] = pd.to_numeric(sub_data_date['CountStudent'])
        sub_data_date = sub_data_date.sort_values('Date', ascending=True) 
        sub_data_date = sub_data_date.fillna(0)
        daycount = (pd.to_datetime(np.max(sub_data_date['Date'])) - pd.to_datetime(np.min(sub_data_date['Date']))).days
        print(daycount)
            
        #Create ds following day order
        date = np.min(sub_data_date['Date'])
        counter_ = 0
        df_series = pd.DataFrame({
            'Date': [],
            'Day':[],
            'SumView':[],
            'CountStudent':[]
        }, dtype=object)
        while counter_ <= daycount:
            if (sub_data_date['Date'] == pd.Timestamp(date)).any():
                row = sub_data_date[sub_data_date['Date'] == date]
                df_series.loc[len(df_series.index)] = [date, counter_+1, row['SumView'], row['CountStudent']]
            else:
                df_series.loc[len(df_series.index)] = [date, counter_+1, 0, 0]
            counter_ += 1
            date = date + timedelta(days=1)
        print(df_series.head())

            
        if not df_series.empty:
            #Standardize data Date
            x_calls = df_series.columns[3:]
            scaller = MinMaxScaler()
            matrix = pd.DataFrame(scaller.fit_transform(df_series[x_calls]),columns=x_calls)
            matrix['Day'] = df_series.iloc[:, 1]
            matrix['Date'] = df_series.iloc[:, 0]
            matrix['SumView'] = df_series.iloc[:, 2].astype(int)
            matrix['CountStudent_NotNormalized'] = df_series.iloc[:, 3].astype(int)
           
            #Calculate Davies Bouldin
            results = {}    
            for i in range(2,20):
                kmeans = KMeans(n_clusters=i, random_state=30)
                matrix['cluster'] = kmeans.fit_predict(matrix[x_calls])
                db_index = davies_bouldin_score(matrix[x_calls], matrix['cluster'])
                results.update({i: db_index})
            keyList = list(results.keys())
            valueList = list(results.values())
            bouldinValue = valueList[0]
            for i in results.values():
                if (i<bouldinValue) and (i>0):
                    bouldinValue = i
            numOfCluster = keyList[valueList.index(bouldinValue)]
        
            #Cluster
            cluster = KMeans(n_clusters=numOfCluster,random_state=217)
            matrix['cluster'] = cluster.fit_predict(matrix[x_calls])
        else: 
            matrix = pd.DataFrame({
                'Date': [],
                'Day':[],
                'cluster':[],
                'CountStudent':[],
                'SumView':[],
                'CountStudent_NotNormalized':[],
            }, dtype=object)
        marker_color= np.array(matrix['cluster']).astype(int)
        cluster_date_fig.add_trace(go.Scatter(x = matrix["Day"], y = matrix["CountStudent_NotNormalized"],
                                                mode='markers',
                                                name='',
                                                text = matrix['cluster'],
                                                hovertemplate =
                                                '<i>Cluster</i>: %{text}'+
                                                '<br><i>Number of Students</i>: %{y}<br>'+
                                                '<i>%{x:$,.0f}</i>',
                                                marker_size=(matrix['CountStudent_NotNormalized']+1)*2,
                                                marker=go.Marker(#size=20,
                                                                #sizemode='diameter',
                                                                opacity=0.5, 
                                                                color=marker_color, 
                                                                #showscale = False
                                                                )))
        cluster_date_fig.add_trace(go.Scatter(x = matrix["Date"], y = matrix["CountStudent_NotNormalized"],
                                                mode='markers',
                                                name='',
                                                xaxis = "x2",
                                                text = matrix['cluster'],
                                                hovertemplate =
                                                '<i>Cluster</i>: %{text}'+
                                                '<br><i>Number of Students</i>: %{y}<br>'+
                                                '<i>%{x}</i>',
                                                marker_size=(matrix['CountStudent_NotNormalized']+1)*2,
                                                marker=go.Marker(#size=20,
                                                                #sizemode='diameter',
                                                                opacity=0.5,
                                                                color=marker_color, 
                                                                #showscale = False
                                                                )))
        cluster_date_fig.update_layout(width = 400, height=550,  margin=dict(l=0, r=0, t=60, b=35, pad=10),
                                        title={
                                            'text': "Event-data-based cluster plot",
                                            'y':0,
                                            'x':0.5,
                                            'xanchor': 'center',
                                            'yanchor': 'bottom'},
                                        yaxis=go.YAxis(showgrid=False,
                                                        zeroline=False,
                                                        showticklabels=False),
                                        #yaxis = dict (
                                         #   title="",
                                          #  titlefont=dict(
                                           #     color="#1f77b4"
                                           # ),
                                           # tickfont=dict(
                                            #    color="#1f77b4"
                                            #),
                                        #),
                                        xaxis=dict(
                                            title="Day order",
                                            titlefont=dict(
                                                color="#1f77b4"
                                            ),
                                            tickfont=dict(
                                                color="#1f77b4"
                                            ),
                                            side="top"
                                        ),
                                        xaxis2=dict(
                                            title="",
                                            titlefont=dict(
                                                color="#ff7f0e"
                                            ),
                                            tickfont=dict(
                                                color="#ff7f0e"
                                            ),
                                            anchor="free",
                                            overlaying="y",
                                            side="bottom",
                                            position=0,
                                            tickangle=-45,
                                        ),  
                                        hovermode='closest',
                                        font=dict(
                                            family="Arial",
                                            size=9,
                                            color="black"
                                        ),
                                        showlegend = False)
        
        shapes = []
        dff = df_submission[df_submission.CourseId==course_selected]
        dff['DueDates'] = pd.to_datetime(dff['DueAt'].dt.date)
        print("Due dates:      ", dff['DueDates'])
        for a_dueDate in dff['DueDates'].unique():
            if isinstance(a_dueDate, type([datetime.date])) == False: #np.isnat(a_dueDate) == False:
                print("date : ", a_dueDate)
                print("type:   ", type(a_dueDate))   
                cluster_date_fig.add_annotation(xref = "x2",
                                    x=pd.to_datetime(a_dueDate), #a_dueDate.astype('datetime64[D]'),
                                    y=dff['StudentId'].nunique(),
                                    text='Due',
                                    #yanchor='bottom',
                                    showarrow=False,
                                    font=dict(size=10, color="Purple", family="Arial"),
                                    align="center"
                                    )
                shapes.append(go.layout.Shape(type= 'line',
                                              yref= 'y', y0= 0, y1=dff['StudentId'].nunique(),
                                            xref= 'x2', x0=pd.to_datetime(a_dueDate), x1 = pd.to_datetime(a_dueDate), #x0 = a_dueDate.astype('datetime64[D]'), x1=a_dueDate.astype('datetime64[D]'),
                                            line=dict(color="Purple",
                                            width=1,
                                            dash="dot")
                            ))
        cluster_date_fig.update_layout(shapes=shapes)
    elif cluster_pattern == "Hour" and course_selected != None:
        #dff = df_submission[df_submission.CourseId==course_selected]
        sub_data_hour = data_hour[data_hour.CourseId==course_selected]
        sub_data_hour = sub_data_hour[['Hour', 'SumView', 'CountStudent']]
        sub_data_hour['SumView'] = pd.to_numeric(sub_data_hour['SumView'])
        sub_data_hour['CountStudent'] = pd.to_numeric(sub_data_hour['CountStudent'])
        sub_data_hour = sub_data_hour.sort_values('Hour', ascending=True) 
        sub_data_hour = sub_data_hour.fillna(0)

        counter_ = 0
        df_hours = pd.DataFrame({
            'Hour': [],
            'SumView':[],
            'CountStudent':[]
        }, dtype=int)

        while counter_ < 24:
            row = sub_data_hour.loc[(pd.to_numeric(sub_data_hour['Hour'], errors='coerce')) == counter_]
            column1 = pd.to_numeric(row['CountStudent'].values)
            if len(column1) > 0:
                df_hours.loc[len(df_hours.index)] = [counter_, pd.to_numeric(row['SumView'].values[0]), pd.to_numeric(row['CountStudent'].values[0])]
            else:
                df_hours.loc[len(df_hours.index)] = [counter_, 0, 0]
            counter_ += 1  
        df_hours['CountStudent'] = pd.to_numeric(df_hours['CountStudent'])
        if not df_hours.empty:
            x_calls = df_hours.columns[2:] 
        
            scaller = MinMaxScaler()
            matrix = pd.DataFrame(scaller.fit_transform(df_hours[x_calls]),columns=x_calls)
            matrix['Hour'] = df_hours.iloc[:, 0]
            matrix['SumView'] = df_hours.iloc[:, 1].astype(int)
            matrix['CountStudent_NotNormalized'] = df_hours.iloc[:, 2].astype(int)
           

            results = {}
            for i in range(2,20):
                kmeans = KMeans(n_clusters=i, random_state=30)
                matrix['cluster'] = kmeans.fit_predict(matrix[x_calls])
                db_index = davies_bouldin_score(matrix[x_calls], matrix['cluster'])
                results.update({i: db_index})
            keyList = list(results.keys())
            valueList = list(results.values())
            bouldinValue = valueList[0]
            for i in results.values():
                if (i<bouldinValue) and (i>0):
                    bouldinValue = i
            numOfCluster = keyList[valueList.index(bouldinValue)]

            cluster = KMeans(n_clusters=numOfCluster,random_state=217)
            matrix['cluster'] = cluster.fit_predict(matrix[x_calls])
        else:
            matrix = pd.DataFrame({
                'Hour': [],
                'cluster':[],
                'CountStudent':[],
                'SumView':[],
                'CountStudent_NotNormalized':[]
            }, dtype=int)

        marker_color= np.array(matrix['cluster']).astype(int)
        cluster_date_fig.add_trace(go.Scatter(x = matrix["Hour"], y = matrix["CountStudent_NotNormalized"],
                                                mode='markers',
                                                name='',
                                                text = matrix['cluster'],
                                                hovertemplate =
                                                '<i>Cluster</i>: %{text}'+
                                                '<br><i>Number of Students</i>: %{y}<br>'+
                                                '<i>Hour</i>: %{x}',
                                                marker_size=(matrix['CountStudent_NotNormalized']+1)*2,
                                                marker=go.Marker(#size=20,
                                                                #sizemode='diameter',
                                                                opacity=0.5, 
                                                                color=marker_color, 
                                                                )))
        cluster_date_fig.update_layout(width = 400, height=550, margin=dict(l=0, r=0, t=60, b=35, pad=10),
                                        title={
                                            'text': "Event-data-based cluster plot",
                                            'y':0,
                                            'x':0.5,
                                            'xanchor': 'center',
                                            'yanchor': 'bottom'},
                                        yaxis=go.YAxis(showgrid=False,
                                                        zeroline=False,
                                                        showticklabels=False),
                                        #yaxis = dict (
                                        #    title="",
                                        #    titlefont=dict(
                                        #        color="#1f77b4"
                                        #),
                                        #   tickfont=dict(
                                        #        color="#1f77b4"
                                        #    ),
                                        #),
                                        xaxis=dict(
                                            title="",
                                            titlefont=dict(
                                                color="#1f77b4"
                                            ),
                                            tickfont=dict(
                                                color="#1f77b4"
                                            ),
                                            #side="top",
                                        ),
                                        hovermode='closest',
                                        font=dict(
                                            family="Arial",
                                            size=9,
                                            color="black"
                                        ),
                                        showlegend = False)
    elif cluster_pattern == "Weekday" and course_selected != None:
        print("cluster weekday   ", cluster_pattern)
        sub_data_weekday = data_weekday[data_weekday.CourseId==course_selected]
        sub_data_weekday = sub_data_weekday[['Weekday', 'WeekdayName', 'CountStudent']]
        sub_data_weekday['Weekday'] = pd.to_numeric(sub_data_weekday['Weekday'])
        sub_data_weekday['CountStudent'] = pd.to_numeric(sub_data_weekday['CountStudent'])
        sub_data_weekday = sub_data_weekday.sort_values('Weekday', ascending=True) 
        sub_data_weekday = sub_data_weekday.fillna(0)

        counter_ = 0
        df_weekday = pd.DataFrame({
            'WeekdayName':[],
            'Weekday': [],
            'CountStudent':[]
        }, dtype=object)

        while counter_ < 7:
            if (pd.to_numeric(sub_data_weekday['Weekday']) == counter_).any():
                row = sub_data_weekday[sub_data_weekday['Weekday'] == counter_]
                df_weekday.loc[len(df_weekday.index)] = [row['WeekdayName'].values[0], counter_, row['CountStudent'].values[0]]
            else:
                df_weekday.loc[len(df_weekday.index)] = ["", counter_, 0]
            counter_ += 1
        print("df weekday ", df_weekday)
            
        if not df_weekday.empty:
            x_calls = df_weekday.columns[2:]
            scaller = MinMaxScaler()
            matrix = pd.DataFrame(scaller.fit_transform(df_weekday[x_calls]),columns=x_calls)
            matrix['Weekday'] = df_weekday.iloc[:, 1]
            matrix['WeekdayName'] = df_weekday.iloc[:, 0]
            matrix['CountStudent_NotNormalized'] = df_weekday.iloc[:, 2].astype(int)

            results = {}
            for i in range(2,6):
                kmeans = KMeans(n_clusters=i, random_state=7)
                matrix['cluster'] = kmeans.fit_predict(matrix[x_calls])
                db_index = davies_bouldin_score(matrix[x_calls], matrix['cluster'])
                results.update({i: db_index})
            keyList = list(results.keys())
            valueList = list(results.values())
            bouldinValue = valueList[0]
            for i in results.values():
                if (i<bouldinValue) and (i>0):
                    bouldinValue = i
            numOfCluster = keyList[valueList.index(bouldinValue)]

            cluster = KMeans(n_clusters=numOfCluster,random_state=7)
            matrix['cluster'] = cluster.fit_predict(matrix[x_calls])
        else:
            matrix = pd.DataFrame({
                'WeekdayName':[],
                'Weekday': [],
                'CountStudent':[],
                'cluster':[]
            }, dtype=object)
        print("matrix ", matrix)
        marker_color= np.array(matrix['cluster']).astype(int)
        cluster_date_fig.add_trace(go.Scatter(x = matrix["WeekdayName"], y = matrix["CountStudent_NotNormalized"],
                                                mode='markers',
                                                name='',
                                                text = matrix['cluster'],
                                                hovertemplate =
                                                '<i>Cluster</i>: %{text}'+
                                                '<br><i>Number of Students</i>: %{y}<br>'+
                                                '<i>Day of Week</i>: %{x}',
                                                marker_size=(matrix['CountStudent_NotNormalized']+1)*2,
                                                marker=go.Marker(
                                                                opacity=0.5, 
                                                                color=marker_color, 
                                                                )))
        cluster_date_fig.update_layout(width = 400, height=550, margin=dict(l=0, r=0, t=60, b=35, pad=10),
                                        title={
                                            'text': "Event-data-based cluster plot",
                                            'y':0,
                                            'x':0.5,
                                            'xanchor': 'center',
                                            'yanchor': 'bottom'},
                                        yaxis=go.YAxis(showgrid=False,
                                                        zeroline=False,
                                                        showticklabels=False),
                                        xaxis=dict(
                                            title="",
                                            titlefont=dict(
                                                color="#1f77b4"
                                            ),
                                            tickfont=dict(
                                                color="#1f77b4"
                                            ),
                                            #side="top",
                                        ),
                                        hovermode='closest',
                                        font=dict(
                                            family="Arial",
                                            size=9,
                                            color="black"
                                        ),
                                        showlegend = False)
    else:
        matrix = pd.DataFrame({
            'Date': [],
            'Day':[],
            'Hour':[],
            'Weekday':[],
            'WeekdayName':[],
            'cluster':[],
            'CountStudent':[],
            'SumView':[],
            'CountStudent_NotNormalized':[],
        }, dtype=object)
        cluster_date_fig = go.Figure(data=go.Scatter(x=[], y=[]))

    print("matrix 3   ", matrix)
    
    return cluster_date_fig, matrix.to_json(date_format='iso', orient='split')
    

# ======= defines callback to the bar chart =======
@app.callback(
    Output('bar_fig', 'figure'),
    Input('ddcourse', 'value'),
    Input('ribar', 'value'))

def update_bargraph(course_selected, show_pattern):
    print(type(show_pattern))
    print(show_pattern)
    if show_pattern=="Count":
        dff = df_submission_count[df_submission_count.CourseId==course_selected]
    else:
        dff = df_submission_percent[df_submission_percent.CourseId==course_selected]

    bar_fig = go.Figure()
    bar_fig.add_trace(go.Bar(
        x=dff["translatedTitle"],
        y=dff["Submitted"],
        name='Submitted',
        marker_color='lightslategrey'
    ))
    bar_fig.add_trace(go.Bar(
        x=dff["translatedTitle"],
        y=dff["NotSubmit"],
        name='Not Submit',
        marker_color='crimson'
    ))

    bar_fig.update_layout(barmode='group', xaxis_tickangle=-45, width=350, height=500,
                                        xaxis_tickfont_size=12,
                                        xaxis={'categoryorder':'category ascending'},
                                        yaxis=dict(
                                            title='Students',
                                            titlefont_size=12,
                                            tickfont_size=12,
                                        ),
                                        legend=dict(
                                            x=0,
                                            y=1.23,
                                            bgcolor='rgba(255, 255, 255, 0)',
                                            bordercolor='rgba(255, 255, 255, 0)'
                                        ),
                                    bargap=0.15, # gap between bars of adjacent location coordinates.
                                    bargroupgap=0.1,
                                    margin=dict(
                                        l=0,
                                        r=0,
                                        b=0,
                                        t=60,
                                        pad=4
                                    ))

    return bar_fig

# ======= defines callback to dynamic visualization =======
@app.callback(
    Output('dynamicDisplayArea', 'children'),
    Output('dynamicPieCharts', 'children'),
    Output('ddcourses', 'options'),
    Output('ddtype', 'disabled'),
    Input('ddcourses', 'value'),
    Input('ddpattern', 'value'),
    Input('ddtype', 'value'))
def update_multigraph(courselist, pattern, type):
    print(courselist)
    graphs = []
    piegraphs = []
    disabled = False
    if courselist != None:
        for i in courselist:
            if pattern=="Submission":
                disabled = False
                if type == "Count":
                    dff = df_submission_count[df_submission_count.CourseId==i]
                else:
                    dff = df_submission_percent[df_submission_percent.CourseId==i]
                bar_fig = go.Figure(data=[
                                            go.Bar(name='Submitted', x=dff["translatedTitle"], y=dff["Submitted"], marker_color='lightslategrey', width=0.2 ),
                                            go.Bar(name='Not Submit', x=dff["translatedTitle"], y=dff["NotSubmit"], marker_color='crimson', width=0.2)
                                        ])
                bar_fig.update_layout(barmode='group', xaxis_tickangle=-45, width=350, height=450,
                                        xaxis_tickfont_size=12,
                                        xaxis={'categoryorder':'category ascending'},
                                        yaxis=dict(
                                            title='Students',
                                            titlefont_size=12,
                                            tickfont_size=12,
                                        ),
                                        legend=dict(
                                            x=0,
                                            y=1.23,
                                            bgcolor='rgba(255, 255, 255, 0)',
                                            bordercolor='rgba(255, 255, 255, 0)'
                                        ),
                                    bargap=0.15, # gap between bars of adjacent location coordinates.
                                    bargroupgap=0.1,
                                    margin=dict(
                                        l=0,
                                        r=0,
                                        b=0,
                                        t=60,
                                        pad=4
                                    ))
                graphs.append(dcc.Graph(id='graph-{}'.format(i), figure=bar_fig))
            else:
                disabled = True
                dff_parallel_full = df_pageview[df_pageview.CourseId==i].sort_values("Result")
                dff_parallel_full['Year'] = dff_parallel_full['Year'].apply(str)
                dff_parallel_full['Month'] = dff_parallel_full['Month'].apply(str)
                dff_parallel_full['Day'] = dff_parallel_full['Day'].apply(str)
                dff_parallel_full['Week'] = dff_parallel_full['Week'].apply(str)
                dff_parallel_full['WeekdayName'] = dff_parallel_full['WeekdayName'].apply(str)
                dff_parallel_full['Hour'] = dff_parallel_full['Hour'].apply(str)
                dff_parallel_full['Minute'] = dff_parallel_full['Minute'].apply(str)

                dff_parallel = dff_parallel_full[["Year", "Month", "Day", "Result"]]

                col_list = []
                for col in dff_parallel.keys():
                    values = dff_parallel[col].unique()
                    value2dummy = dict(zip(values, range(len(values))))  # works if values are strings, otherwise we probably need to convert them
                    dff_parallel[col] = [value2dummy[v] for v in dff_parallel[col]]
                    col_dict = dict(
                        label=col,
                        categoryarray=list(value2dummy.values()),
                        ticktext=list(value2dummy.keys()),
                        values=dff_parallel[col],
                    )
                    col_list.append(col_dict)

                print("test here:   ", dff_parallel)
                color = dff_parallel.loc[:,"Result"]
                colorscale = [[0, 'lightslategrey'], [1, 'crimson']]
                paralell_fig = go.Figure(data=[go.Parcats(dimensions=col_list,  
                                        line={'color': color, 'colorscale': colorscale, 'shape': 'hspline'},
                                        hoveron='color', hoverinfo='count+probability',
                                        labelfont={'size': 12, 'family': 'Arial'},
                                        tickfont={'size': 10, 'family': 'Arial'},
                                        arrangement='perpendicular')])
                paralell_fig.update_layout(height=500, width=400, margin = dict(l=0, r=20, b=0,t=0))
                graphs.append(dcc.Graph(id='graph-{}'.format(i), figure=paralell_fig))


            # ======= builds the pie chart =======
            resultLabels = ['Completed', 'Incomplete']
            dff_Result = df_finalResult[df_finalResult.CourseId==i]
            resultValues = []
            resultValues.append(dff_Result['Completed'].values[0])
            resultValues.append(dff_Result['Incomplete'].values[0])
            print("Final result: ", dff_Result)
            print("dff_result:    ", resultValues)
            #dff_Result = dff_Result.values.flatten()
            pie_fig = go.Figure(data=[go.Pie(labels=resultLabels, 
                                            values=resultValues, 
                                            name="Course Result",
                                            textinfo='label+percent',
                                            insidetextorientation='radial')])
            pie_fig.update_traces(hoverinfo='label+percent+name', textfont_size=10, hole=.2,
                                marker=dict(colors=['lightslategrey', 'crimson'], line=dict(color='#000000', width=1)))
            pie_fig.update(layout_showlegend=False)
            pie_fig.update_layout(width = 220, height=220, margin = dict(t=10, l=0, r=0, b=0))
        
            piegraphs.append(dcc.Graph(id='piegraph-{}'.format(i), figure=pie_fig))

    # ==================set enable for droplist
    if courselist != None and len(courselist) == 3:
        courses = [{'label' : i, 'value' : j} for i, j in zip(df_courseSelection.iloc[:,3], df_courseSelection.iloc[:,0]) if j in courselist]      
    else:
        courses = opts1


    return graphs, piegraphs, courses, disabled


# ======= interactive between scatter plot and the others =======
@app.callback(
    Output('paralell_fig', 'figure'),
    Output('tableCluster', 'data'), 
    Output('tableCluster', 'columns'),
    Input('cluster_date_fig', 'selectedData'),
    Input('ddcourse', 'value'),
    Input('ddparallel', 'value'),
    Input('cluster_data', 'data'),
    Input('ddcluster', 'value'),
)
def update_interactivegraphs(slct_data, course_selected, show_pattern, cluster_data, cluster_pattern):
    df_cluster = pd.read_json(cluster_data, orient='split')
    print("df_cluster  ", df_cluster)
    if course_selected != None:
        dff_parallel_full = df_pageview[df_pageview.CourseId==course_selected].sort_values("Result")
        print("dff_parallel_full :    ", dff_parallel_full)
        dff_parallel_full['Year'] = dff_parallel_full['Year'].apply(str)
        dff_parallel_full['Month'] = dff_parallel_full['Month'].apply(str)
        dff_parallel_full['Day'] = dff_parallel_full['Day'].apply(str)
        dff_parallel_full['Week'] = dff_parallel_full['Week'].apply(str)
        dff_parallel_full['Weekday'] = dff_parallel_full['Weekday'].apply(str)
        dff_parallel_full['WeekdayName'] = dff_parallel_full['WeekdayName'].apply(str)
        dff_parallel_full['Hour'] = dff_parallel_full['Hour'].apply(str)
        dff_parallel_full['Minute'] = dff_parallel_full['Minute'].apply(str)
        
        
        if show_pattern=="Date":
            dff_parallel = dff_parallel_full[["Year", "Month", "Day", "Result"]]
        elif show_pattern=="Time":
            dff_parallel = dff_parallel_full[["Hour", "Minute", "Result"]]
        else:
            dff_parallel = dff_parallel_full[["Month", "Week", "WeekdayName", "Result"]]
    else: 
        dff_parallel = pd.DataFrame()

    if slct_data is None or len(slct_data['points']) == 0:
        print(f'selected data: {slct_data}')
        if course_selected != None:
            col_list = []
            for col in dff_parallel.keys():
                values = dff_parallel[col].unique()
                value2dummy = dict(zip(values, range(len(values))))  # works if values are strings, otherwise we probably need to convert them
                dff_parallel[col] = [value2dummy[v] for v in dff_parallel[col]]
                col_dict = dict(
                    label=col,
                    #categoryorder = "category ascending", 
                    categoryarray=list(value2dummy.values()),
                    ticktext=list(value2dummy.keys()),
                    values=dff_parallel[col],
                )
                col_list.append(col_dict)

            print("test here:   ", dff_parallel)
            color = dff_parallel.loc[:,"Result"]
            colorscale = [[0, 'lightslategrey'], [1, 'crimson']]
            paralell_fig = go.Figure(data=[go.Parcats(dimensions=col_list,  
                                    line={'color': color, 'colorscale': colorscale, 'shape': 'hspline'},
                                    hoveron='color', hoverinfo='count+probability',
                                    labelfont={'size': 12, 'family': 'Arial'},
                                    tickfont={'size': 10, 'family': 'Arial'},
                                    arrangement='perpendicular')])
            paralell_fig.update_layout(height=500, width=400, margin=dict(l=0, r=20, t=30, b=0, pad=7),)
        else: 
            paralell_fig = go.Figure(data=[go.Parcats(dimensions=[])])

        if cluster_pattern == "Day":
            dff_cluster_shown = df_cluster.loc[:,["Day", "Date", "CountStudent_NotNormalized","cluster"]]
            columns=[{"name": i, "id": i} for i in dff_cluster_shown.columns]
            columns[0]["name"] = "Order of Day"
            columns[2]["name"] = "Number of Students"
            columns[3]["name"] = "Cluster"
        elif cluster_pattern == "Hour":
            dff_cluster_shown = df_cluster.loc[:,["Hour", "CountStudent_NotNormalized","cluster"]]
            columns=[{"name": i, "id": i} for i in dff_cluster_shown.columns]
            columns[1]["name"] = "Number of Students"
            columns[2]["name"] = "Cluster"
        elif cluster_pattern == "Weekday":
            dff_cluster_shown = df_cluster.loc[:,["WeekdayName", "CountStudent_NotNormalized","cluster"]]
            columns=[{"name": i, "id": i} for i in dff_cluster_shown.columns]
            columns[0]["name"] = "Day of Week"
            columns[1]["name"] = "Number of Students"
            columns[2]["name"] = "Cluster"
        else:
            dff_cluster_shown=pd.DataFrame()
        
        data=dff_cluster_shown.to_dict('records')

        return paralell_fig, data, columns
    
    else:
        print(f'selected data: {slct_data}')
        if cluster_pattern == "Day":
            listdates = []
            for a_point in slct_data['points']:
                a_date = a_point['x']
                listdates.append(pd.to_datetime(a_date))
            print(listdates)
            
            dff_parallel_selected = pd.DataFrame()
            dff_cluster_selected = pd.DataFrame()
            df_cluster['Date'] = pd.to_datetime(df_cluster['Date']).dt.date 

            for a_point in listdates:
                temp = dff_parallel_full[dff_parallel_full.Date == a_point]
                dff_parallel_selected = dff_parallel_selected.append(temp)
                temp = df_cluster[df_cluster.Date == a_point]
                dff_cluster_selected = dff_cluster_selected.append(temp)
        elif cluster_pattern == "Hour":
            listhours = []
            for a_point in slct_data['points']:
                an_hour = a_point['x']
                listhours.append(pd.to_numeric(an_hour))
            print(listhours)
            
            dff_parallel_selected = pd.DataFrame()
            dff_cluster_selected = pd.DataFrame()
            
            dff_parallel_full['Hour'] = pd.to_numeric(dff_parallel_full['Hour'])
            for a_point in listhours:
                temp = dff_parallel_full[dff_parallel_full.Hour == a_point]
                dff_parallel_selected = dff_parallel_selected.append(temp)
                temp = df_cluster[df_cluster.Hour == a_point]
                dff_cluster_selected = dff_cluster_selected.append(temp)
        elif cluster_pattern == "Weekday":
            listweekdays = []
            for a_point in slct_data['points']:
                a_weekday = a_point['x']
                listweekdays.append(a_weekday)
            print(listweekdays)
            
            dff_parallel_selected = pd.DataFrame()
            dff_cluster_selected = pd.DataFrame()
            
            #dff_parallel_full['Weekday'] = pd.to_numeric(dff_parallel_full['Weekday'])
            for a_point in listweekdays:
                temp = dff_parallel_full[dff_parallel_full.WeekdayName == a_point]
                dff_parallel_selected = dff_parallel_selected.append(temp)
                temp = df_cluster[df_cluster.WeekdayName == a_point]
                dff_cluster_selected = dff_cluster_selected.append(temp)

        if show_pattern=="Date":
            dff_parallel = dff_parallel_selected[["Year", "Month", "Day", "Result"]]
        elif show_pattern=="Time":
            dff_parallel = dff_parallel_selected[["Hour", "Minute", "Result"]]
        else:
            dff_parallel = dff_parallel_selected[["Month", "Week", "WeekdayName", "Result"]]
        #dff_parallel_full['Hour'] = dff_parallel_full['Hour'].apply(str)
        print("dff_parallel    : ", dff_parallel)
        col_list = []
        for col in dff_parallel.keys():
            values = dff_parallel[col].unique()
            value2dummy = dict(zip(values, range(len(values))))  # works if values are strings, otherwise we probably need to convert them
            dff_parallel[col] = [value2dummy[v] for v in dff_parallel[col]]
            col_dict = dict(
                label=col,
                #categoryorder = "category ascending", 
                categoryarray=list(value2dummy.values()),
                ticktext=list(value2dummy.keys()),
                values=dff_parallel[col],
            )
            col_list.append(col_dict)

        print("test here:   ", dff_parallel)
        color = dff_parallel.loc[:,"Result"]
        colorscale = [[0, 'lightslategrey'], [1, 'crimson']]
        paralell_fig = go.Figure(data=[go.Parcats(dimensions=col_list,  
                                line={'color': color, 'colorscale': colorscale, 'shape': 'hspline'},
                                hoveron='color', hoverinfo='count+probability',
                                labelfont={'size': 12, 'family': 'Arial'},
                                tickfont={'size': 10, 'family': 'Arial'},
                                arrangement='perpendicular')])
        paralell_fig.update_layout(height=500, width=400, margin=dict(l=0, r=20, t=30, b=0, pad=7))

        if cluster_pattern == "Day":
            dff_cluster_shown = dff_cluster_selected.loc[:,["Day", "Date", "CountStudent_NotNormalized","cluster"]]
            columns=[{"name": i, "id": i} for i in dff_cluster_shown.columns]  
            columns[0]["name"] = "Order of Day"
            columns[2]["name"] = "Number of Students"
            columns[3]["name"] = "Cluster"
        elif cluster_pattern == "Hour":
            dff_cluster_shown = dff_cluster_selected.loc[:,["Hour", "CountStudent_NotNormalized","cluster"]]
            columns=[{"name": i, "id": i} for i in dff_cluster_shown.columns]
            columns[1]["name"] = "Number of Students"
            columns[2]["name"] = "Cluster"
        elif cluster_pattern == "Weekday":
            dff_cluster_shown = dff_cluster_selected.loc[:,["WeekdayName", "CountStudent_NotNormalized","cluster"]]
            columns=[{"name": i, "id": i} for i in dff_cluster_shown.columns]
            columns[0]["name"] = "Day of Week"
            columns[1]["name"] = "Number of Students"
            columns[2]["name"] = "Cluster"

        data=dff_cluster_shown.to_dict('records')
        
        #bar_fig = go.Figure(data=[go.Bar(x=[], y=[])])
        return paralell_fig, data, columns


if __name__ == '__main__':
    app.run_server(debug=True)