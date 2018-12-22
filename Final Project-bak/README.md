

## Project Title:
### Canadian Household Debt Dashboard
Canada is currently experiencing record-breaking levels of household debt. Consumer spending is central to the Canadian economy and therefore to financial stability. However, with the household debt ratio reaching 163%1 there is a growing concern that households debts are overextended.
In this project I would like to create a observational dashboard to see what contributes to the household debts.
While creating this dashboard, i wanted to answer following research questions,
1.How much debt does an average Canadian household have, across various regions.
2.what kind of factors are contributing the most to the household debt?
3.How does the debt profile varies across different regions?

## Pre-requisites:

#### Libraries:
numpy

matplotlib

flask

pandas

requests

Javascript Highchart library

Bootstrap webframework

## Url for App:

http://ec2-3-82-192-160.compute-1.amazonaws.com:5000/

## How it works:

The app is designed with two tabs:

### 1) Dashboard:
Dashboard mentions details three visuals and summary of dataset provided.
a) Total sample size for the area in the survey.
b) Mean and Medium household debt in this region
c) I have also included standard deviation which specifies the spread for the samples.


### 2) Statistics Graph
a) Primary Mortgage VS Household debt.
b) Household earners VS Household debt.
c) Male/Female debt VS Household debt.
d) Student debt VS Household debt.


### Input Data
For this project, i found 2005 survey of Financial security, which is a canada wide survey that uses 5276 households represent 12.5 million canadian population. There were initially 82 factor but i trimmed down to 4 by running linear regression algorithm. These four are
a) Primary Mortgage held by a household.
b) Total number of earner in the household.
c) Total Student load in the household.
d) Primary income generator, Male or Female.

## Built with:

Python 3.0 Flask Framework

Web Framework : Bootstrap(https://getbootstrap.com/. )

Handling requests(Flask Application) : JQuery and custom Javascript

Plots :Javascript library Highcharts.js(https://www.highcharts.com/)

Data storage: MySQL


## License:
CUNY DATA608 Final Project

## Development:
Harpreet Shoker
