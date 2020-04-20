from django.http import JsonResponse

from youtube_dl import YoutubeDL
from youtube_search import YoutubeSearch

dl = YoutubeDL(params={
    "extractaudio": True,
    "noplaylist": True,
    "audioformat": "mp3"
})

def search(request, query, max_results):
    results = YoutubeSearch(query, max_results).to_dict()
    links = ["https://youtube.com/" + r["link"] for r in results]

    results = []

    for link in links:
        info = dl.extract_info(link, download=False)

        results.append({
            "title": info["title"],
            "url": info["requested_formats"][-1]["url"]
        })

    return JsonResponse({
        "results": results
    })
