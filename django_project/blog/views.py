from django.shortcuts import redirect, render
from .models import Job
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from urllib.parse import urlencode

states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 
'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 
'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 
'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 
'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
]

def home(request):
    job_list = Job.objects.all()
    paginator = Paginator(job_list, 20)  

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/home.html', {'page_obj': page_obj})


def search_results(request):
    # job_list = Job.objects.all()
    # paginator = Paginator(job_list, 20)

    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)

    # Get search parameters from the GET request
    state_code = request.GET.get('state_code')
    title = request.GET.get('title')
    location = request.GET.get('location')
    employment_type = request.GET.get('employment_type')
    industries = request.GET.get('industries')
    query = Job.objects.all()

    # Apply filters if parameters are provided
    if state_code:
        query = query.filter(state_code=state_code)
    if title:
        query = query.filter(title__icontains=title)
    if location:
        query = query.filter(location__icontains=location)
    if employment_type:
        query = query.filter(employment_type__icontains=employment_type)
    if industries:
        query = query.filter(industries__icontains=industries)

    # Set up pagination
    paginator = Paginator(query, 20)  # 20 jobs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Rebuild the query string without 'page' parameter
    query_params = request.GET.copy()
    if 'page' in query_params:
        del query_params['page']
    query_string = urlencode(query_params, doseq=True)
    
    return render(request, 'blog/search_form.html',
                  {
                        'page_obj': page_obj,
                        'states': states,
                        'selected_states': state_code,
                        'query_string': query_string
                  })

    # return render(request, 'blog/search_form.html', {'page_obj': page_obj})

# def add_to_favorites(request, job_id):
#     # Get the list of favorites from the session, or an empty list if none exist
#     favorites = request.session.get('favorites', [])
#     # Add job_id to favorites list if not already included
#     if job_id not in favorites:
#         favorites.append(job_id)
#         request.session['favorites'] = favorites  # Save back to session
#         messages.add_message(request, messages.INFO, 'This job was added to your favorites.')
#     else:
#         messages.add_message(request, messages.INFO, 'This job is already in your favorites.')
    
#     # Stay on the same page, or wherever appropriate
#     return redirect(request.META.get('HTTP_REFERER', 'home'))


def add_to_favorites(request, job_id):
    # Convert job_id to string if it's not, to ensure consistent handling in session
    job_id = str(job_id)

    # Get the list of favorites from the session, or an empty list if none exist
    favorites = request.session.get('favorites', [])

    # Add job_id to favorites list if not already included
    if job_id not in favorites:
        favorites.append(job_id)
        request.session['favorites'] = favorites  # Save back to session
        request.session.save()
        messages.add_message(request, messages.INFO, 'This job was added to your favorites.')
    else:
        messages.add_message(request, messages.INFO, 'This job is already in your favorites.')
    
    # Redirect back to the referring page, if possible, or to the home page
    return redirect(request.META.get('HTTP_REFERER', '/'))  # Use '/' as a more neutral default

def favorite_jobs(request):
    # Retrieve the list of favorite job IDs from the session
    favorite_ids = request.session.get('favorites', [])
    print("Favorite IDs:", favorite_ids)  # Debug statement to see what IDs are retrieved

    # Fetch the jobs from the database based on the IDs stored in the session
    if favorite_ids:
        jobs = Job.objects.filter(id__in=favorite_ids)
        print("Jobs found:", jobs.count())  # Debug to see if jobs are being found
    else:
        jobs = Job.objects.none()

    return render(request, 'blog/favorite_jobs.html', {'jobs': jobs})

def remove_from_favorites(request, job_id):
    # Convert job_id to the correct type if necessary
    job_id = str(job_id)
    # Retrieve the list of favorite job IDs from the session
    favorite_ids = request.session.get('favorites', [])
    # Remove the job ID from the list if it exists
    if job_id in favorite_ids:
        favorite_ids.remove(job_id)
        request.session['favorites'] = favorite_ids  # Update the session
        request.session.save()  # Make sure to save the session changes
    # Redirect to the favorite jobs page or return an appropriate response
    return HttpResponseRedirect(reverse('favorite-jobs'))

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
