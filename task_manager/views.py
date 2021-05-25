from django_filters.views import FilterView
from tasks.models import Task
from task_manager.filters import MyTasksFilter


class MyTasksListView(FilterView):
    model = Task
    template_name = 'index.html'
    filterset_class = MyTasksFilter

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Task.objects.filter(executor=self.request.user)
