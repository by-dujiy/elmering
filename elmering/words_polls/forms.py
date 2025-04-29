from django import forms
from words_polls.models import Foreign_Word, Translate_Word, Words_Collection


# class ForeignWordForm(forms.ModelForm):
#     class Meta:
#         model = Foreign_Word
#         fields = '__all__'

#     foreign_word = forms.CharField(max_length=120)
#     translations = ...


# class TranslateWordsForm(forms.ModelForm):
#     class Meta:
#         model = Translate_Word
#         fields = ['word']

#     translate_words = forms.CharField()


# # ForeignWordSet = forms.modelformset_factory(
# #                                             Foreign_Word,
# #                                             fields=['word'])


# ForeignWordSet = forms.inlineformset_factory(
#                                             Foreign_Word,
#                                             Translate_Word,
#                                             form=TranslateWordsForm,
#                                             extra=1,
#                                             can_delete=True)


# CollectionSet = forms.inlineformset_factory(
#                                             Words_Collection,
#                                             Foreign_Word,
#                                             form=ForeignWordForm,
#                                             extra=1,
#                                             can_delete=True)


# WordsPollSet = forms.inlineformset_factory(
#     Words_Collection,
#     Foreign_Word,
#     form=
# )

"""
Claude Sonnet
"""


class TranslateWordForm(forms.ModelForm):
    """Form for handling individual translation words"""
    class Meta:
        model = Translate_Word
        fields = ['word']
        widgets = {
            'word': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-light',
                'placeholder': 'Translation'
            })
        }


class ForeignWordForm(forms.ModelForm):
    """Form for handling foreign words with nested translations"""
    class Meta:
        model = Foreign_Word
        fields = ['word', 'words_collection']
        widgets = {
            'word': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-light',
                'placeholder': 'Foreign word'
            }),
            'words_collection': forms.Select(attrs={
                'class': 'form-control bg-dark text-light'
            })
        }

    # This will handle multiple translations as a string input
    translations_text = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-dark text-light',
            'placeholder': 'Translations (comma separated)'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If we're editing an existing instance, populate the translations field
        if self.instance.pk:
            translations = self.instance.translate_word_set.all()
            self.initial['translations_text'] = ', '.join([t.word for t in translations])

    def save(self, commit=True):
        instance = super().save(commit=commit)

        if commit and self.cleaned_data.get('translations_text'):
            # First, delete existing translations to replace them
            instance.translate_word_set.all().delete()

            # Create new translation objects
            translations = [t.strip() for t in self.cleaned_data['translations_text'].split(',') if t.strip()]
            for translation in translations:
                Translate_Word.objects.create(
                    word=translation,
                    foreign_word=instance
                )

        return instance


# Create formset for handling multiple foreign words within a collection
ForeignWordFormSet = forms.inlineformset_factory(
                                                    Words_Collection,
                                                    Foreign_Word,
                                                    form=ForeignWordForm,
                                                    extra=1,
                                                    can_delete=True)

# Create formset for handling multiple translations for a single foreign word
TranslateWordFormSet = forms.inlineformset_factory(
                                                    Foreign_Word,
                                                    Translate_Word,
                                                    form=TranslateWordForm,
                                                    extra=1,
                                                    can_delete=True)
