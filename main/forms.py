"""
This module defines the forms for the Django application.

Currently, it includes the `ReviewForm` which is a `ModelForm` for the `Review` model.
"""

from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    """
    A form for creating and updating `Review` instances.

    The form includes all fields from the `Review` model.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the form.

        The user argument is popped from kwargs and stored as an instance variable.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments. Should include 'user'.
        """
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Review
        fields = ['review_text', 'grade']
