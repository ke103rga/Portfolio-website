from django.shortcuts import render
from .models import Project, Category, StudySource

navigation_menu = [
    {"page_title": "Home", "url_name": "home"},
    {"page_title": "Studying", "url_name": "studying"},
    {"page_title": "Resume", "url_name": "resume"}
]


def index(requests):
    main_projects = Project.objects.filter(is_published=True).order_by("global_priory")[:3]
    categories = Category.objects.all()
    context = {
        "main_projects": main_projects,
        "navigation_menu": navigation_menu,
        "categories": categories,
        "selected_section": "Home"
    }
    return render(requests, "portfolioApp/index.html", context=context)


def studying(requests):
    study_sources = StudySource.objects.all().order_by("order")
    context = {
        "navigation_menu": navigation_menu,
        "selected_section": "Studying",
        "study_sources": study_sources
    }
    return render(requests, "portfolioApp/studying.html", context=context)


def resume(requests):

    context = {
        "navigation_menu": navigation_menu,
        "selected_section": "Resume"
    }
    return render(requests, "portfolioApp/resume.html", context=context)


def category(requests, type):
    category_projects = Project.objects.filter(category__slugname=type).filter(is_published=True).order_by("group_priory")
    projects_headers = list(map(lambda project: project.title, category_projects))
    category = Category.objects.get(slugname=type)
    print(category.title)
    context = {
        "navigation_menu": navigation_menu,
        "category_projects": category_projects,
        "projects_headers": projects_headers,
        "category": category,
        "it": range(50)
    }
    return render(requests, "portfolioApp/category.html", context=context)

