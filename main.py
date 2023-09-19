from flask import Flask

app = Flask(__name__)


'''
@app.route("/")
def hello_world():
    prefix_google = """
    <!-- Google tag (gtag.js) -->
    <script async 
    src="https://www.googletagmanager.com/gtag/js?id=G-MJVVD9G9FC"></script> 
    <script>
        window.dataLayer = window.dataLayer || []; 
        function gtag(){dataLayer.push(arguments);} 
        gtag('js', new Date());
        gtag('config', ' G-MJVVD9G9FC');
    </script>
    
"""
    return prefix_google + "Hello World"
'''


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


if __name__ == "__main__":
    app.run(debug=True)
