from django.http import JsonResponse
from django.shortcuts import render

from .models import Image


def index(request):
    recent_images = Image.objects.order_by("-id")[:20]
    if len(recent_images) > 0:
        last_id = min([o.id for o in recent_images])
    else:
        last_id = -1

    return render(request, 'gallery/index.html', {'recent_images': recent_images, 'last_id': last_id})


def load_more(request):
    try:
        request_max_id = request.GET['max_id']
        request_max_id = int(request_max_id)
    except Exception as ex:
        print(ex)
        return JsonResponse({'recent_images': [], 'last_id': '-1'})

    more_images = Image.objects.filter(id__lt=request_max_id).order_by("-id")[:20]
    if len(more_images) == 0:
        return JsonResponse({'recent_images': [], 'last_id': '-1'})

    last_id = min([o.id for o in more_images]) if len(more_images) == 20 else -1
    more_images = [
        {
            'title': o.title,
            'description': o.description,
            'image_original_url': o.image_original.url,
            'image_thumbnail_url': o.image_thumbnail.url,
        }
        for o in more_images
    ]

    return JsonResponse({'more_images': more_images, 'last_id': last_id})
