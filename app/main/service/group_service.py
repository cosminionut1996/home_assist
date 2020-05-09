
from app.main import db
from app.main.model.group import Group, GroupInvite
from http import HTTPStatus


def create_group(data, creator_id):
    # TODO: A user might want to create multiple groups and they should be stored differently
    group = get_a_group(creator_id=creator_id)
    if group:
        return dict(
            group={
                "creator_id": group.creator_id,
                "date_created": group.date_created,
                "name": group.name,
                "id": group.id
            }
        ), HTTPStatus.FOUND

    group = Group(
        creator_id=creator_id,
        name=data['name']
    )
    try:
        # insert the group
        db.session.add(group)
        db.session.commit()
        return dict(
            group={
                "creator_id": group.creator_id,
                "date_created": group.date_created,
                "name": group.name,
                "id": group.id
            }
        ), HTTPStatus.CREATED
    except Exception as e:
        return dict(
            error='Encountered an unexpected error'
        ), HTTPStatus.INTERNAL_SERVER_ERROR

def get_all_groups():
    return Group.query.all()

def get_a_group(group_id=None, creator_id=None):
    # TODO: A user might want to create multiple groups and they should be stored differently
    if group_id:
        return Group.query.filter_by(id=group_id).first()
    elif creator_id:
        return Group.query.filter_by(creator_id=creator_id).first()
    raise ValueError("Bad parameters chosen for group filter.")

def update_group(data, group_id=None, creator_id=None):
    group = get_a_group(group_id=group_id, creator_id=creator_id)
    if not group:
        return dict(
            error='Group not found'
        ), HTTPStatus.NOT_FOUND
    if group:
        for key, value in data.items():
            group.__setattr__(key, value)
    try:
        # update the group
        db.session.add(group)
        db.session.commit()
        return dict(
            group={
                "creator_id": group.creator_id,
                "date_created": group.date_created,
                "name": group.name,
                "id": group.id
            }
        ), HTTPStatus.OK
    except Exception as e:
        return dict(
            error='Encountered an unexpected error'
        ), HTTPStatus.INTERNAL_SERVER_ERROR

def delete_group(group_id, creator_id):
    deletions = Group.query.filter_by(
        id=group_id,
        creator_id=creator_id
    ).delete()
    if deletions:
        db.session.commit()
        return dict(), HTTPStatus.NO_CONTENT
    else:
        return dict(
            error='Group not found'
        ), HTTPStatus.NOT_FOUND

def create_group_invite(public_id_sender, public_id_invitee, group_id):
    group_invite = GroupInvite(
        public_id_sender=public_id_sender,
        public_id_invitee=public_id_invitee,
        group_id=group_id,
        token='hello'
    )
    try:
        db.session.add(group)
        db.session.commit()
        return dict(
            public_id_invitee=group_invite.public_id_invitee,
            public_id_sender=group_invite.public_id_sender,
        ), HTTPStatus.CREATED
    except Exception as e:
        return dict(
            error='Encountered an unexpected error'
        ), HTTPStatus.INTERNAL_SERVER_ERROR
