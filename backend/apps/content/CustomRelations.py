from rest_framework.relations import HyperlinkedRelatedField
# NOTE: RE-LEARN FROM KWARGS AS IT IS STILL CONFUSING

class CustomHyperlinkedRelatedField(HyperlinkedRelatedField):

    def __init__(self, *args, **kwargs):
        self.lookup_fields = kwargs.pop("lookup_fields", [])
        super().__init__(*args, **kwargs)

    def get_url(self, obj, view_name, request, format):
        """
        Given an object, return the URL that hyperlinks to the object.

        May raise a `NoReverseMatch` if the `view_name` and `lookup_field`
        attributes are not configured to correctly match the URL conf.
        """

        # Unsaved objects will not yet have a valid URL.
        if hasattr(obj, "pk") and obj.pk in (None, ""):
            return None

        # Build kwargs from lookup_fields
        kwargs = {}
        for model_field, url_param in self.lookup_fields:
            attr = obj
            for field in model_field.split("."):
                attr = getattr(attr, field)
                if attr is None:
                    return None  # Can't build URL if any part is None
            kwargs[url_param] = attr

        return self.reverse(view_name, kwargs=kwargs, request=request, format=format)


class CustomHyperlinkedIdentityField(CustomHyperlinkedRelatedField):
    """
    A read-only field that represents the identity URL for an object, itself.

    This is in contrast to `HyperlinkedRelatedField` which represents the
    URL of relationships to other objects.
    """

    def __init__(self, view_name=None, **kwargs):
        assert view_name is not None, 'The `view_name` argument is required.'
        kwargs['read_only'] = True
        kwargs['source'] = '*'
        super().__init__(view_name, **kwargs)

    def use_pk_only_optimization(self):
        # We have the complete object instance already. We don't need
        # to run the 'only get the pk for this relationship' code.
        return False
