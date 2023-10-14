from flask import Flask, request, render_template, make_response, jsonify
import logging,requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.oauth2 import service_account
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)



app = Flask(__name__)
@app.route("/")
def root():
    return """ 
   <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Hello from Space  🚀 !</title>
            
           <!-- Google tag (gtag.js) -->
            <script async src="https://www.googletagmanager.com/gtag/js?id=G-MJVVD9G9FC"></script>
            <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());

            gtag('config', 'G-MJVVD9G9FC');
            </script>
        </head>
        <body>
            <h1>Hello from Space! 🚀</h1>
            <button id="analyticsButton">Click me to send an event</button>
                <form action="/logger" method="GET">

        <button type="submit">Go to logger </button>
    
    </form>
            <script>
                document.getElementById("analyticsButton").addEventListener("click", function () {
                    gtag('event', 'button_click', {
                        'event_category': 'Button',
                        'event_label': 'Button Clicked'
                    });
                });
            </script>
        </body>
        </html>
    """

@app.route("/logger", methods=["GET"])
def logger():

    # Log on the server side (Python)

    logging.info("This is a server-side log.")
    logging.warning('Ying SU')

    # Log on the browser side

    log_script = """

    <script>

      console.log("This is a browser-side log.");

    </script>

    """
    return render_template('textbox.html',user_message = "je suis Ying")

@app.route("/make_google_request", methods=["GET"])
def make_google_request():
    try:
        # Make a request to Google
        response = requests.get("https://www.google.com/")

        # Check if the request was successful
        if response.status_code == 200:
            return response.cookies.get_dict()
        else:
            return "Google request failed with status code: " + str(response.status_code)

    except Exception as e:
        return "An error occurred: " + str(e)
    
@app.route("/make_google_analytics_request", methods=["GET"])
def make_google_analytics_request():
    try:
        # Make a request to Google
        response = requests.get("https://analytics.google.com/analytics/web/#/p407449646/reports/intelligenthome")

        # Check if the request was successful
        if response.status_code == 200:
            return response.cookies.get_dict()
        else:
            return "Google Analytics request failed with status code: " + str(response.status_code)

    except Exception as e:
        return "An error occurred: " + str(e)

################################################################
    
# Load Google Analytics API credentials from a JSON key file
credentials = service_account.Credentials.from_service_account_file(
    'ga4-project-402014-54f684c5ca17.json',
    scopes=['https://www.googleapis.com/auth/analytics.readonly']
)
analytics = build('analyticsreporting', 'v4', credentials=credentials)

@app.route("/get_google_analytics_data", methods=["GET"])
def get_google_analytics_data():
    # Fetch data from Google Analytics
    response = analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': '407449646',
                    'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
                    'metrics': [{'expression': 'ga:users'}]
                }
            ]
        }
    ).execute()

    # Extract and display the number of users (visitors)
    data = response['reports'][0]['data']
    user_count = data['totals'][0]['values'][0]

    return f"Number of Visitors: {user_count}"



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
