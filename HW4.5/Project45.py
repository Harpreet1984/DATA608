#!flask/bin/python
from flask import Flask,  jsonify, abort, make_response
import pandas as pd

app = Flask(__name__)

#@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
@app.route('/project4.5/api/v1.0/species_count/<string:boro>', methods=['GET'])
def get_trees(boro):
    #boro = 'Bronx'
    soql_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=spc_common,count(tree_id)' +\
        '&$where=boroname=\'' + boro + '\'' +\
        '&$group=spc_common').replace(' ', '%20')
    soql_trees = pd.read_json(soql_url)
    if soql_trees.empty:
        abort(404)
    return jsonify(soql_trees.to_json())


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)
    

#Here are few valid requests
     #curl http://localhost:5000/project4.5/api/v1.0/species_count/Brooklyn
     #curl http://localhost:5000/project4.5/api/v1.0/species_count/Bronx

#Here are some invalid request, this will show 404 error
     #curl http://localhost:5000/project4.5/api/v1.0/species_count/abc
