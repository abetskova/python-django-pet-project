import random
from django.db.models import F
from django.http import HttpResponseRedirect
from django.urls import reverse
def random_quote(request):
	quotes = Quote.objects.all()
	if not quotes:
		return render(request, 'quotes/random_quote.html', {'quote': None})
	# Выбор случайной цитаты с учетом веса
	weighted_quotes = [(q, q.weight) for q in quotes]
	quote = random.choices([q for q, w in weighted_quotes], weights=[w for q, w in weighted_quotes], k=1)[0]
	# Увеличиваем счетчик просмотров
	Quote.objects.filter(pk=quote.pk).update(views=F('views') + 1)
	return render(request, 'quotes/random_quote.html', {'quote': quote})

def vote_quote(request, quote_id, action):
	quote = Quote.objects.get(pk=quote_id)
	if action == 'like':
		quote.likes = F('likes') + 1
	elif action == 'dislike':
		quote.dislikes = F('dislikes') + 1
	quote.save()
	return HttpResponseRedirect(reverse('random_quote'))

def top_quotes(request):
	quotes = Quote.objects.order_by('-likes')[:10]
	return render(request, 'quotes/top_quotes.html', {'quotes': quotes})

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
