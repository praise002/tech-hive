from rest_framework.throttling import UserRateThrottle


class ArticleSummaryThrottle(UserRateThrottle):
    """
    Custom throttle for article summary endpoint
    Allows 10 requests per hour per authenticated user
    """

    scope = "article_summary"


class ArticleSummaryRegenerateThrottle(UserRateThrottle):
    """
    Custom throttle for force regeneration
    Allows 3 regenerations per hour per authenticated user
    """

    scope = "article_summary_regenerate"

    def allow_request(self, request, view):
        """
        Only apply this throttle if force_regenerate is True
        """
        force_regenerate = (
            request.query_params.get("force_regenerate", "false").lower() == "true"
        )

        if not force_regenerate:
            # Don't throttle if not forcing regeneration
            return True

        # Apply throttle if forcing regeneration
        return super().allow_request(request, view)
