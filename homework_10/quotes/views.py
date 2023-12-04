from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.
from .forms import AuthorForm, TagForm, QuoteForm
from .models import Tag, Author, Quote


def top_tags():
    quotes = Quote.objects.all()
    tag_list = {}
    for quote in quotes:
        for tag in quote.tags.all():
            if tag.name not in tag_list:
                tag_list[tag.name] = 1
            else:
                tag_list[tag.name] += 1
    sorted_tag_list = dict(sorted(tag_list.items(), key=lambda x: x[1], reverse=True))
    result = list(sorted_tag_list)[0:10]
    return result


def main(request, page=1):
    quotes = Quote.objects.all()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(
        request,
        "quotes/index.html",
        context={"quotes": quotes_on_page, "tags": top_tags()},
    )


def author(request, author_fn):
    author = Author.objects.get(fullname=author_fn)
    return render(request, "quotes/author.html", {"author": author})


def tag(request, tag_name):
    tag = Tag.objects.get(name=tag_name)
    all_quotes = Quote.objects.all()
    quotes = [q for q in all_quotes if tag in q.tags.all()]
    return render(request, "quotes/tag.html", {"quotes": quotes, "tag": tag})


@login_required
def new_author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="quotes:root")
        else:
            return render(request, "quotes/new_author.html", {"form": form})
    return render(request, "quotes/new_author.html", {"form": AuthorForm()})


@login_required
def new_tag(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="quotes:root")
        else:
            return render(request, "quotes/new_tag.html", {"form": form})
    return render(request, "quotes/new_tag.html", {"form": TagForm()})


@login_required
def new_quote(request):
    all_tags = Tag.objects.all()
    authors = Author.objects.all()

    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_note = form.save()
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist("tags"))
            for tag in choice_tags.iterator():
                new_note.tags.add(tag)
            choice_author = Author.objects.filter(
                name__in=request.POST.getlist("authors")
            )
            for author in choice_author.iterator():
                new_note.authors.add(author)
            return redirect(to="quotes:root")
        else:
            return render(
                request,
                "quotes/new_quote.html",
                {"all_tags": all_tags, "authors": authors, "form": form},
            )
    return render(
        request,
        "quotes/new_quote.html",
        {"all_tags": all_tags, "authors": authors, "form": QuoteForm()},
    )
