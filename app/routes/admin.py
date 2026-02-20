from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from bson.objectid import ObjectId
from datetime import datetime
from app import mongo
from app.utils.auth import check_password, hash_password, login_required_admin

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def calculate_total(team):
    team['total_score'] = team.get('leaderboard1_score', 0) + team.get('leaderboard2_score', 0) + team.get('leaderboard3_score', 0)
    return team

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin = mongo.db.admins.find_one({'username': username})
        
        if admin and check_password(password, admin['password']):
            session['admin_id'] = str(admin['_id'])
            session['admin_username'] = admin['username']
            flash('Logged in successfully!', 'success')
            return redirect(url_for('admin.teams'))
        else:
            flash('Invalid credentials', 'error')
    
    return render_template('login.html')

@admin_bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('leaderboard.main_leaderboard'))

@admin_bp.route('/')
@login_required_admin
def index():
    return redirect(url_for('admin.teams'))

@admin_bp.route('/teams', methods=['GET', 'POST'])
@login_required_admin
def teams():
    if request.method == 'POST':
        team_name = request.form.get('team_name').strip()
        if team_name:
            existing = mongo.db.teams.find_one({'name': team_name})
            if existing:
                flash('Team already exists!', 'error')
            else:
                mongo.db.teams.insert_one({
                    'name': team_name,
                    'leaderboard1_score': 0,
                    'leaderboard2_score': 0,
                    'leaderboard3_score': 0,
                    'created_at': datetime.utcnow()
                })
                flash(f'Team "{team_name}" created!', 'success')
    
    teams = list(mongo.db.teams.find())
    teams = [{**t, '_id': str(t['_id'])} for t in teams]
    teams = [calculate_total(t) for t in teams]
    teams.sort(key=lambda x: x['name'])
    return render_template('admin_teams.html', teams=teams)

@admin_bp.route('/points', methods=['GET', 'POST'])
@login_required_admin
def points():
    if request.method == 'POST':
        team_id = request.form.get('team_id')
        leaderboard_num = int(request.form.get('leaderboard_num'))
        points = int(request.form.get('points'))
        
        if team_id and points > 0:
            score_key = f'leaderboard{leaderboard_num}_score'
            mongo.db.teams.update_one(
                {'_id': ObjectId(team_id)},
                {'$inc': {score_key: points}}
            )
            flash(f'Added {points} points to leaderboard {leaderboard_num}!', 'success')
    
    teams = list(mongo.db.teams.find())
    teams = [{**t, '_id': str(t['_id'])} for t in teams]
    teams = [calculate_total(t) for t in teams]
    teams.sort(key=lambda x: x['name'])
    return render_template('admin_points.html', teams=teams)

@admin_bp.route('/management', methods=['GET', 'POST'])
@login_required_admin
def management():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add_user':
            username = request.form.get('username').strip()
            password = request.form.get('password')
            
            if username and password:
                existing = mongo.db.admins.find_one({'username': username})
                if existing:
                    flash('Username already exists!', 'error')
                else:
                    mongo.db.admins.insert_one({
                        'username': username,
                        'password': hash_password(password)
                    })
                    flash(f'User "{username}" created!', 'success')
        
        elif action == 'change_password':
            admin_id = request.form.get('admin_id')
            new_password = request.form.get('new_password')
            
            if admin_id and new_password:
                if session.get('admin_id') != admin_id:
                    flash('You can only change your own password!', 'error')
                else:
                    mongo.db.admins.update_one(
                        {'_id': ObjectId(admin_id)},
                        {'$set': {'password': hash_password(new_password)}}
                    )
                    flash('Password changed successfully!', 'success')
        
        elif action == 'delete_user':
            admin_id = request.form.get('admin_id')
            
            if admin_id:
                if session.get('admin_id') == admin_id:
                    flash('You cannot delete yourself!', 'error')
                else:
                    mongo.db.admins.delete_one({'_id': ObjectId(admin_id)})
                    flash('User deleted!', 'success')
    
    admins = list(mongo.db.admins.find())
    admins = [{**a, '_id': str(a['_id'])} for a in admins]
    return render_template('admin_management.html', admins=admins, current_admin_id=session.get('admin_id'))

@admin_bp.route('/delete_team/<team_id>')
@login_required_admin
def delete_team(team_id):
    mongo.db.teams.delete_one({'_id': ObjectId(team_id)})
    flash('Team deleted!', 'success')
    return redirect(url_for('admin.teams'))
