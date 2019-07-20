from django.views import generic

from .models import Category, Entry


class EntryMixin:
    date_field = 'pub_date'
    model = Entry


class CategoryMixin:
    model = Category


class EntryArchiveIndex(EntryMixin, generic.ArchiveIndexView):
    pass


class EntryArchiveYear(EntryMixin, generic.YearArchiveView):
    make_object_list = True


class EntryArchiveMonth(EntryMixin, generic.MonthArchiveView):
    pass


class EntryArchiveDay(EntryMixin, generic.DayArchiveView):
    pass


class EntryDetail(EntryMixin, generic.DateDetailView):
    def get_queryset(self):
        # Allow logged-in users to view draft entries.
        if self.request.user.is_authenticated:
            return Entry.objects.all()
        return Entry.live.all()


class CategoryList(CategoryMixin, generic.ListView):
    pass


class CategoryDetail(CategoryMixin, generic.DetailView):
    pass
