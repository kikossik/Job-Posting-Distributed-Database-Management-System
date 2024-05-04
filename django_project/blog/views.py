from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Job
from urllib.parse import urlencode
from itertools import chain
from django.core.paginator import Paginator

DATABASE_MAPPING = {
    'first': {'NY', 'VT', 'CT', 'DE', 'FL', 'GA', 'ME', 'MD', 'MA', 'NH', 'NJ', 'NC', 'PA', 'RI', 'SC', 'VA', 'WV'},
    'second': {'CA', 'OR', 'WA', 'AK', 'HI'},
    'third': {'AL', 'AZ', 'AR', 'CO', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'MN', 'MS', 'MO', 'MT', 'MI', 'NE', 'NV', 'NM', 'ND', 'OH', 'OK', 'SD', 'TN', 'TX', 'UT', 'WI', 'WY'}
}
DATABASES = ['first', 'second', 'third']

def home(request):
    d_default_jobs = list(Job.objects.all().order_by('-date_posted'))
    # Fetch jobs from each specified database, and sort them by `date_posted`
    d_first_jobs = Job.objects.using('first').all().order_by('-date_posted')
    d_second_jobs = Job.objects.using('second').all().order_by('-date_posted')
    d_third_jobs = Job.objects.using('third').all().order_by('-date_posted')

    # Combine and sort jobs by `date_posted`
    combined_jobs = d_default_jobs + list(chain(d_first_jobs, d_second_jobs, d_third_jobs))

    # Use Paginator to paginate the combined list
    paginator = Paginator(combined_jobs, 20)  # 20 jobs per page
    page_number = request.GET.get('page', 1)  # Default to page 1 if `page` is not in the request
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/home.html', {'page_obj': page_obj})

def search_results(request):
    title = request.GET.get('title')
    location = request.GET.get('location')
    employment_type = request.GET.get('employment_type')
    industries = request.GET.get('industries')
    selected_states = request.GET.getlist('state_code')
    combined_query = []

    # Iterate over all databases
    for db in DATABASES:
        query = Job.objects.using(db).all()

        # Apply filters
        if title:
            query = query.filter(title__icontains=title)
        if selected_states:
            query = query.filter(state_code__in=selected_states)
        if location:
            query = query.filter(location__icontains=location)
        if employment_type:
            query = query.filter(employment_type__icontains=employment_type)
        if industries:
            query = query.filter(industries__icontains=industries)
        
        combined_query.extend(list(query))

    # Set up pagination
    paginator = Paginator(combined_query, 20)  # 20 jobs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Rebuild the query string without 'page' parameter for pagination links
    query_params = request.GET.copy()
    if 'page' in query_params:
        del query_params['page']
    query_string = urlencode(query_params, doseq=True)

    return render(request, 'blog/search_form.html', {
        'page_obj': page_obj,
        'states': sorted(list(chain(*DATABASE_MAPPING.values()))),  # Provide all available states for UI
        'selected_states': selected_states,
        'query_string': query_string
    })


class PostListView(ListView):
    model = Job
    template_name = 'blog/home.html'
    context_object_name = 'jobs'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Job
    template_name = 'blog/user_posts.html'
    context_object_name = 'jobs'
    # ordering = ['-date_posted']
    paginate_by = 5
    def get_queryset(self):
        agency_name = self.kwargs.get('username')

        # Query jobs from all databases
        default_jobs = Job.objects.filter(agency=agency_name).order_by('-date_posted')
        first_jobs = Job.objects.using('first').filter(agency=agency_name).order_by('-date_posted')
        second_jobs = Job.objects.using('second').filter(agency=agency_name).order_by('-date_posted')
        third_jobs = Job.objects.using('third').filter(agency=agency_name).order_by('-date_posted')

        # Combine all results
        combined_jobs = list(chain(default_jobs, first_jobs, second_jobs, third_jobs))

        # Sort the combined list by date_posted
        return sorted(combined_jobs, key=lambda job: job.date_posted, reverse=True)
class PostDetailView(DetailView):
    model = Job
    template_name = 'blog/job_detail.html'  # Add the template name explicitly



class PostCreateView(LoginRequiredMixin, CreateView):
    model = Job
    fields = ['job_title', 'agency']
    template_name = 'blog/job_form.html'  # Add the template name explicitly

    def form_valid(self, form):
        form.instance.agency = self.request.user.username  # Assign the username as agency
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Job
    fields = ['job_title', 'agency']
    template_name = 'blog/job_form.html'  # Add the template name explicitly

    def form_valid(self, form):
        form.instance.agency = self.request.user.username  # Assign the username as agency
        return super().form_valid(form)

    def test_func(self):
        job = self.get_object()
        return self.request.user.username == job.agency  # Compare the username with agency


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Job
    success_url = '/'
    template_name = 'blog/job_confirm_delete.html'  # Add the template name explicitly

    def test_func(self):
        job = self.get_object()
        return self.request.user.username == job.agency 

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
