import subprocess
import qbittorrentapi
import time
import subprocess

# Command to install qBittorrent-nox
install_command = ["apt-get", "install", "qbittorrent-nox", "-y"]

# Function to start qbittorrent-nox subprocess
def start_qbittorrent():
    command = ["qbittorrent-nox"]
    try:
        subprocess.Popen(command)
        print("qbittorrent-nox started successfully.")
    except Exception as e:
        print(f"Error starting qbittorrent-nox: {e}")

# instantiate a Client using the appropriate WebUI configuration
conn_info = dict(
    host="localhost",
    port=8080,
    username="admin",
    password="adminadmin",
)

# Start qbittorrent-nox subprocess
start_qbittorrent()

# Wait for qBittorrent to initialize
time.sleep(5)

# Instantiate qBittorrent API client
qbt_client = qbittorrentapi.Client(**conn_info)

# the Client will automatically acquire/maintain a logged-in state
# in line with any request. therefore, this is not strictly necessary;
# however, you may want to test the provided login credentials.
try:
    qbt_client.auth_log_in()
except qbittorrentapi.LoginFailed as e:
    print(e)

# Add magnet link
magnet_link = 'magnet:?xt=urn:btih:BC006C06892064C31A5ECAFC0A32C94AACF0DE83&dn=www.1TamilMV.world%20-%20Queen%20Elizabeth%20%282023%29%20Tamil%20HQ%20HDRip%20-%20250MB%20-%20x264%20-%20AAC%20-%20ESub.mkv&tr=udp%3a%2f%2ftracker.openbittorrent.com%3a80%2fannounce&tr=udp%3a%2f%2ftracker.opentrackr.org%3a1337%2fannounce&tr=udp%3a%2f%2ftracker.openbittorrent.com%3a80%2fannounce&tr=udp%3a%2f%2ftracker.opentrackr.org%3a1337%2fannounce&tr=udp%3a%2f%2ftracker.trackerfix.com%3a85%2fannounce&tr=%2audp%3a%2f%2f9.rarbg.me%3a2960%2fannounce&tr=%2audp%3a%2f%2f9.rarbg.to%3a2980%2fannounce&tr=%2audp%3a%2f%2ftracker.thinelephant.org%3a12710%2fannounce&tr=%2audp%3a%2f%2ftracker.slowcheetah.org%3a14760%2fannounce&tr=wss%3a%2f%2fwstracker.online'
if qbt_client.torrents_add(urls=magnet_link) != "Ok.":
    raise Exception("Failed to add torrent.")

# display qBittorrent info
print(f"qBittorrent: {qbt_client.app.version}")
print(f"qBittorrent Web API: {qbt_client.app.web_api_version}")
for k, v in qbt_client.app.build_info.items():
    print(f"{k}: {v}")

# Polling to print progress, downloading speed, and total size downloaded
while True:
    for torrent in qbt_client.torrents_info():
        print(f"{torrent.hash[-6:]}: {torrent.name} - Progress: {torrent.progress * 100:.2f}%, Download Speed: {torrent.dlspeed / (1024 * 1024):.2f} MB/s, Downloaded Size: {torrent.downloaded / (1024 * 1024 * 1024):.2f} GB")
        if torrent.progress == 1:
            file_path = torrent.save_path + "/" + torrent.name
            print(f"Download completed. File path: {file_path}")
    time.sleep(5)  # Adjust the interval as needed

# logout
qbt_client.auth_log_out()
