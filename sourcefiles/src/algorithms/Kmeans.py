from sklearn.cluster import KMeans
from sklearn.metrics import davies_bouldin_score
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import numpy as np
import plotly.graph_objs as pgo
import dash_core_components as dcc

def Kmeans (df):
    x_calls = df.columns[1:]

    scaller = MinMaxScaler()
    matrix = pd.DataFrame(scaller.fit_transform(df[x_calls]),columns=x_calls)
    matrix['Late'] = df.iloc[:, 1]
    matrix['Missing'] = df.iloc[:, 2]
    matrix['Attempts'] = df.iloc[:, 3].astype(int)
    matrix['Grade'] = df.iloc[:, 4].astype(int)
    
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

def functionPCA(df):
    X = np.array(df)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    pca = PCA()
    pca.fit(X_scaled)
    pca.n_components = 3
    X_reduced = pca.fit_transform(X_scaled)
    print("X_reduced ", X_reduced)
    df_X_reduced = pd.DataFrame(X_reduced, index=df.index)
    return X_reduced, df_X_reduced

def cluster(df, n_clusters):
    X_reduced, df_X_reduced = functionPCA(df)

    """ results = {}    
    for i in range(2,20):
        kmeans = KMeans(n_clusters=i)
        Z = kmeans.fit_predict(X_reduced)
        db_index = davies_bouldin_score(X_reduced, Z)
        results.update({i: db_index})
    keyList = list(results.keys())
    valueList = list(results.values())
    bouldinValue = valueList[0]
    for i in results.values():
        if (i<bouldinValue) and (i>0):
            bouldinValue = i
    n_clusters = keyList[valueList.index(bouldinValue)] """

    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(X_reduced)
    Z = kmeans.predict(X_reduced)

    print ("kmeans ", kmeans)
    print("z ", Z)
    return kmeans, Z, df_X_reduced

""" def check_clusters(df):

    

    max_clusters = len(df)
    inertias = np.zeros(max_clusters)
    figs = []
    for i in range(1, max_clusters):
        kmeans, Z, df_X_reduced = cluster(df, i)
        inertias[i] = kmeans.inertia_ 
        data = pgo.Data([
                pgo.Scatter(
                        x=range(1, max_clusters),
                        y=inertias[1:]
                )
            ])  
        layout = pgo.Layout(
            title='Baltimore dataset - Investigate k-means clustering',
            xaxis=pgo.XAxis(title='Number of clusters',
                            range=[0, max_clusters]),
            yaxis=pgo.YAxis(title='Inertia')
        )
        
        fig = pgo.Figure(data=data, layout=layout)
        figs.append(dcc.Graph(id='graph-{}'.format(0), figure=fig))
    return figs """