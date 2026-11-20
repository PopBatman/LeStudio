OPERATOR_GROUP = "Opérateurs Studio"


def is_operator(user):
    return user.is_active and user.groups.filter(name=OPERATOR_GROUP).exists()
