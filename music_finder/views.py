from django.http import JsonResponse, HttpResponseBadRequest

from youtube_search import YoutubeSearch
from youtube_dl import YoutubeDL

from multiprocessing import Pool

ydl_params = {
    "format": "bestaudio/mp4",
    "noplaylist": True,
}

def get_info(link):
    with YoutubeDL(ydl_params) as ydl:
        try:
            info = ydl.extract_info(link, download=False)
        except:
            return None

    return {
        "title": info["title"],
        "url": info["url"]
    }

def search(request, query, max_results):
    if max_results < 1:
        return HttpResponseBadRequest("`max_results' must be > 0")

    results = YoutubeSearch(query, max_results).to_dict()
    links = ["https://youtube.com/" + r["link"] for r in results]

    with Pool() as pool:
        results = [result for result in pool.map(get_info, links) if result]
        return JsonResponse({"results": results})
