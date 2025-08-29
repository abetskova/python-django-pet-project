from django import forms
from .models import Quote, Source

class QuoteForm(forms.ModelForm):
    source_name = forms.CharField(max_length=255, label='Источник (фильм, книга и т.д.)')
    source_type = forms.CharField(max_length=100, label='Тип источника', required=False)

    class Meta:
        model = Quote
        fields = ['text', 'weight']
        labels = {
            'text': 'Текст цитаты',
            'weight': 'Вес цитаты',
        }

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get('text')
        weight = cleaned_data.get('weight')
        source_name = cleaned_data.get('source_name')
        source_type = cleaned_data.get('source_type')

        # Проверка на уникальность цитаты
        if Quote.objects.filter(text=text).exists():
            self.add_error('text', 'Такая цитата уже существует.')

        # Проверка лимита цитат на источник
        source, _ = Source.objects.get_or_create(name=source_name, defaults={'type': source_type})
        if Quote.objects.filter(source=source).count() >= 3:
            self.add_error('source_name', 'У этого источника уже 3 цитаты.')

        return cleaned_data
