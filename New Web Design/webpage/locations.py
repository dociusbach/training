from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .actions import upload_image
from . import db

from .dbfunctions import *
from .checks import *


location = Blueprint('location', __name__)



@location.route('/About', methods=['GET', 'POST'])
def about():
    return render_template("about.html", user=current_user, profile_picture=check_image(current_user.iconFile))

@location.route('/Training', methods=['GET', 'POST'])
def training():
    return render_template("training.html", user=current_user, profile_picture=check_image(current_user.iconFile))

@location.route('/auth_home', methods=['GET', 'POST'])
@login_required
def auth_home():
    return render_template("auth_home.html", user=current_user, profile_picture=check_image(current_user.iconFile))

@location.route('/People', methods=['GET', 'POST'])
@login_required
def people():

    return render_template("people.html", user=current_user, profile_picture=check_image(current_user.iconFile), groups = display_group_members())
@location.route('/Groups', methods=['GET', 'POST'])
@login_required
def groups():

    return render_template("groups.html", user=current_user, profile_picture=check_image(current_user.iconFile), mygroups=get_user_groups(), mggroups=get_managed_groups())

@location.route('/Groups/new', methods=['GET', 'POST'])
@login_required
def new_group():
    if request.method == 'POST':
        group_name =request.form.get('groupname')
        create_group(group_name, current_user.email)

    return render_template("new_group.html", user=current_user, profile_picture=check_image(current_user.iconFile))

@location.route('/Groups/addMember', methods=['GET', 'POST'])
@login_required
def add_member_group():
    if request.method == 'POST':
        group_name = request.form.get('groupname')
        members = request.form.get('email').split(', ')
       
        for member in members:
             print (member)
             add_group_member(group_name, member)
        

    return render_template("add_group_member.html", user=current_user, profile_picture=check_image(current_user.iconFile), groups=get_managed_groups())

@location.route('/Projects/new', methods=['GET', 'POST'])
@login_required
def new_project():
    
    # if request.method == 'POST':
    #     proj_name = request.form.get('projectname')
    #     proj_desc = request.form.get('projectdesc')
    #     boxes = request.form.getlist('checkbox')

    #     new_path = upload_image()

    #     file_check = new_path['upload'] == "Failed"
    #     proj_name_check =  Project.query.filter_by(name = proj_name).first() is not None
        
    #     send_data = not (file_check or proj_name_check)
    #     if send_data is False:
    #         if proj_name_check is True:
    #              flash(category='error', message=f'Project Name {proj_name} is already in use')
    #         return redirect(request.url)
    #     else:
            
    #         new_project = Project(name = proj_name, iconFile = new_path['newPath'], description=proj_desc, created_by=current_user.id)
    #         db.session.add(new_project)   
    #         for x in range((len(boxes)-1)):
    #             x+=1
    #             Project.query.filter_by(name = proj_name).update({f"link{x}":f"boxes{x-1}"}, synchronize_session=False) 
            
    #         db.session.commit()
    #         flash(category='success', message="Project Created")
    #         return redirect(url_for('location.projects'))

    return render_template("new_project.html", user=current_user, profile_picture=check_image(current_user.iconFile))

@location.route('/Projects/join', methods=['GET', 'POST'])
@login_required
def join_project():

    # if request.method == 'POST':
    #     proj_name = request.form.get('projectname')
    #     project_check = Project.query.filter_by(name = proj_name).first() is None
        
    #     if project_check:
    #         flash(category='error', message=f'Project Name {proj_name} does not exist')
    #     else:
    #         project = Project.query.filter_by(name = proj_name).first()
    #         join_group = Project_Join(project = project.id, user = current_user.id)
    #         db.session.add(join_group)
    #         db.session.commit()
    #         flash(category='success', message=f"You have been added to {proj_name}")
    #         return redirect(url_for('location.projects'))
    return render_template("join_project.html", user=current_user, profile_picture=check_image(current_user.iconFile))

@location.route('/Competitions', methods=['GET', 'POST'])
@login_required
def competitions():
    
    
       
       

    return render_template("competitions.html", user=current_user, profile_picture=check_image(current_user.iconFile) )