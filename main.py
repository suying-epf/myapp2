def hello_world():
    prefix_google = """
<!-- Google tag (gtag.js) -->
<script async 
src="https://www.googletagmanager.com/gtag/js?id=G-MJVVD9G9FC"></script> 
<script>
    window.dataLayer = window.dataLayer || []; 
    function gtag(){dataLayer.push(arguments);} 
    gtag('js', new Date());
    gtag('config', ' YOUR_GA_CODE');
    </script>
"""
    return prefix_google + "Hello World"
    app = Flask(__name__)

    @app.route("/")
    def root():
        return "Hello from Space! 🚀"
