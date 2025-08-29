from django.utils.dateparse import parse_date

def filter_transactions(request, qs):
    filter_type = request.GET.get('type', 'all')
    if filter_type in ['income', 'expense']:
        qs = qs.filter(type = filter_type)
    
    month = request.GET.get('month')
    if month:
        try:
            year, month_num = map(int, month.split('-'))
            qs = qs.filter(date__year = year, date__month = month_num)
        except ValueError:
            pass

    search_query = request.GET.get('search', '')
    if search_query:
        qs = qs.filter(description = search_query)

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date:
        qs = qs.filter(date__gte = parse_date(start_date))
    if end_date:
        qs = qs.filter(date__lte = parse_date(end_date))

    return qs, filter_type, search_query, start_date, end_date