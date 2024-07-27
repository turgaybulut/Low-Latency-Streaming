import http.server
import socketserver
import os
import threading
import subprocess
import time
import qrcode

QR_PORT = 1234
RTMP_PORT = 1935
PLAYER_PORT = 8080
FFMPEG_PATH = "/home/turgay/bin/ffmpeg"
RTMP_URL = f"rtmp://localhost:{RTMP_PORT}/live/app"
GPAC_DASH_PATH = "/usr/local/var/www/"
NODE_PATH = "/usr/bin/node"
PLAYER_PATH = os.path.abspath("static")
SEG_DURATION = 4
CHUNK_DURATION = 1

FFMPEG_COMMAND = [
    FFMPEG_PATH,
    "-f", "flv",
    "-listen", "1",
    "-i", RTMP_URL,
    "-c:v", "h264",
    "-force_key_frames", f"expr:gte(t,n_forced*{SEG_DURATION})",
    "-profile:v", "baseline",
    "-map", "v:0", "-s:0", "320x180",
    "-map", "v:0", "-s:1", "384x216",
    "-map", "a:0", "-c:a", "aac", "-b:a", "128k",
    "-ldash", "1",
    "-streaming", "1",
    "-use_template", "1",
    "-use_timeline", "0",
    "-adaptation_sets", "id=0,streams=v id=1,streams=a",
    "-seg_duration", f"{SEG_DURATION}",
    "-frag_duration", f"{CHUNK_DURATION}",
    "-frag_type", "duration",
    "-utc_timing_url", "https://time.akamai.com/?iso",
    "-window_size", "5",
    "-extra_window_size", "5",
    "-remove_at_exit", "1",
    "-f", "dash",
    "-target_latency", "1.5",
    "-tune", "zerolatency",
    "-preset", "ultrafast",
    "-threads", "16",
    "-fflags", "nobuffer",
    os.path.join(GPAC_DASH_PATH, "ldash", "1.mpd"),
]

GPAC_DASH_COMMAND = [
    NODE_PATH,
    os.path.join(GPAC_DASH_PATH, "gpac-dash.js"),
    "-chunk-media-segments",
    "-cors",
    "-chunks-per-segment", f"{int(SEG_DURATION / CHUNK_DURATION)}",
]


def generate_qr():
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1,
    )
    qr.add_data(time.time())
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f"{PLAYER_PATH}/qr.png")


def start_qr_server():
    os.chdir(PLAYER_PATH)
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", QR_PORT), handler)
    print("QR code serving at port", QR_PORT)
    threading.Thread(target=httpd.serve_forever).start()
    return httpd


def start_ffmpeg():
    subprocess.run(FFMPEG_COMMAND)


def start_gpac_dash_server():
    subprocess.check_call(GPAC_DASH_COMMAND, cwd=GPAC_DASH_PATH)


class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PLAYER_PATH, **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()


def start_player_server():
    os.chdir(PLAYER_PATH)
    handler = CustomHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PLAYER_PORT), handler)
    print("Player serving at port", PLAYER_PORT)
    threading.Thread(target=httpd.serve_forever).start()
    return httpd


def main():
    generate_qr()

    httpd_qr = start_qr_server()
    ffmpeg_thread = threading.Thread(target=start_ffmpeg)
    ffmpeg_thread.start()
    gpac_dash_thread = threading.Thread(target=start_gpac_dash_server)
    gpac_dash_thread.start()
    httpd_player = start_player_server()

    try:
        while True:
            generate_qr()
            time.sleep(0.4)
    except KeyboardInterrupt:
        httpd_qr.shutdown()
        httpd_qr.server_close()
        httpd_player.shutdown()
        httpd_player.server_close()
        ffmpeg_thread.join()
        gpac_dash_thread.join()

if __name__ == "__main__":
    main()
