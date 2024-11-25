from ..extensions import db


class VideoPlayer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    autoPlay = db.Column(db.Boolean, nullable=False, default=False)
    showIcon = db.Column(db.Boolean, nullable=False, default=False)
