def has_premium_access(user):
    """
    Check if user has active premium access.
    """
    if not user or not user.is_authenticated:
        return False

    try:
        return user.subscription.is_active
    except Exception:
        # No subscription = BASIC user
        return False


def get_user_plan_name(user):
    """Get display name of user's current plan"""
    if has_premium_access(user):
        return user.subscription.plan.name

    return "Basic"


def get_user_features(user):
    """Get feature dictionary for user"""
    BASIC_FEATURES = {
        "priority_support": False,
        "analytics_dashboard": False,
        "ad_free": False,
        "early_access": False,
    }

    if has_premium_access(user):
        return user.subscription.plan.features

    return BASIC_FEATURES
