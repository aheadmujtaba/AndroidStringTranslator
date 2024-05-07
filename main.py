# Import necessary libraries
import html
import os
import xml.etree.ElementTree as ET
import sys
from io import BytesIO
import re
import time
import shutil
from pathlib import Path
import asyncio
import urllib.parse

from gtranslate import perform_translate


# Define your translate function and other subroutines here

def main():
    OUTPUTlangs = sys.argv[3:]
    print("\n\n====================Welcome to String Transltor by Ahmad Mujtaba========================\n\n")
    
    if not OUTPUTlangs:
        OUTPUTlangs = ["af", "sq", "am", "ar", "hy", "az", "eu", "be", "bn", "bs", "bg", "ca", "ceb", "ny", "zh-CN",
                       "co", "hr", "cs", "da", "nl", "en", "eo", "et", "tl", "fi", "fr", "fy", "gl", "ka", "de", "el",
                       "gu", "ht", "ha", "haw", "iw", "hi", "hmn", "hu", "is", "ig", "id", "ga", "it", "ja", "jw", "kn",
                       "kk", "km", "rw", "ko", "ku", "ky", "lo", "la", "lv", "lt", "lb", "mk", "mg", "ms", "ml", "mt",
                       "mi", "mr", "mn", "my", "ne", "no", "or", "ps", "fa", "pl", "pt", "pa", "ro", "ru", "sm", "gd",
                       "sr", "st", "sn", "sd", "si", "sk", "sl", "so", "es", "su", "sw", "sv", "tg", "ta", "tt", "te",
                       "th", "tr", "tk", "uk", "ur", "ug", "uz", "vi", "cy", "xh", "yi", "yo",
                       "zu"]  # Add your list of output languages here

    # Create output directory
    OUTDIRECTORY = Path('out')
    if OUTDIRECTORY.exists():
        shutil.rmtree("out")
    os.makedirs("out")

    async def start_translate():
        coroutines = []
        for OUTPUTLANGUAGE in OUTPUTlangs:
            coroutines.append(perform_translate(OUTPUTLANGUAGE))
        await asyncio.gather(*coroutines)

    # Run the translation process
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_translate())
    print("Translation completed successfully.")


if __name__ == "__main__":
    main()
