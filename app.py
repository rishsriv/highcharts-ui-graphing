#!/usr/bin/python
 # -*- coding: utf-8 -*-
import os
from flask import Flask, request, render_template, redirect, render_template_string, jsonify
import pandas as pd
import numpy as np
import json
import re

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def input_data():
    if request.method == 'GET':
        return render_template('chart.html')
    elif request.method == 'POST':
        data = request.form.get('input_data', None)
        title = request.form.get('title', '')
        subtitle = request.form.get('subtitle', '')
        yaxisunit = request.form.get('yaxisunit', '')
        chart_type = request.form.get('chart_type', 'line')
        #colors
        data = np.array(json.loads(data.replace('null', '""')))
        row, col = np.shape(data)
        data = data[:(row-1),:(col-1)]
        data = pd.DataFrame(data)
        cols = data.iloc[0]
        data.columns = cols
        cols_to_use = []
        cols_to_use = [col for col in cols if col.lstrip().rstrip() != ""]
        data = data[cols_to_use]
        data = data[1:]
        cols = data.columns.tolist()
        return_obj = {}
        return_obj['categories'] = data[cols[0]].tolist()
        def to_float(x):
            try:
                return float(x)
            except:
                return 0
        for i in cols[1:]:
        	data[i] = data[i].apply(to_float)
        if chart_type != 'pie':
        	return_obj['series'] = [{'name': cols[i], 'data': data[cols[i]].tolist()} for i in range(1,len(cols))]
        else:
        	groups = data[cols[0]].tolist()
        	values = data[cols[1]].tolist()
        	return_obj['series'] = [{'data': [{'name': groups[i], 'y': values[i]} for i in range(len(groups))],
        	'name': cols[1]}]
        return_obj['category_text'] = cols[0]
        return_obj['title'] = title
        return_obj['subtitle'] = subtitle
        return_obj['yaxisunit'] = yaxisunit
        return_obj['chart_type'] = chart_type
        return jsonify(return_obj)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000)