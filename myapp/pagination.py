from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def paginate_queryset(total_item,per_page, request):
    paginator = Paginator(total_item, per_page)
    page = request.GET.get('page', 1)
    
    


    
    

