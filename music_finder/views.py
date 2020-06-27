from django.http import JsonResponse

from pyquery import PyQuery as pq
import urllib.parse

from pytube import YouTube

from multiprocessing import Pool
from os import cpu_count

def get_info(tup):
    query, link = tup

    try:
        info = YouTube(link).streams.get_audio_only()
    except:
        return None
    else:
        return {
            "title": query if info.title == "YouTube" else info.title,
            "url": info.url
        }

def search_youtube(query, max_results):
    if max_results > 100:
        raise ValueError("Can't find this many")
    elif max_results < 1:
        raise ValueError("Must be greater than zero")

    encoded_query = urllib.parse.quote(query)

    found = 0
    page = 1

    while found < max_results:
        url = f"https://youtube.com/results?search_query={encoded_query}&page={page}"

        empty = True

        for title in pq(url=url)("div.yt-lockup-content .yt-uix-tile-link"):
            found += 1

            if found > max_results:
                break

            empty = False

            yield query, "https://youtube.com" + pq(title).attr("href")

        if empty:
            break

        page += 1

def search(request, query, max_results):
    links = search_youtube(query, max_results)

    processes = cpu_count() * 4

    with Pool(processes) as pool:
        results = [result for result in pool.map(get_info, links) if result]

    return JsonResponse({"results": results})
