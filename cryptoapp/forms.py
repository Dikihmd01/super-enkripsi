from django import forms

class CryptoForm(forms.Form):
    message = forms.CharField(label="Pesan",
                                error_messages= {
                                    'required': 'Pesan harus diisi'
                                },
                                widget=forms.Textarea(
                                    attrs={
                                        'class': 'form-control',
                                        'rows': 2,
                                        'cols': 3,
                                        'placeholder': 'Masukkan pesan'
                                    }
                                ))

    key = forms.CharField(label="Kunci Vigenere Cipher",
                            max_length=250, widget=forms.TextInput(
                                attrs={
                                    'class': 'form-control',
                                    'placeholder': 'Masukkan kunci berupa kata',
                                    'required': 'Kunci vigenere harus diisi'
                                }
                            ))

    key_rf = forms.IntegerField(label="Kunci Rail Fence",
                            error_messages= {
                                'invalid': 'Kunci harus diisi dengan angka dari 0-9!',
                                'required': 'Kunci Rail Fence harus diisi'
                            },
                            widget=forms.TextInput(
                                attrs={
                                    'class': 'form-control',
                                    'placeholder': 'Hanya berupa angka dari 2-9'
                                }
                            ))