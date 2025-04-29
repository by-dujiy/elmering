from django.db import transaction
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from words_polls.models import Words_Collection, Foreign_Word, Translate_Word


class CollectionListView(ListView):
    model = Words_Collection


class CollectionDetailView(DetailView):
    model = Words_Collection
    template_name = 'words_polls/collection_detail.html'
    context_object_name = 'collection'
    pk_url_kwarg = 'id'


class CollectionEditView(TemplateView):
    template_name = 'words_polls/collection_edit.html'

    def get(self, request, pk):
        collection = get_object_or_404(
            Words_Collection.objects.prefetch_related(
                'foreign_words__translate_words'),
            pk=pk)
        return render(request, self.template_name, {'collection': collection})

    def post(self, request, pk):
        collection = get_object_or_404(
            Words_Collection.objects.prefetch_related(
                'foreign_words__translate_words'),
            pk=pk)
        request_dict = request.POST.dict()
        with transaction.atomic():
            # find and delete from db deleted from post-request foreign words
            db_set = set(collection.foreign_words.all().values_list("word", flat=True))
            post_word_set = set([value for key, value in request_dict.items() if key.startswith('word_')])
            to_delete = db_set - post_word_set
            if to_delete:
                collection.foreign_words.filter(word__in=to_delete).delete()
            # find and make changes
            for key, value in request_dict.items():
                if 'word_' in key:
                    fw = collection.foreign_words.get(id=key[5:])
                    transl_set = set(fw.translate_words.all().values_list(
                        "word",
                        flat=True)
                        )
                    post_transl = set([x.strip() for x in request_dict.get(
                        f"translation_{key[5:]}").split(',')]
                        )
                    if value != fw.word:
                        fw.word = value
                        fw.save()
                    new_transl: set = post_transl - transl_set
                    if new_transl:
                        Translate_Word.objects.bulk_create(
                            [Translate_Word(word=word, foreign_word=fw)
                             for word in new_transl]
                        )
                    del_transl = transl_set - post_transl
                    if del_transl:
                        fw.translate_words.filter(word__in=del_transl).delete()
                if key == 'collection_name':
                    if collection.collection_name != value:
                        collection.collection_name = value
                        collection.save()
                # create new foreign and translation
                if 'nw_' in key:
                    new_fw = request_dict.get(f"nw_{key[3:]}")
                    foreign_word = Foreign_Word.objects.create(
                        word=new_fw,
                        words_collection=collection
                    )
                    new_transl = [
                        Translate_Word(word=x.strip(),
                                       foreign_word=foreign_word)
                        for x in request_dict.get(f"nt_{key[3:]}").split(',')]
                    if new_transl:
                        Translate_Word.objects.bulk_create(new_transl)
        return redirect("words_polls:detail", id=pk)


class CollectionCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'words_polls/collection_create.html'

    def post(self, request):
        collection_name = request.POST.get('collection_name')
        collection = Words_Collection.objects.create(
            collection_name=collection_name,
            user=request.user
            )
        for key, value in request.POST.items():
            if 'nw_' in key:
                new_fw = request.POST.get(f"nw_{key[3:]}")
                foreign_word = Foreign_Word.objects.create(
                    word=new_fw,
                    words_collection=collection
                )
                new_transl = [
                    Translate_Word(word=x.strip(),
                                   foreign_word=foreign_word)
                    for x in request.POST.get(f"nt_{key[3:]}").split(',')]
                if new_transl:
                    Translate_Word.objects.bulk_create(new_transl)
        return redirect("words_polls:index")


class CollectionDeleteView(LoginRequiredMixin, DeleteView):
    model = Words_Collection
    success_url = '/'
