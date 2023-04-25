"""This module contains routes for the app."""
from flask import (Blueprint, jsonify, 
                   render_template, session, request)
from flask_login import login_required
from ..extensions.extensions import youtube

from ..utils.http_status_codes import HTTP_200_OK

home = Blueprint("home", __name__)
query = 'Python programming'
search_client = youtube.get_search_client(query)
similar_search_client = youtube.get_related_video_search_client()

@home.route("/")
@home.route("/home")
@home.route("/index")
@home.route("/videos")
# @login_required
def home_page():
    """Render the home page."""
    videos = []
    return render_template('home/home.html', title='Home', videos=videos)

@home.route('/load_videos')
def load_videos():
    next_page = request.args.get('next_token')
    prev_token, next_token, videos = search_client.search_videos(next_page_token=next_page)
    videos = [video.to_dict() for video in videos] 
    
    return jsonify({
        'videos': videos,
        'next_token': next_token
    })

@home.route("/play_video")
# @login_required
def play_video():
    video_id = request.args.get("video_id")
    video = youtube.find_video_by_id(video_id) 
    
    comments = [
        comment.get_comment() for comment in video.get_video_comments()
    ]
    
    video = video.to_dict()
    similar_videos = []
    return render_template('home/play_video.html', 
            video=video, similar_videos=similar_videos,
            comments=comments)
    
    
@home.route('/similar_videos')
def get_similar_videos():
    video_id = request.args.get("video_id")
    next_page = request.args.get('next_token')
    prev, next_token, similar_videos = similar_search_client.search_related_videos(video_id, next_page_token=next_page)
    similar_videos = [video.to_dict() for video in similar_videos]
    return jsonify({
        'videos': similar_videos,
        'next_token': next_token
    })

@home.route("/search", methods=["POST"])
def search_videos():
    return 'Search video'


@home.route("/suggestions", methods=["POST"])
def get_suggestions():
    """Get suggestions when seraching."""
    return 'Suggestions'
