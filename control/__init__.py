from flask import Flask, render_template, redirect, request


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')

    from .rgb import rgb_bp, init_strips
    app.register_blueprint(rgb_bp, url_prefix='/rgb')
    init_strips()

    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=80)

