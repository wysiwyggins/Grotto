from characterBuilder.models import Character

def character_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # get character detail
        character = None
        try:
            character = Character.objects.get(pk=request.session.get("character_pk"))
        except Character.DoesNotExist:
            pass
        request.character = character
        response = get_response(request)

        return response

    return middleware
