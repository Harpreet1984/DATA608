# -*- coding: utf-8 -*-
"""
DATA 608 Final Project: Canadian Household Debt
Authors:
    Harpreet Shoker
"""

from flask import Flask, render_template, request
import json
import numpy as np
import pandas as pd


app = Flask(__name__)
app.debug = True

class Recommender:

    item_similarity_top_k = 0
    def __init__(self):
        data = pd.read_csv("/home/ec2-user/608/data608-final-project/data/Survey_of_financial_security_2005.csv")
        data_mod_1 = data[data["wdprmor"] != 0]
        data_mod_2 = data_mod_1[data_mod_1["wdprmor"] < 1000000]
        self.data = data_mod_2[data_mod_2["wdprmor"] != 0]

    # Create dashboard visuals
    # Data is gathered from a MYSQL Database on EC2 and sent to the browser and vsiuals are generated using Highcharts.js
    def getVisuals(self, region):

        total_count=0
        mean=0
        median=0
        standard_deviation=0
        if (region == "3"):
            data_df = self.data[self.data["region"] == 3]
            total_count=522
            mean=182874
            median=146000
            standard_deviation=164889
        elif (region == "2"):
            data_df = self.data[self.data["region"] == 2]
            total_count=286
            mean=119583
            median=82687
            standard_deviation=134083
        elif (region == "5"):
            data_df = self.data[self.data["region"] == 5]
            total_count=262
            mean=207749
            median=151675
            standard_deviation=235455

        elif (region == "4"):
            data_df = self.data[self.data["region"] == 4]
            total_count=480
            mean=129137
            median=994750
            standard_deviation=126850

        descriptive_stat= {"success":True}

        debt_primary_mortgage = {"success":True,"data":[]}
        for index, row in data_df.iterrows():
            debt_primary_mortgage['data'].append([row["wdtotal"],row["wdprmor"]])

        debt_household_earners = {"success":True,"data":[]}
        quebec_grouped_earner = data_df.groupby('nbear27')
        quebec_grouped_earner_aggr = quebec_grouped_earner['wdtotal'].agg([np.sum])
        for name in quebec_grouped_earner_aggr.index:
            debt_household_earners['data'].append({"name": name,"y":int(quebec_grouped_earner_aggr.loc[name]["sum"])})


        debt_student_loan = {"success":True,"data":[]}
        for index, row in data_df.iterrows():
            debt_student_loan['data'].append([row["wdtotal"],row["wdsloan"]])



        debt_male_female = {"success":True,"data":[]}
        quebec_grouped_sex = data_df.groupby('hcsex_r')
        quebec_grouped_sex_aggr = quebec_grouped_sex['wdtotal'].agg([np.sum])
        for name in quebec_grouped_sex_aggr.index:
            #debt_male_female ['data'].append([int(quebec_grouped_sex_aggr.loc[name]["sum"]), name])
            debt_male_female ['data'].append({"name": name, "y": int(quebec_grouped_sex_aggr.loc[name]["sum"])})


        return {"descriptive_stat":descriptive_stat, "total_count":total_count, "mean":mean, "median": median, "standard_deviation":standard_deviation, "debt_primary_mortgage" : debt_primary_mortgage ,
        "debt_household_earners": debt_household_earners, "debt_student_loan": debt_student_loan, "debt_male_female": debt_male_female}


    # Get a sample of users to reduce load on the interface
    def sampleUsers(self):
        users = np.array(list(self.item_similarity_top_k['user_id']))
        users = np.unique(users)
        users = np.random.choice(users, 10, replace=False).reshape(10,1).tolist()
        return {"success":True, "data":users}


recommender = Recommender()

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/ontarioDashboard")
def dashboard():
    return render_template('index.html')

@app.route("/bcDashboard")
def bcDashboard():
    return render_template('bcIndex.html')

@app.route("/quebecDashboard")
def quebecDashboard():
    return render_template('qeIndex.html')

@app.route("/albertaDashboard")
def albertaDashboard():
    return render_template('alIndex.html')

@app.route("/canadaDashboard")
def canadaDashboard():
    return render_template('index.html')


@app.route("/getGraphics",methods=['GET'])
def getGraphics():
    graphics = recommender.getVisuals("3")
    return json.dumps(graphics)

@app.route("/getGraphicsBC",methods=['GET'])
def getGraphicsBC():
    graphics = recommender.getVisuals("5")
    return json.dumps(graphics)

@app.route("/getGraphicsQE",methods=['GET'])
def getGraphicsQE():
    graphics = recommender.getVisuals("2")
    return json.dumps(graphics)

@app.route("/getGraphicsAL",methods=['GET'])
def getGraphicsAL():
    graphics = recommender.getVisuals("4")
    return json.dumps(graphics)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
