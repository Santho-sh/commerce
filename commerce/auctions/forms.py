from django import forms


class CreateForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    description = forms.CharField(widget=forms.Textarea(attrs={"rows":4}))
    starting_bid = forms.IntegerField()
    image = forms.ImageField()
    category = forms.CharField(label='Category', max_length=100, required=False)