import os
import requests
import zipfile
import sys
import time
from tqdm import tqdm  # Progress bar in CMD

# ANSI escape codes voor rode kleur
RED = "\033[91m"
RESET = "\033[0m"

# Automatisch de map bepalen waar de .exe draait
if getattr(sys, 'frozen', False):  
    huidige_map = os.path.dirname(sys.executable)  # Map van de .exe
else:
    huidige_map = os.path.dirname(__file__)  # Map van het script

# Lijst met bestanden die je wilt downloaden
download_links = [
    "https://www.nirsoft.net/utils/winprefetchview.zip",
    "https://www.voidtools.com/Everything-1.4.1.1026.x86-Setup.exe",
    "https://www.nirsoft.net/utils/usbdeview.zip",
    "https://github.com/spokwn/BAM-parser/releases/download/v1.2.7/BAMParser.exe",
    "https://www.nirsoft.net/utils/lastactivityview.zip",
    "https://github.com/winsiderss/si-builds/releases/download/3.2.25056.2303/systeminformer-3.2.25056.2303-canary-setup.exe"
]

# Headers om detectie door de server te voorkomen
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    "Referer": "https://echo.ac/",
    "Accept-Language": "en-US,en;q=0.9"
}

def download_bestand(url, folder):
    """Downloadt een bestand en slaat het op in de opgegeven map met extra headers."""
    bestandsnaam = os.path.join(folder, url.split("/")[-1])
    
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
    """Pakt een zip-bestand uit, bewaart alleen .exe-bestanden en verwijdert de rest."""
    try:
        with zipfile.ZipFile(zip_pad, "r") as zip_ref:
            zip_ref.extractall(doel_map)

            # Lijst van uitgepakte bestanden verkrijgen
            uitgepakte_bestanden = zip_ref.namelist()

        os.remove(zip_pad)

        # Behoud alleen .exe-bestanden
        for bestand in uitgepakte_bestanden:
            bestand_pad = os.path.join(doel_map, bestand)
            if not bestand.lower().endswith(".exe"):
                try:
                    if os.path.isfile(bestand_pad):
                        os.remove(bestand_pad)
                    elif os.path.isdir(bestand_pad):
                        os.rmdir(bestand_pad)
                except Exception as e:
                    print(f"Fout bij verwijderen van {bestand}: {e}")

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
    for link in download_links:
        bestand_pad = download_bestand(link, huidige_map)
        if bestand_pad and bestand_pad.endswith(".zip"):
            extract_exe(bestand_pad, huidige_map)

    hacker_banner()
    print(f"\n{RED}Download voltooid!{RESET}\n")

# Start direct bij het uitvoeren van de .exe
if __name__ == "__main__":
    start_download()

    # Direct sluiten na ENTER
    input("\nDruk op ENTER om af te sluiten...")
    sys.exit()
