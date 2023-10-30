from flask import redirect, flash, request, url_for
from . import db
from .actions import serialize_user_information
from .dbmodels import  User, UserGroup, Group, Competition, CompetitionGroup
from flask_login import current_user
from .actions import upload_image
from collections import defaultdict

# Not displayed in Groups
def get_user_groups():
    groups = []
    check_managed = UserGroup.query.filter_by(user_id=current_user.id, is_manager=False).first() is not None
    
    if check_managed:

        group_get = UserGroup.query.filter_by(user_id=current_user.id, is_manager=False).all()
      
        for x in group_get:
            groups.append(Group.query.filter_by(id = x.group_id).first())

    return groups
# displayed in groups
def get_managed_groups():
    groups = []
    check_managed = UserGroup.query.filter_by(user_id=current_user.id, is_manager = True).first() is not None
    if check_managed:

        group_get = UserGroup.query.filter_by(user_id=current_user.id, is_manager = True).all()
        for x in group_get:
            groups.append(Group.query.filter_by(id = x.group_id).first())
    return groups

#used on post request for create group page    
def create_group(group_name, owner_email):

    check_group_name = Group.query.filter_by(name = group_name).first() is None
    check_owner = User.query.filter_by(email = owner_email).first() != None

    if check_group_name and check_owner:

        group = Group(name = group_name)
        db.session.add(group)
        db.session.commit()

        get_group  = Group.query.filter_by(name = group_name).first()
        owner_attachment = UserGroup(group_id = get_group.id, user_id = current_user.id, is_manager = True)
        db.session.add(owner_attachment)
        db.session.commit()

    else:
        if check_group_name is False:
            flash(category="error", message="Group already exists")
            return redirect(request.url)
        if check_owner is False:
            flash(category="error", message="Owner does not exist")
            return redirect(request.url)


# Not in use yet
def create_competition(comp_name, iconFile, *args):
    groups = []
    failed_groups = []
    competition_check = Competition.query.filter_by(name=comp_name).first() is None
    create_image = (upload_image(iconFile))
    check_image = (create_image["upload"] == "Pass")
    for x in args:
            group = Group.query.filter_by(name=x).first() 
            if group is not None:
                groups.append(group)
            else:
                failed_groups.append(x)
    group_check = (len(groups) != 0)
    if competition_check and check_image and group_check:
        
        competition = Competition(name = comp_name, iconFile = create_image["newPath"], created_by = current_user.id)
        db.session.add(competition)
        db.session.commit()
        added_competition = Competition.query.filter_by(name=comp_name).first()
        
        for x in groups:
            comp_attach = CompetitionGroup(group_id = x.id, competition_id = added_competition.id)
            db.session.add(comp_attach)
            db.session.commit()

# use in the groups add group member page
def add_group_member(groupname, email):
    user = User.query.filter_by(email = email).first()
    if user is None:
        flash(category="error", message =f"{email} does not exist")
    group = Group.query.filter_by(name = groupname).first()
    if (user is not None) and (group is not None):
        check_user = UserGroup.query.filter_by(group_id = group.id, user_id = user.id).first() is None
        check_managed = UserGroup.query.filter_by(group_id = group.id, user_id=current_user.id, is_manager = True).first() is not None
        if check_managed and check_user:
        
            add_user = UserGroup(group_id = group.id, user_id = user.id, is_manager = False)
            db.session.add(add_user)
            db.session.commit()
            flash(category="success", message=f"{user.email} has been added to {group.name}")
            return redirect(url_for('location.groups'))
        elif not check_user: 
            flash(category="error", message=f"{email} is already part of this group")
            
        elif not check_managed:
            flash(category="error", message="You do not have the right to perform this action")
            return redirect(request.url)

# Use for displaying all group members that the user is a part of
def display_group_members():
    serialized_grouped = []
    grouped_users = defaultdict(list)
    check_membership = UserGroup.query.filter_by(user_id = current_user.id).first() is not None
    if check_membership:
        
        member_groups = UserGroup.query.filter_by(user_id = current_user.id).all()
        for member_group in member_groups:
            temp_users = UserGroup.query.filter_by(group_id = member_group.group_id).all()
            group = Group.query.filter_by(id = member_group.group_id).first()
            for temp_user in temp_users:
                check_user = (User.query.filter_by(id = temp_user.user_id).first())
                if check_user.id != current_user.id:
                    grouped_users[group.name].append(User.query.filter_by(id = temp_user.user_id).first())
        for group, users in grouped_users.items():
            group_info = {
                'group_name': group,
                'users': [serialize_user_information(user) for user in users]
            }
            serialized_grouped.append(group_info)
    
        
    return serialized_grouped
     
