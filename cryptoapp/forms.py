from django import forms

class CryptoForm(forms.Form):
    message = forms.CharField(label="Masukkan pesan",
                                widget=forms.Textarea(
                                    attrs={
                                        'class': 'form-control',
                                        'rows': 2,
                                        'cols': 3
                                    }
                                ))
    key = forms.CharField(label="Masukan kunci",
                            max_length=250, widget=forms.TextInput(
                                attrs={'class': 'form-control'}
                            ))