import os

def export_environ(request):
    """Exports OS environmental variables so they can be available in templates
    """
    return {k: v for k, v in os.environ.items()}
