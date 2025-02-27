import plotly.graph_objects as go
import dash_core_components as dcc
import plotly.express as px
import pandas as pd
import textwrap
import numpy as np
import src.algorithms.Kmeans as Kmeans
import plotly.graph_objs as pgo
from datetime import datetime

def showLineGraph_courseaccess(df, df_due):
    shapes = []
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df.Date, y=df.CountStudent, name="Number of Students",  mode='lines', line_shape='spline', text = df.CountStudent, marker=dict(color="#32CD32")))
    fig.add_trace(go.Scatter(x=df.Date, y=df.SumView, name="Sum View", yaxis='y2',  mode='markers', text = df.SumView, marker=dict(color="#2F4F4F")))
    if len(df_due.index) != 0:
        for a_dueDate in df_due['DueAt'].unique():
            if isinstance(a_dueDate, type([datetime.date])) == False and a_dueDate != None: #np.isnat(a_dueDate) == False:
                a_dueDate = pd.to_datetime(a_dueDate).tz_localize(None)
                if pd.to_datetime(df['Date']).min() <= a_dueDate <= pd.to_datetime(df['Date']).max():
                    print("date : ", a_dueDate)
                    print("type:   ", type(a_dueDate))   
                    fig.add_annotation(xref = "x",
                                        x=a_dueDate, #a_dueDate.astype('datetime64[D]'),
                                        y=df['CountStudent'].max(),
                                        text='Due',
                                        #yanchor='bottom',
                                        showarrow=False,
                                        font=dict(size=10, color="tomato", family="Arial"),
                                        align="center"
                                        )
                    shapes.append(go.layout.Shape(type= 'line',
                                                    yref= 'y', y0= 0, y1=df['CountStudent'].max(),
                                                xref= 'x', x0=a_dueDate, x1 = a_dueDate, #x0 = a_dueDate.astype('datetime64[D]'), x1=a_dueDate.astype('datetime64[D]'),
                                                line=dict(color="tomato",
                                                width=1,
                                                dash="dot")
                                ))

    fig.update_layout(
                    xaxis=dict(
                            #title=x_title,
                            #titlefont=dict(
                            #    family='Arial',
                            #    size=12,
                            #    color="rgb(150,150,150)"
                            #),
                            tickfont=dict(
                                color="rgb(150,150,150)"
                            ),
                            #tickangle=45,
                            #side="top",
                        ),
                    yaxis=dict(
                            title="Number of Students",
                            titlefont=dict(
                                family='Arial',
                                size=12,
                                color="rgb(150,150,150)"
                            ),
                            tickfont=dict(
                                color="rgb(150,150,150)"
                            ),
                            #anchor="free",
                            side="left",
                            #tickmode="sync",
                            #position=1
                    ),
                    yaxis2=dict(
                            title="Sum View",
                            titlefont=dict(
                                family='Arial',
                                size=12,
                                color="rgb(150,150,150)"
                            ),
                            tickfont=dict(
                                color="rgb(150,150,150)"
                            ),
                            overlaying="y",
                            side='right',
                            tickmode="sync",
                        ),
                    showlegend=True,
                    shapes = shapes)
    fig.update_traces(hoverinfo='text')
    #fig.update_layout(legend=dict(y=0.5, traceorder='reversed', font_size=16))
    fig.update_layout(height=550, width= 1500)
    #figs.append(dcc.Graph(id='graph-{}'.format(0), figure=fig))
    return fig

def showParallelPlot_Assignments(df): #HV
    figs = []
   
    col_list = []
    for col in df.keys():
        values = df[col].unique()
        value2dummy = dict(zip(values, range(len(values))))  # works if values are strings, otherwise we probably need to convert them
        df[col] = [value2dummy[v] for v in df[col]]
        col_dict = dict(
            label=col,
            #categoryorder = "category ascending", 
            categoryarray=list(value2dummy.values()),
            ticktext=list(value2dummy.keys()),
            values=df[col],
        )
        col_list.append(col_dict)

    # Build colorscale
    if 'Type' in df:
        color = df.Type
    else:
        color = df.Title
    #print (" color  ", color)
    colorscale = ['#F4A460', '#2F4F4F', '#00BFFF','#32CD32','#DC143C']

    fig = go.Figure(
        data=[go.Parcats(
            domain={'y': [0, 1]}, dimensions=col_list,
            line={'colorscale': colorscale, 'color': color, 'shape': 'hspline'})
        ])

    fig.update_traces(#labelfont={"size": 16, "family": "Arial"},
                    #tickfont={"size": 13, "family": "Arial"},
                    arrangement="freeform")
    fig.update_layout(height=700, width=1200, margin = dict(r = 120))
    #figs.append(dcc.Graph(id='graph-{}'.format(0), figure=fig))
    return fig

def showParallelPlot_AnalyticsQuiz(df):
    if len(df.index) != 0:
        col_list = []
        for col in df.keys():
            values = df[col].unique()
            value2dummy = dict(zip(values, range(len(values))))  # works if values are strings, otherwise we probably need to convert them
            df[col] = [value2dummy[v] for v in df[col]]
            col_dict = dict(
                label=col,
                #categoryorder = "category ascending", 
                categoryarray=list(value2dummy.values()),
                ticktext=list(value2dummy.keys()),
                values=df[col],
            )
            col_list.append(col_dict)

        # Build colorscale
        color = df.Status
        #print (" color  ", color)
        colorscale = ['#F4A460', '#2F4F4F', '#00BFFF','#32CD32','#DC143C']

        fig = go.Figure(
            data=[go.Parcats(
                domain={'y': [0, 1]}, dimensions=col_list,
                line={'colorscale': colorscale, 'color': color, 'shape': 'hspline'},
                hoveron='color', hoverinfo='count+probability',
                labelfont={'size': 12, 'family': 'Arial'},
                tickfont={'size': 10, 'family': 'Arial'},)
            ])

        fig.update_traces(arrangement="freeform")
        fig.update_layout(height=700, width=1000,) #margin = dict(r = 120))
        #figs.append(dcc.Graph(id='graph-{}'.format(0), figure=fig))
        return fig
    else:
        return go.Figure()

def updateParallelPlot_AnalyticsQuiz(df1, df2): #unused
    col_list1 = []
    for col in df1.keys():
        values = df1[col].unique()
        value2dummy = dict(zip(values, range(len(values))))  # works if values are strings, otherwise we probably need to convert them
        df1[col] = [value2dummy[v] for v in df1[col]]
        col_dict = dict(
            label=col,
            #categoryorder = "category ascending", 
            categoryarray=list(value2dummy.values()),
            ticktext=list(value2dummy.keys()),
            values=df1[col],
        )
        col_list1.append(col_dict)

    col_list2 = []
    for col in df2.keys():
        values = df2[col].unique()
        value2dummy = dict(zip(values, range(len(values))))  # works if values are strings, otherwise we probably need to convert them
        df2[col] = [value2dummy[v] for v in df2[col]]
        col_dict = dict(
            label=col,
            #categoryorder = "category ascending", 
            categoryarray=list(value2dummy.values()),
            ticktext=list(value2dummy.keys()),
            values=df2[col],
        )
        col_list2.append(col_dict)

    # Build colorscale
    color = df2.Status
    #print (" color  ", color)
    colorscale = ['#F4A460', '#2F4F4F', '#00BFFF','#32CD32','#DC143C']

    fig = go.FigureWidget(
        data=[go.Parcats(
            domain={'y': [0, 1]}, dimensions=col_list1,
            line={'colorscale': colorscale, 'color': color, 'shape': 'hspline'}),

            go.Parcats(
            domain={'y': [0, 1]}, dimensions=col_list2,
            line={'colorscale': colorscale, 'color': color, 'shape': 'hspline'})
        ])

    fig.update_traces(arrangement="freeform")
    fig.update_layout(height=1200, width=1200, margin = dict(r = 120))
    
    return fig

def update_data(fig, trace, points, state): #no use
    # Compute new color array
    new_color = np.array(fig.data[0].marker.color)
    new_color[points.point_inds] = 'Red'

    with fig.batch_update():
        # Update scatter color
        fig.data[0].line.color = new_color

        # Update parcats colors
        fig.data[1].line.color = new_color


def showParallelPlot_Quiz(df): #unused
    figs = []
   
    col_list = []
    for col in df.keys():
        values = df[col].unique()
        value2dummy = dict(zip(values, range(len(values))))  # works if values are strings, otherwise we probably need to convert them
        df[col] = [value2dummy[v] for v in df[col]]
        col_dict = dict(
            label=col,
            #categoryorder = "category ascending", 
            categoryarray=list(value2dummy.values()),
            ticktext=list(value2dummy.keys()),
            values=df[col],
        )
        col_list.append(col_dict)

    # Build colorscale
    color = df.Title
    #print (" color  ", color)
    colorscale = ['#F4A460', '#2F4F4F', '#00BFFF','#32CD32','#DC143C']
    

    fig = go.Figure(
        data=[go.Parcats(dimensions=col_list,
            line={'colorscale': colorscale, 'color': color, 'shape': 'hspline'})
        ])

    fig.update_traces(#labelfont={"size": 16, "family": "Arial"},
                    #tickfont={"size": 13, "family": "Arial"},
                    arrangement="freeform")
    fig.update_layout(height=700, width=1200, margin = dict(r = 120))
    figs.append(dcc.Graph(id='graph-{}'.format(0), figure=fig))
    return figs

def showScatterGraph_cluster(df):
    figs = []
    df = df[['StudentId', 'Late', 'Missing', 'Attempts', 'Grade']]
    df = df.fillna(0)
    print("df ", df)
    n_clusters = 5
   
    model, Z, df_X_reduced = Kmeans.cluster(df, n_clusters)  

    df['Grade']=df['Grade'].apply(lambda x: float(x))
    trace0 = pgo.Scatter(x=df_X_reduced[0],#df['Attempts'],
                        y=df_X_reduced[1],
                        text=Z,
                        name='',
                        mode='markers',
                        hovertemplate='<i>Cluster</i>: %{text}',#+'<br>Grade: %{text} <br>Attempts: %{x}',
                        marker=pgo.Marker(size=df['Grade'],
                                        sizemode='diameter',
                                        sizeref=df['Grade'].max()/50,
                                        opacity=0.5,
                                        color=Z),
                        showlegend=False
                        ) 
    
    trace1 = pgo.Scatter(x=model.cluster_centers_[:, 0],
                     y=model.cluster_centers_[:, 1],
                     name='',
                     mode='markers',
                     marker=pgo.Marker(symbol='x',
                                       size=12,
                                       color=Z),
                     showlegend=False
    )
    data7 = pgo.Data([trace0, trace1])
    layout5 = pgo.Layout(
                     xaxis=pgo.XAxis(showgrid=False,
                                     zeroline=False,
                                     showticklabels=False),
                     yaxis=pgo.YAxis(showgrid=False,
                                     zeroline=False,
                                     showticklabels=False),
                     hovermode='closest'
    )
    layout7 = layout5
    layout7['title'] = 'Quiz clusters'
    fig = pgo.Figure(data=data7, layout=layout7)
    fig.update_layout(width=1500)
    figs.append(dcc.Graph(id='graph-{}'.format(0), figure=fig))
    return figs

def showBarGraph(df):
    figs = []

    fig = go.Figure()
    for i in df['Status'].unique():
        df_temp = df[df.Status==i]
        fig.add_trace(go.Bar(x=df_temp['Title'], 
                             y=df_temp['RateStudent'], 
                             name=str(df_temp['Status'].values[0]), 
                             customdata=np.transpose([df_temp['Status'], df_temp['RateStudent']]),
                            showlegend=False,
                    ))
        fig.add_trace(go.Bar(x=df_temp['Title'], 
                             y=df_temp['CountStudent'], 
                             name=str(df_temp['Status'].values[0]), 
                             customdata=np.transpose([df_temp['Status'], df_temp['RateStudent']]),
                             yaxis='y2',
                             showlegend=True,
                             texttemplate="%{customdata[1]:.1f}%",
                            textposition="inside",
                            hovertemplate="<br>".join([
                                "%{x}",
                                "Percent of Students: %{customdata[1]:.2f}",
                                "Number of Students: %{y}",
                                "Status: %{customdata[0]}",
                            ])
                    ))

    fig.update_layout(barmode='stack',
                    xaxis=dict(
                            titlefont=dict(
                                family='Arial',
                                size=12,
                                color="rgb(150,150,150)"
                            ),
                            tickfont=dict(
                                color="rgb(150,150,150)"
                            ),
                            tickangle=35,
                            #side="top",
                        ),
                    yaxis=dict(
                        title='Percentage',
                        titlefont_size=12,
                        tickfont_size=12,
                    ),
                    yaxis2=dict(
                        title='Number of Students',
                        side="right",
                        overlaying="y",
                        tickmode="sync",
                    ),
                    legend=dict(
                        yanchor="top",
                        y=1,
                        xanchor="right",
                        x=1.5
                    ),
                    bargap=0.15,
                    height=600, width=400, margin=dict(l=0, r=0, t=0, b=0, pad=0),)
    
    #figs.append(dcc.Graph(id='graph-{}'.format(0), figure=fig))
    return fig

def showBarGraph_HV(df): #for HV course
    figs = []
    colors = {'Discussion':'#FFC0CB','Assignment':'#FFD700','Quiz':'#00BFFF','File':'#32CD32','Others':'#E6E6FA'}
    fig = px.bar(df, x = df.Title, y = df.CountStudent,
             color = df.Type,
             category_orders = df.Type,
             color_discrete_map = colors,
             text=df.CountStudent)
    fig.update_layout(height=700, width=700, margin=dict(l=0, r=0, t=0, b=0, pad=0),)
    #figs.append(dcc.Graph(id='graph-{}'.format(0), figure=fig))
    return fig

def showLineGraph_individualcourseaccess(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.AccessedDate, y=df.ViewCount, name="Page View",  mode='markers', marker=dict(color="#32CD32")))
    fig.update_layout(
                    xaxis=dict(
                            tickfont=dict(
                                color="rgb(150,150,150)"
                            ),
                        ),
                    yaxis=dict(
                            title="View Count",
                            titlefont=dict(
                                family='Arial',
                                size=12,
                                color="rgb(150,150,150)"
                            ),
                            tickfont=dict(
                                color="rgb(150,150,150)"
                            ),
                    ),
                    showlegend=False)
    fig.update_traces(hoverinfo='text')
    fig.update_layout(height=550, width= 700)
    return fig