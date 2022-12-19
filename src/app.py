from flask import Flask, redirect, render_template, request
from matplotlib.pyplot import title
import func
import plotly
import plotly.express as px
import json
import yfinance as yahooFinance
import os
import wrangles

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
@app.route("/home", methods=['POST', 'GET'])
def hello_world():
    
    if request.method == 'POST':
            
        # Loading initial data
        ticker = request.form['ticker']
        time_frame = request.form.get('time', '')
        data_info = request.form.get('data_info', 'Close')
        save_data = request.form.get('save_data', '')
        # company info dictionary
        company_info = yahooFinance.Ticker(ticker).info # Not working, find a way to get stock info
        
        secret_key = os.getenv('ALPHAV_KEY', '...')
        
        try:
            # Get data from Yahoo Finance
            data_object = yahooFinance.Ticker(ticker)
            data = data_object.history(period='max')
            data.reset_index(inplace=True)
            
            
            # Getting data from x time ago
            results = func.x_month_ago(data, int(time_frame), data_info)
            results[['Open', 'High', 'Low', 'Close', 'Volume']] = results[['Open', 'High', 'Low', 'Close', 'Volume']].astype(float)
        except:
            return render_template("not_found.html", title = "Ticker Not Found")
        
        
        fig1 = px.line(results, x = 'Date', y = data_info, title = f"({ticker}) - {time_frame} Month Data")
        graph1JSON = json.dumps(fig1, cls = plotly.utils.PlotlyJSONEncoder)
        
        params = {
            'Count': results[data_info].describe().iloc[0].round(0),
            'Mean': results[data_info].describe().iloc[1].round(2),
            'Std': results[data_info].describe().iloc[2].round(2),
            'Min': results[data_info].describe().iloc[3].round(2),
            'Max': results[data_info].describe().iloc[7].round(2),
        }
        
        return render_template("home.html", graph1JSON = graph1JSON, title = "Stock Info", companyInfo = company_info, visibility = "visible" , **params)
         
    else:
        return render_template('home.html', title = "Home", visibility="hidden", companyInfo = '')
            
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')