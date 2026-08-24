from .models import User


def get_user_role(user):
    """
    Returns the role of the logged-in user.
    """
    if not user or not user.is_authenticated:
        return None

    return user.role


def is_admin(user):
    """
    Checks whether the user is an Admin.
    """
    return (
        user.is_authenticated
        and user.role == User.Role.ADMIN
    )


def is_investigator(user):
    """
    Checks whether the user is an Investigator.
    """
    return (
        user.is_authenticated
        and user.role == User.Role.INVESTIGATOR
    )


def is_forensic_expert(user):
    """
    Checks whether the user is a Forensic Expert.
    """
    return (
        user.is_authenticated
        and user.role == User.Role.FORENSIC_EXPERT
    )


def is_judge(user):
    """
    Checks whether the user is a Judge.
    """
    return (
        user.is_authenticated
        and user.role == User.Role.JUDGE
    )