import pytube


def getVideoInfo(videoURL):
    
    # potrebne info extraktuje se pouze potrebne
        # nahledovy obrazek
        # nazev videa
        # autor

    video = pytube.YouTube(videoURL)


    result = {
        "thumbnail": video.thumbnail_url,
        "title": video.title,
        "author": video.author,
        "url": video.watch_url,
        "streams": video.streams.filter(progressive=True).all(),
        "audio": video.streams.filter(only_audio=True).first()
    }


    for stream in result['streams']:
        print(stream)

    return result