from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from app.utils.auth import login_required_admin

leaderboard_bp = Blueprint('leaderboard', __name__)

def calculate_total(team):
    team['total_score'] = team.get('leaderboard1_score', 0) + team.get('leaderboard2_score', 0) + team.get('leaderboard3_score', 0)
    return team

@leaderboard_bp.route('/')
def main_leaderboard():
    from app import mongo
    teams = list(mongo.db.teams.find())
    teams = [calculate_total(t) for t in teams]
    teams.sort(key=lambda x: x['total_score'], reverse=True)
    return render_template('leaderboard.html', teams=teams, title='Main Leaderboard', leaderboard_num=0)

@leaderboard_bp.route('/leaderboard/<int:num>')
def leaderboard(num):
    from app import mongo
    if num not in [1, 2, 3]:
        return redirect(url_for('leaderboard.main_leaderboard'))
    
    teams = list(mongo.db.teams.find())
    teams = [calculate_total(t) for t in teams]
    score_key = f'leaderboard{num}_score'
    teams.sort(key=lambda x: x.get(score_key, 0), reverse=True)
    return render_template('leaderboard.html', teams=teams, title=f'Leaderboard {num}', leaderboard_num=num)
