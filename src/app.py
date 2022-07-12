from flask import Flask, redirect, render_template, request, jsonify, url_for
import func
import plotly
import plotly.express as px
import json

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
@app.route("/home", methods=['POST', 'GET'])
def hello_world():
    
    if request.method == 'POST':
            
        # Loading initial data
        ticker = request.form['ticker']
        time_frame = request.form['time']
        data_info = request.form['data_info']
        data = func.ticker_data_all(ticker)
        # Getting data from x time ago
        results = func.x_month_ago(data, int(time_frame), data_info)
        # return jsonify(results.tolist())
        
        fig = px.bar(results)
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
        
        return render_template('base.html', graphJSON=graphJSON)
    else:
        return render_template('base.html')
        
@app.route("/new")
def test_new():
    return render_template('new.html')
    
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')