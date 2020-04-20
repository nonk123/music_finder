from django.http import JsonResponse

from youtube_dl import YoutubeDL
from youtube_search import YoutubeSearch

from multiprocessing.pool import ThreadPool

dl = YoutubeDL(params={
    "extractaudio": True,
    "noplaylist": True,
    "audioformat": "mp3"
})

def get_info(link):
    info = dl.extract_info(link, download=False)

    return {
        "title": info["title"],
        "url": info["requested_formats"][-1]["url"]
    }

def search(request, query, max_results):
    results = YoutubeSearch(query, max_results).to_dict()
    links = ["https://youtube.com/" + r["link"] for r in results]

    return JsonResponse({
        "results": ThreadPool().map(get_info, links)
    })
