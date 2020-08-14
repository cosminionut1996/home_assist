
from app.main import db
from app.main.model.group import Group
from app.main.model.membership import Membership
from http import HTTPStatus


def create_group(data, uuid_creator):
    # TODO: A user might want to create multiple groups and they should be stored differently
    group = get_a_group(uuid_creator=uuid_creator)
    if group:
        return dict(
            group={
                "uuid_creator": group.uuid_creator,
                "date_created": group.date_created,
                "name": group.name,
                "_uuid": group._uuid
            }
        ), HTTPStatus.FOUND

    group = Group(
        uuid_creator=uuid_creator,
        name=data['name']
    )
    try:
        # insert the group
        db.session.add(group)
        db.session.commit()
        return dict(
            group={
                "uuid_creator": group.uuid_creator,
                "date_created": group.date_created,
                "name": group.name,
                "_uuid": group._uuid
            }
        ), HTTPStatus.CREATED
    except Exception as e:
        return dict(
            error='Encountered an unexpected error'
        ), HTTPStatus.INTERNAL_SERVER_ERROR

def get_groups(
    uuid_user,
    owned=None,
    member=None,
    name=None
):
    qr = Group.query

    if owned and member:
        qr = qr.join(Membership, Membership.uuid_Resource==Group._uuid)
        qr = qr.filter(
            (Group.uuid_creator==uuid_user)
            | (Membership.uuid_member==uuid_user)
        )
    elif owned:
        qr = qr.filter(Group.uuid_creator==uuid_user)
    elif member:
        qr = qr.join(
            Membership,
            (Membership.uuid_resource == Group._uuid)
            & (Membership.uuid_member == uuid_user)
        )
    else:
        return list(), HTTPStatus.BAD_REQUEST

    if name:
        qr = qr.filter_by(name=name)

    qr = qr.all()

    return qr, HTTPStatus.OK if qr else HTTPStatus.NOT_FOUND

def get_a_group(uuid_group=None, uuid_creator=None):
    # TODO: A user might want to create multiple groups and they should be stored differently
    if uuid_group:
        return Group.query.filter_by(_uuid=uuid_group).first()
    elif uuid_creator:
        return Group.query.filter_by(uuid_creator=uuid_creator).first()
    raise ValueError("Bad parameters chosen for group filter.")

def update_group(data, uuid_group=None, uuid_creator=None):
    group = get_a_group(uuid_group=uuid_group, uuid_creator=uuid_creator)
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
                "uuid_creator": group.uuid_creator,
                "date_created": group.date_created,
                "name": group.name,
                "_uuid": group._uuid
            }
        ), HTTPStatus.OK
    except Exception as e:
        return dict(
            error='Encountered an unexpected error'
        ), HTTPStatus.INTERNAL_SERVER_ERROR

def delete_group(uuid_group, uuid_creator):
    deletions = Group.query.filter_by(
        _uuid=uuid_group,
        uuid_creator=uuid_creator
    ).delete()
    if deletions:
        db.session.commit()
        return dict(), HTTPStatus.NO_CONTENT
    else:
        return dict(
            error='Group not found'
        ), HTTPStatus.NOT_FOUND
