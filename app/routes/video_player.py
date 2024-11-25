from flask import Blueprint, jsonify, request
from flask.views import MethodView

from ..extensions import db
from ..models.video_player import VideoPlayer

videoPlayer = Blueprint('videoPlayer', __name__)


class VideoPlayers(MethodView):

    def get(self):
        video_players = VideoPlayer.query.all()
        user_obj = [
            {
                "id": video_player.id,
                "name": video_player.name,
                "autoPlay": video_player.autoPlay,
                "showIcon": video_player.showIcon
            }
            for video_player in video_players
        ]

        return jsonify(user_obj), 200

    def post(self):
        req: dict = request.get_json()

        validation_error = validate_user_input(req)
        if validation_error:
            return jsonify(validation_error), 400

        name = req.get("name")
        auto_play = req.get("autoPlay", False)
        show_icon = req.get("showIcon", False)

        existing_user = VideoPlayer.query.filter_by(name=name).first()
        if existing_user:
            return jsonify({"message": "Video player already exists"}), 400

        video_player = VideoPlayer(name=name, autoPlay=auto_play, showIcon=show_icon)
        try:
            db.session.add(video_player)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Database error occurred", "error": str(e)}), 500

        return jsonify({"id": video_player.id, "name": video_player.name, "autoPlay": video_player.autoPlay,
                        "showIcon": video_player.showIcon}), 201

    def put(self, video_player_id):
        req = request.get_json()

        # Find the existing video player
        video_player = VideoPlayer.query.get(video_player_id)
        if not video_player:
            return jsonify({"message": "VideoPlayer not found"}), 404

        # Update fields if they exist in the request
        if "name" in req:
            video_player.name = req["name"]
        if "autoPlay" in req:
            video_player.autoPlay = req["autoPlay"]
        if "showIcon" in req:
            video_player.showIcon = req["showIcon"]

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Database error occurred", "error": str(e)}), 500

        return jsonify({
            "id": video_player.id,
            "name": video_player.name,
            "autoPlay": video_player.autoPlay,
            "showIcon": video_player.showIcon
        }), 200

    def delete(self, video_player_id):
        video_player = VideoPlayer.query.get(video_player_id)
        if not video_player:
            return jsonify({"message": "Video player not found"}), 404

        try:
            db.session.delete(video_player)
            db.session.commit()
            return jsonify({"message": f"Video player with id {video_player_id} deleted successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Error occurred while deleting video player", "error": str(e)}), 500

    def validate_user_input(req):
        required_fields = ['name', 'autoPlay', 'showIcon']
        for field in required_fields:
            if field not in req:
                return {"message": f"{field} is required"}, 400
        return None


videoPlayer.add_url_rule('/video-player/<int:video_player_id>', view_func=VideoPlayers.as_view('videoPlayer_delete'),
                         methods=['DELETE'])
videoPlayer.add_url_rule('/video-player/<int:video_player_id>', view_func=VideoPlayers.as_view('videoPlayer_put'),
                         methods=['PUT'])
videoPlayer.add_url_rule('/video-players', view_func=VideoPlayers.as_view('videoPlayer'))
