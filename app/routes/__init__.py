from flask import Blueprint

from .user import main as user_main
from .video_player import videoPlayer

routes = Blueprint('routes', __name__)
routes.register_blueprint(user_main, url_prefix='/v1')
routes.register_blueprint(videoPlayer, url_prefix='/v1')
