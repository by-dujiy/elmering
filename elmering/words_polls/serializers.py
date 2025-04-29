from words_polls.models import Foreign_Word, Words_Collection, Translate_Word
from rest_framework import serializers


class TranslateWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translate_Word
        fields = ['word']


class ForeignWordSerializer(serializers.ModelSerializer):
    translations = TranslateWordSerializer(
        many=True,
        source='translate_words',
        required=False
    )

    class Meta:
        model = Foreign_Word
        fields = ['id', 'word', 'translations']


class WordsCollectionSerializer(serializers.ModelSerializer):
    words = ForeignWordSerializer(
        many=True,
        source='foreign_words',
        required=False
    )

    class Meta:
        model = Words_Collection
        fields = ['collection_name', 'words']


{'csrfmiddlewaretoken': 'A6oGBNEghxzjfMdUr1MxXfVnKyXMaPGGpNhmRDiPyEC6RHz33k7weTagygocZhQY', 'collection_name': 'basic set 2', 'word_3': 'fair', 'translation_3': 'справедливый, ярмарка', 'word_5': 'conform', 'translation_5': 'соответствовать', 'word_16': 'new', 'translation_16': 'novv', 'word_17': 'zippo', 'translation_17': 'молния, змейка на брюках', 'word_18': 'deep', 'translation_18': 'глубина, уровень', 'word_new[]': 'throat', 'translation_new[]': '2222'}