from django.http import JsonResponse, HttpResponseBadRequest

from fast_youtube_search import search_youtube

from pytube import YouTube

from multiprocessing import Pool
from os import cpu_count

def get_info(result):
    try:
        url = YouTube(f"https://youtube.com/watch?v={result['id']}")
        url = url.streams.get_audio_only().url

        return {
            "title": result["name"],
            "url": url
        }
    except:
        return None

def search(request, query, max_results):
    if max_results > 50:
        return HttpResponseBadRequest("Can't find this many")
    elif max_results < 1:
        return HttpResponseBadRequest("Must be greater than zero")

    results = search_youtube(query, 4, max_results)

    processes = cpu_count() * 4

    with Pool(processes) as pool:
        response = [obj for obj in pool.map(get_info, results) if obj]

    return JsonResponse({"results": response})
