
from django.shortcuts import render, redirect
from .forms import QuoteForm
from .models import Source, Quote

def add_quote(request):
	if request.method == 'POST':
		form = QuoteForm(request.POST)
		if form.is_valid():
			source_name = form.cleaned_data['source_name']
			source_type = form.cleaned_data.get('source_type', '')
			source, _ = Source.objects.get_or_create(name=source_name, defaults={'type': source_type})
			quote = Quote(
				text=form.cleaned_data['text'],
				source=source,
				weight=form.cleaned_data['weight']
			)
			quote.save()
			return redirect('add_quote_success')
	else:
		form = QuoteForm()
	return render(request, 'quotes/add_quote.html', {'form': form})

def add_quote_success(request):
	return render(request, 'quotes/add_quote_success.html')
