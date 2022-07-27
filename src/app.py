from flask import Flask, redirect, render_template, request, jsonify, url_for
from matplotlib.pyplot import title
import func
import plotly
import plotly.express as px
import json
import yfinance as yahooFinance

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
@app.route("/home", methods=['POST', 'GET'])
def hello_world():
    
    if request.method == 'POST':
            
        # Loading initial data
        ticker = request.form['ticker']
        time_frame = request.form['time']
        data_info = request.form['data_info']
        # company info dictionary
        company_info = yahooFinance.Ticker(ticker).info
        
        try:
            data = func.ticker_data_all(ticker)
            # Getting data from x time ago
            results = func.x_month_ago(data, int(time_frame), data_info)
        except:
            return render_template("not_found.html", title = "Ticker Not Found")
        
        
        fig1 = px.line(results, x = 'Date', y = data_info, title = f"{company_info['shortName']} ({ticker}) - {time_frame} Month Data")
        graph1JSON = json.dumps(fig1, cls = plotly.utils.PlotlyJSONEncoder)
        
        params = {
            'Count': results[data_info].describe().iloc[0].round(0),
            'Mean': results[data_info].describe().iloc[1].round(2),
            'Std': results[data_info].describe().iloc[2].round(2),
            'Min': results[data_info].describe().iloc[3].round(2),
            'Max': results[data_info].describe().iloc[7].round(2),
        }
        
        return render_template("index.html", graph1JSON = graph1JSON, title = "Stock Info", companyInfo = company_info, **params)
         
    else:
        return render_template('home.html', title = "Home")
        
            
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')