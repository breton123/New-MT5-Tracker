from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Page Routes
    from .routes.account import account_bp
    from .routes.config import config_bp
    from .routes.createAccount import createAccount_bp
    from .routes.errorLog import errorLog_bp
    from .routes.index import index_bp
    from .routes.setLoader import setLoader_bp
    
    # API Routes
    from .routes.api.copyToAccount import copyToAccount_bp
    from .routes.api.deleteSet import deleteSet_bp
    from .routes.api.getProfileSets import getProfileSets_bp
    from .routes.api.uploadSets import uploadSets_bp
    from .routes.api.downloadCSV import downloadCSV_bp
   

    
    app.register_blueprint(account_bp)
    app.register_blueprint(config_bp)
    app.register_blueprint(createAccount_bp)
    app.register_blueprint(errorLog_bp)
    app.register_blueprint(index_bp)
    app.register_blueprint(setLoader_bp)
    
    app.register_blueprint(copyToAccount_bp)
    app.register_blueprint(deleteSet_bp)
    app.register_blueprint(getProfileSets_bp)
    app.register_blueprint(uploadSets_bp)
    app.register_blueprint(downloadCSV_bp)
    
    return app
