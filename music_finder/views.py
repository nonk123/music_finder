from django.http import JsonResponse

from youtube_search import YoutubeSearch
from pytube import YouTube

from multiprocessing import Pool

def get_info(link):
    info = YouTube(link).streams.get_audio_only()

    return {
        "title": info.title,
        "url": info.url
    }

def search(request, query, max_results):
    results = YoutubeSearch(query, max_results).to_dict()
    links = ["https://youtube.com/" + r["link"] for r in results]

    with Pool() as pool:
        return JsonResponse({
            "results": pool.map(get_info, links)
        })
