from django.shortcuts import render


def home(request):
    return render(request, 'landing/home.html')


def sdr_agent(request):
    return render(request, 'landing/sdr.html')


def slides_index(request):
    decks = [
        {
            'slug': 'pitch',
            'title': 'Pitch Otomata',
            'description': 'Plateforme agentique pour l\'acquisition B2B',
            'slides_count': 11,
        },
        {
            'slug': 'competition',
            'title': 'Analyse Concurrentielle',
            'description': 'AI SDR, Data Enrichment, et positionnement',
            'slides_count': 12,
        },
    ]
    return render(request, 'slides/index.html', {'decks': decks})


def slides_deck(request, deck_name):
    template = f'slides/{deck_name}.html'
    decks = ['pitch', 'competition']
    current_index = decks.index(deck_name) if deck_name in decks else 0

    context = {
        'deck_name': deck_name,
        'decks': decks,
        'prev_deck': decks[current_index - 1] if current_index > 0 else None,
        'next_deck': decks[current_index + 1] if current_index < len(decks) - 1 else None,
    }
    return render(request, template, context)
