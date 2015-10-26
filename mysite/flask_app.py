

from flask import Flask, render_template, request, send_file
import soundcloud
import wget
import os
import zipfile
import shutil

MYID = "None-ya"
MYSEC = "Business"

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

def file_self_destruct(file_path):
    os.remove(file_path)
    print "removed: " + str(file_path)

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template("landing.html")

@app.route('/download/<path:filename>')
def download(filename):
    return send_file(filename, as_attachment=True)

@app.route('/playerror/')
def landing():
    return render_template("playerror.html")

@app.route('/process/')
def processurl():

    target_url = request.args.get("soundcloudurl")
    client = soundcloud.Client(client_id=MYID)
    try:
        res_list = client.get("/resolve", url=target_url)
    except:
        return render_template("playerror.html", wrong_url=target_url)
    else:
        pl_name = (res_list.title).encode("utf-8")
        pl_artwork = res_list.artwork_url
        pl_user = (res_list.user["username"]).encode("utf-8")
        pl_number_of_tracks = str(len(res_list.tracks))
        folder_name = "mysite/downloads/" + pl_name + " - " + pl_user
        safe_folder_name = "downloads/" + pl_name + " - " + pl_user
        os.mkdir(folder_name)
        track_count = 1
        good_count = 0
        for track in res_list.tracks:
            if track["streamable"]:
		        step1_stream_url = track["stream_url"]
		        track_filename = folder_name + "/" + (track["title"]).encode("utf-8") + ".mp3"
		        step2_stream_url = client.get(step1_stream_url, allow_redirects=False)
		        step3_stream_url = step2_stream_url.location
		        this_dl = wget.download(step3_stream_url, out=track_filename)
		        good_count += 1

            track_count += 1

        zipf = zipfile.ZipFile((folder_name + ".zip"), 'w')
        zipdir(folder_name, zipf)
        zipf.close()
        shutil.rmtree(folder_name)
        return render_template("process.html", channel=pl_user, artwork_url=pl_artwork, playlist_name=pl_name, link=(safe_folder_name + ".zip"))


if __name__ == "__main__":
    app.run()
