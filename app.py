from asyncio import streams
from flask import Flask, render_template, request
from flask import send_file, send_from_directory, safe_join, abort #odeslani vida do prohlizece
from dwnScripts.getVideoInfo import getVideoInfo
import datetime
import pytube
import io, os #k hledání cesty stazeneho videa(os k odstranení videa)

app = Flask(__name__)


@app.route("/")
def mainPage():
    #options={
        #"format": "bestaudio/best",
        #"audioformat":"mp3"
    #}
    #url = 'https://www.youtube.com/watch?v=RvoqC0btbWA&t=47s&ab_channel=ongakuu'

    #with youtube_dl.YoutubeDL(options) as ydl:
        #ydl.download([url])

    return render_template("mainPage.html")


@app.route("/videoDown", methods=["POST"])
def downloadPage():

    videoURL = request.form["videoURL"]
    print(videoURL)

    try:
        videoInfo = getVideoInfo(videoURL)
        return render_template("downloadPage.html", video=videoInfo, success=True)
    except:
        return render_template("downloadPage.html", success=False)

@app.route("/sendFile", methods=["POST"])
def sendFile():

    fileToDownload = request.form["streams"]
    fileToDownloadUrl = request.form["url"]

    print(fileToDownload)
    print(fileToDownloadUrl)


    video = pytube.YouTube(fileToDownloadUrl)

    streamToDown = video.streams.get_by_itag(fileToDownload)

    download_path = streamToDown.download()

    returnFile = io.BytesIO()

    with open(download_path, 'rb') as f:
        returnFile.write(f.read())
    returnFile.seek(0)


    os.remove(download_path)

    fname = download_path.split("//")[-1]

    return send_file(returnFile, as_attachment=True, attachment_filename=fname)







app.run(debug=True)