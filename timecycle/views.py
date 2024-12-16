from django.views.generic import CreateView, FormView, TemplateView, UpdateView, ListView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import MetaCycle, Activity
from .forms import MetaCycleForm, ActivityForm 
from .utils import get_today_tasks_dataframe 


# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        script, div = get_today_tasks_dataframe(self.request.user)
        context['meta_cycles'] = MetaCycle.objects.all()  # Get all MetaCycles for the dropdown
        context['activities'] = Activity.objects.all()          
        context['bokeh_script'] = script
        context['bokeh_div'] = div

        #print (script, div)
        return context
    
        

class SuccessView(TemplateView):
    template_name = 'success.html' 


class NewTimeCycleView(CreateView):
    model = MetaCycle
    template_name = 'new-cycle.html'
    form_class = MetaCycleForm

    def form_valid(self, form):
        # Associate the meta cycle with the logged-in user
        form.instance.user = self.request.user  
        # Save the instance first
        meta_cycle = form.save()  
        # Redirect to new activity view with the pk of the created meta cycle
        return redirect('new-activity', pk=meta_cycle.pk)  # Redirect 
    

class ViewCyclesView(ListView):
    model = MetaCycle
    template_name = 'view-cycles.html'  # Create this template to display cycles
    context_object_name = 'meta_cycles'  # This will be available in the template as 'meta_cycles'

class EditCycleView(UpdateView):
    model = MetaCycle
    form_class = MetaCycleForm
    template_name = 'edit-cycle.html'
    success_url = reverse_lazy('index')  # Redirect to index or another page after successful update

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meta_cycle'] = self.object  # Pass the current meta cycle instance to the template
        return context

class NewActivityView(FormView):
    template_name = 'new-activity.html'
    form_class = ActivityForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meta_cycles'] = MetaCycle.objects.all()  # Pass all MetaCycles for selection
        return context

    def form_valid(self, form):
        # Get selected MetaCycle from form data
        meta_cycle_id = self.request.POST.get('meta_cycle')
        meta_cycle = get_object_or_404(MetaCycle, pk=meta_cycle_id)  # Ensure it exists
        activity = form.save(commit=False)
        activity.meta_cycle = meta_cycle  # Associate with selected MetaCycle
        activity.save()
        return redirect('success')  # Redirect after saving
    
class ViewActivitiesView(ListView):
    model = Activity
    template_name = 'view-activities.html'  # Create this template to display cycles
    context_object_name = 'activities'  # This will be available in the template as 'meta_cycles'


class EditActivityView(UpdateView):
    model = Activity
    form_class = ActivityForm
    template_name = 'edit-activity.html'
    success_url = reverse_lazy('index')  # Redirect to index or another page after successful update

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meta_cycles'] = MetaCycle.objects.all()  # Pass all MetaCycles for selection
        context['activity'] = self.object  # Pass the current activity instance to the template
        return context
