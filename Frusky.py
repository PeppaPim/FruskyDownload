import os
import requests
import zipfile
import sys
import time
from tqdm import tqdm  # Progress bar in CMD
from urllib.parse import urlparse  # Voor veilige bestandsnaam

# ANSI escape codes voor rode kleur
RED = "\033[91m"
RESET = "\033[0m"

# Automatisch de map bepalen waar de .exe draait
if getattr(sys, 'frozen', False):
    huidige_map = os.path.dirname(sys.executable)  # Map van de .exe
else:
    huidige_map = os.path.dirname(__file__)  # Map van het script

# Lijst met normale downloads
download_links = [
    "https://www.nirsoft.net/utils/winprefetchview.zip",
    "https://www.voidtools.com/Everything-1.4.1.1026.x86-Setup.exe",
    "https://www.nirsoft.net/utils/usbdeview.zip",
    "https://github.com/spokwn/BAM-parser/releases/download/v1.2.9/BAMParser.exe",
    "https://www.nirsoft.net/utils/lastactivityview.zip",
    "https://github.com/winsiderss/si-builds/releases/download/3.2.25056.2303/systeminformer-3.2.25056.2303-canary-setup.exe",
    "https://builds.dotnet.microsoft.com/dotnet/WindowsDesktop/9.0.6/windowsdesktop-runtime-9.0.6-win-x64.exe",
    "https://download.ericzimmermanstools.com/MFTECmd.zip"
]

# Links die als ZIP bewaard moeten worden in aparte map (niet uitpakken)
special_zip_links = [
    "https://www.brimorlabs.com/Tools/LiveResponseCollection-Cedarpelta.zip",
    "https://download.ericzimmermanstools.com/net9/TimelineExplorer.zip",
    "https://github.com/Yamato-Security/hayabusa/releases/download/v3.3.0/hayabusa-3.3.0-win-x64.zip"
]

# Map voor speciale ZIP-bestanden
special_zip_folder = os.path.join(huidige_map, "SpecialZips")
os.makedirs(special_zip_folder, exist_ok=True)

# Headers om detectie door de server te voorkomen
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    "Referer": "https://echo.ac/",
    "Accept-Language": "en-US,en;q=0.9"
}

def veilige_bestandsnaam(url):
    """Maakt een veilige bestandsnaam, zonder query-strings."""
    parsed = urlparse(url)
    naam = os.path.basename(parsed.path)
    if not naam:
        naam = "downloaded_file"
    return naam

def download_bestand(url, folder):
    """Downloadt een bestand en slaat het op in de opgegeven map met extra headers."""
    naam = veilige_bestandsnaam(url)
    bestandsnaam = os.path.join(folder, naam)

    try:
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024
        with open(bestandsnaam, "wb") as bestand, tqdm(
            total=total_size, unit='B', unit_scale=True, desc=f"{RED}⬇ {os.path.basename(bestandsnaam)}",
            ascii=" █▓▒░", bar_format="{l_bar}{bar} {n_fmt}/{total_fmt} [{rate_fmt}]" + RESET
        ) as progress_bar:
            for chunk in response.iter_content(block_size):
                bestand.write(chunk)
                progress_bar.update(len(chunk))

        return bestandsnaam

    except requests.exceptions.RequestException as e:
        print(f"{RED}Fout bij downloaden: {url} ({e}){RESET}")
        return None

def extract_exe(zip_pad, doel_map):
    """Pakt een zip-bestand uit:
    - Bevat het een map? Dan alles uitpakken.
    - Bevat het géén map, alleen losse bestanden? Dan alleen .exe's uitpakken.
    Daarna het zip-bestand zelf verwijderen.
    """
    try:
        with zipfile.ZipFile(zip_pad, "r") as zip_ref:
            namen = zip_ref.namelist()
            bevat_map = any("/" in naam for naam in namen)

            if bevat_map:
                zip_ref.extractall(doel_map)
            else:
                for naam in namen:
                    if naam.lower().endswith(".exe"):
                        zip_ref.extract(naam, doel_map)

        os.remove(zip_pad)

    except zipfile.BadZipFile:
        print(f"{RED}Fout: Kan {zip_pad} niet uitpakken (geen geldig ZIP-bestand).{RESET}")

def hacker_banner():
    """Toont de ASCII-banner in brute rode letters"""
    time.sleep(1)
    os.system("cls" if os.name == "nt" else "clear")
    print(RED + """
@@@@@@@@  @@@@@@@   @@@  @@@   @@@@@@   @@@  @@@  @@@ @@@  
@@@@@@@@  @@@@@@@@  @@@  @@@  @@@@@@@   @@@  @@@  @@@ @@@  
@@!       @@!  @@@  @@!  @@@  !@@       @@!  !@@  @@! !@@  
!@!       !@!  @!@  !@!  @!@  !@!       !@!  @!!  !@! @!!  
@!!!:!    @!@!!@!   @!@  !@!  !!@@!!    @!@@!@!    !@!@!   
!!!!!:    !!@!@!    !@!  !!!   !!@!!!   !!@!!!      @!!!   
!!:       !!: :!!   !!:  !!!       !:!  !!: :!!     !!:    
:!:       :!:  !:!  :!:  !:!      !:!   :!:  !:!    :!:    
 ::       ::   :::  ::::: ::  :::: ::    ::  :::     ::    
 :         :   : :   : :  :   :: : :     :   :::     :     
    """ + RESET)
    time.sleep(3)

def start_download():
    """Start het downloaden van bestanden en sluit de CMD na ENTER."""
    print(f"\n{RED}Download gestart...{RESET}\n")

    # Combineer gewone en speciale links
    alles_te_downloaden = download_links + special_zip_links

    for link in alles_te_downloaden:
        if link in special_zip_links:
            doel_map = special_zip_folder
        else:
            doel_map = huidige_map

        bestand_pad = download_bestand(link, doel_map)

        if bestand_pad and bestand_pad.endswith(".zip") and link not in special_zip_links:
            extract_exe(bestand_pad, huidige_map)

    hacker_banner()
    print(f"\n{RED}Download voltooid!{RESET}\n")

# Start direct bij het uitvoeren van de .exe
if __name__ == "__main__":
    start_download()
    input("\nDruk op ENTER om af te sluiten...")
    sys.exit()
