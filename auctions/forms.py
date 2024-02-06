from django import forms

class NewListing(forms.Form):
    title = forms.CharField(
        label="",
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'Title', 'class': 'form-control form-group col-12'})
    )
    description = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={'placeholder': 'Description', 'class': 'form-control form-group col-12'})
    )
    starting_bid = forms.DecimalField(
        label="",
        max_digits=6,
        decimal_places=2,
        min_value=0.01,
        max_value=9999.99,
        widget=forms.NumberInput(attrs={'placeholder': 'Starting bid', 'class': 'form-control form-group col-12'})
    )
    image_url = forms.URLField(
        label="",
        widget=forms.URLInput(attrs={'placeholder': 'Image URL', 'class': 'form-control form-group col-12'})
    )
    category = forms.CharField(
        label="",
        max_length=128,
        widget=forms.TextInput(attrs={'placeholder': 'Category', 'class': 'form-control form-group col-6'})
    )

class AddBid(forms.Form):
    new_bid = forms.DecimalField(label="", max_digits=6, decimal_places=2, min_value=0.01, max_value=9999.99, widget=forms.NumberInput(attrs={'placeholder': 'Your bid'}))


class AddComment(forms.Form):
    comment = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={'placeholder': 'Write comment', 'class': 'form-control form-group'})
    )
