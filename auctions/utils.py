from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def paginate_listings(request, listings, per_page):
    paginator = Paginator(listings, per_page)
    page = request.GET.get('page')
    
    try:
        paginated_listings = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paginated_listings = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        paginated_listings = paginator.page(paginator.num_pages)

    return paginated_listings
