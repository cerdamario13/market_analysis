from flask import Flask, render_template, request, jsonify
import func

app = Flask(__name__)

@app.route("/home", methods=['GET'])
def hello_world():
    return render_template('home.html')
        
@app.route("/time2_ago", methods=['POST'])
def time2_ago():
    
    # Loading initial data
    ticker = request.args.get('ticker')
    data = func.ticker_data_all(ticker)
    
    time_frame = request.args.get('time')
    data_info = request.args.get('data_info')
    
    # Getting data from x time ago
    results = func.x_month_ago(data, int(time_frame), data_info)
    
    return jsonify(results.tolist())
    
if __name__ == '__main__':
    app.run(debug=False, port=8000, host='0.0.0.0')