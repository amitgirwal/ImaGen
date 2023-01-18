
def theme(request):
    if 'is_dark_theme' in request.session:
        is_dark_theme = request.session.get('is_dark_theme')
        return {'is_dark_theme': is_dark_theme}
    return {'is_dark_theme': False}