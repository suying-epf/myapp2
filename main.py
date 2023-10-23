from google.oauth2 import service_account
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.oauth2 import service_account
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)
import logging,requests,sys
from html import unescape
from flask import Flask, render_template, request
import json
from datetime import datetime,timedelta
from pytrends.request import TrendReq



# Create a Flask web application
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)
logs = []


credentials = service_account.Credentials.from_service_account_file(
    'ga4-project-402014-54f684c5ca17.json', scopes=['https://www.googleapis.com/auth/analytics.readonly']
)


def sample_run_report():
    """Runs a simple report on a Google Analytics 4 property."""
    user_count = 0
    property_id = "407449646"
    client = BetaAnalyticsDataClient(credentials=credentials)

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="country")],
        metrics=[Metric(name="activeUsers")],
        date_ranges=[DateRange(start_date="2023-03-31", end_date="today")],
    )
    response = client.run_report(request)

    for row in response.rows:
        user_count += int(row.metric_values[0].value)

    return user_count

# Define a route for the homepage
@app.route('/')
def root():
    return render_template("index.html")

@app.route('/logger', methods=['GET', 'POST'])
def logger_page():
    log_message ='This a log message'
    logger.info('This is a log message!')
    response_message = "This is a response"
    user_count = sample_run_report()
    
    if request.method == 'POST' and 'log_message' in request.form:
        log_message = request.form.get('log_message')
        logger.info(log_message)
        # return render_template('logger.html', logs=log_message)
    
    if request.method == 'POST' and request.form.get('action') == 'Google':
            response = requests.get("https://www.google.com")  
            if response.status_code == 200:
                response_message = response.cookies.get_dict()
            else:
                response_message = "Request to Google failed."
            
            # return render_template("logger.html", logs=log_message,response_message=response_message)
    
    if request.method == 'POST' and request.form.get('action') == 'ganalytics':
        response = requests.get("https://analytics.google.com/analytics/web/#/p407490614/reports/intelligenthome")
        if response.status_code == 200:
            response_message = response.text
        else:
            response_message = "Request to Google failed."

        # return render_template("logger.html", logs=log_message,response_message=response_message)
    
    return render_template("logger.html", logs=log_message,response_message=response_message, user_count=user_count)
    
# Initialize pytrends
pytrends = TrendReq(hl='en-US', tz=360)

def get_google_trends(keywords, start_date, end_date):
    pytrends.build_payload(keywords, cat=0, timeframe=f'{start_date} {end_date}', geo='', gprop='')
    return pytrends.interest_over_time()

@app.route('/trends', methods=['GET', 'POST'])
def trends_page():
    data = {}
    keywords = ["Apple", "Orange"]  # replace with your desired keywords
    if request.method == 'POST':
        today = datetime.now().date()
        start_date = today - timedelta(days=90)
        df = get_google_trends(keywords, start_date.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d"))
        print("df=",df)
        data = {
            'dates': list(df.index.strftime('%Y-%m-%d')),
            'values': {keyword: list(df[keyword]) for keyword in keywords}
        }
        print("data=",data)
    data_json = json.dumps(data)
    return render_template("trends.html", data_json=data_json)


# Run the application
if __name__ == '__main__':
    app.run(debug=True)