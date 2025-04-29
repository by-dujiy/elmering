import re
from django.conf import settings
from django.db import models


class Words_Collection(models.Model):
    VISIBILITY_CHOICES = (
        ('public', 'Public'),
        ('shared', 'Shared'),
        ('private', 'Private'),
    )

    collection_name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=180, unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    create_date = models.DateField(auto_now_add=True)
    visibility = models.CharField(max_length=10,
                                  choices=VISIBILITY_CHOICES,
                                  default='private'
                                  )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='words_collections'
                             )
    shared_with = models.ManyToManyField(
            settings.AUTH_USER_MODEL,
            related_name='shared_collections',
            blank=True,
            )

    class Meta:
        db_table = "words_collection"
        ordering = ["-create_date"]

    def __repr__(self) -> str:
        return (f"(Collection_id: {self.id} '{self.collection_name}' "
                f"|{self.create_date})")

    def __str__(self) -> str:
        return self.collection_namef


class Foreign_Word(models.Model):
    word = models.CharField(verbose_name="foreign word", max_length=48)
    create_date = models.DateField(auto_now_add=True)
    appearance_count = models.IntegerField(default=0)
    right_answer = models.IntegerField(default=0)
    last_appearance = models.DateTimeField(null=True)
    words_collection = models.ForeignKey(Words_Collection,
                                         related_name='foreign_words',
                                         on_delete=models.CASCADE)

    class Meta:
        db_table = "foreign_words"
        ordering = ["create_date"]

    def __repr__(self) -> str:
        return (f"(Foreign_Word_id: {self.id} - '{self.word}' "
                f"|{self.create_date})")

    def __str__(self) -> str:
        return self.word


class Translate_Word(models.Model):
    word = models.CharField(max_length=48)
    foreign_word = models.ForeignKey(Foreign_Word,
                                     related_name='translate_words',
                                     on_delete=models.CASCADE)

    class Meta:
        db_table = "translate_words"

    def __repr__(self) -> str:
        return (f"(Translate_Word_id: {self.id} '{self.word}', "
                f"{self.foreign_word})")

    def __str__(self) -> str:
        return self.word
