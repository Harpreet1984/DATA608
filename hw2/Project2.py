import datashader as ds
import datashader.transfer_functions as tf
import datashader.glyphs
from datashader import reductions
from datashader.core import bypixel
from datashader.utils import lnglat_to_meters as webm, export_image
from datashader.colors import colormap_select, Greys9, viridis, inferno
import copy


from pyproj import Proj, transform
import numpy as np
import pandas as pd
import urllib
import json
import datetime
#import colorlover as cl

import plotly.plotly as py
import plotly.graph_objs as go
from plotly import tools

from shapely.geometry import Point, Polygon, shape
from functools import partial

from IPython.display import GeoJSON

bk = pd.read_csv('nyc_pluto_18v1/PLUTO_for_WEB/BK_18v1.csv')
bx = pd.read_csv('nyc_pluto_18v1/PLUTO_for_WEB/BX_18v1.csv')
mn = pd.read_csv('nyc_pluto_18v1/PLUTO_for_WEB/MN_18v1.csv')
qn = pd.read_csv('nyc_pluto_18v1/PLUTO_for_WEB/QN_18v1.csv')
si = pd.read_csv('nyc_pluto_18v1/PLUTO_for_WEB/SI_18v1.csv')

ny = pd.concat([bk, bx, mn, qn, si], ignore_index=True)

# Getting rid of some outliers
ny = ny[(ny['YearBuilt'] > 1850) & (ny['YearBuilt'] < 2020) & (ny['NumFloors'] != 0)]


wgs84 = Proj("+proj=longlat +ellps=GRS80 +datum=NAD83 +no_defs")
nyli = Proj("+proj=lcc +lat_1=40.66666666666666 +lat_2=41.03333333333333 +lat_0=40.16666666666666 +lon_0=-74 +x_0=300000 +y_0=0 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs")
ny['XCoord'] = 0.3048*ny['XCoord']
ny['YCoord'] = 0.3048*ny['YCoord']
ny['lon'], ny['lat'] = transform(nyli, wgs84, ny['XCoord'].values, ny['YCoord'].values)

ny = ny[(ny['lon'] < -60) & (ny['lon'] > -100) & (ny['lat'] < 60) & (ny['lat'] > 20)]

#Defining some helper functions for DataShader
background = "black"
export = partial(export_image, background = background, export_path="export")
cm = partial(colormap_select, reverse=(background!="black"))


trace = go.Scatter(
    # I'm choosing BBL here because I know it's a unique key.
    x = ny.groupby('YearBuilt').count()['BBL'].index,
    y = ny.groupby('YearBuilt').count()['BBL']
)

layout = go.Layout(
    xaxis = dict(title = 'Year Built'),
    yaxis = dict(title = 'Number of Lots Built')
)

fig = go.Figure(data = [trace], layout = layout)

py.iplot(fig, filename = 'ny-year-built')

############Question 1  Start ########################################
#create a drived column based on the year built and the number of floors
ny['YearBuilt_NumFloors']  =ny['YearBuilt'].astype(str) +'-' + ny['NumFloors'].astype(str)
traceQ1 = go.Scatter(
    # choosing derived column because it's a unique key.
    x = ny.groupby(['YearBuilt_NumFloors']).count()['NumBldgs'].index,
    y = ny.groupby(['YearBuilt_NumFloors']).count()['NumBldgs']
)


layoutQ1 = go.Layout(
    xaxis = dict(title = 'Year Built & Number of floors'),
    yaxis = dict(title = 'Number of Buildings')
)

figQ1 = go.Figure(data = [traceQ1], layout = layoutQ1)
#Graph shows how many buildings of a certain number of floors based on the year.
py.iplot(figQ1, filename = 'ny-No-Of-Buildings')

#Strategy to bin buildings with an interval of 10
buidingbins = 10
buildingCut = pd.cut(ny.groupby(['YearBuilt_NumFloors']), np.logspace(1, np.log(ny.groupby(['YearBuilt_NumFloors']).count()['NumBldgs'].max()), buidingbins))


############Question 1  END ########################################

cvs = ds.Canvas(800, 500, x_range = (ny['YearBuilt'].min(), ny['YearBuilt'].max()), 
                                y_range = (ny['NumFloors'].min(), ny['NumFloors'].max()))
agg = cvs.points(ny, 'YearBuilt', 'NumFloors')
view = tf.shade(agg, cmap = cm(Greys9), how='log')
export(tf.spread(view, px=2), 'yearvsnumfloors')

NewYorkCity   = (( -74.29,  -73.69), (40.49, 40.92))
cvs = ds.Canvas(700, 700, *NewYorkCity)
agg = cvs.points(ny, 'lon', 'lat')
view = tf.shade(agg, cmap = cm(inferno), how='log')
export(tf.spread(view, px=2), 'firery')


############Question 2  Start ########################################

#Calculate AssessStructure value
ny['AssessStructure']  =ny['AssessTot'] - ny['AssessLand']
landbins = 100
structurebins = 100

landCut = pd.cut(ny['AssessLand'], np.linspace(ny['AssessLand'].min(), ny['AssessLand'].max(), landbins))
StructureCut = pd.cut(ny['AssessStructure'], np.logspace(1, np.log(ny['AssessStructure'].max()), structurebins))

xlabelsQ2 = np.floor(np.linspace(ny['AssessLand'].min(), ny['AssessLand'].max(), landbins))
ylabelsQ2 = np.floor(np.linspace(ny['AssessStructure'].min(), ny['AssessStructure'].max(), structurebins))

dataQ2 = [
    go.Heatmap(z = ny.groupby([landCut, StructureCut])['BBL'].count().unstack().fillna(0).values,
              colorscale = 'Greens', x = xlabelsQ2, y = ylabelsQ2)
]

py.iplot(dataQ2, filename = 'datashaderQ2-2d-hist')

############Question 2  END #########################################