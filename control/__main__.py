from flask import Flask, render_template, redirect, request






def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')

    from .rgb import rgb_bp
    app.register_blueprint(rgb_bp, url_prefix='/rgb')

    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0')

