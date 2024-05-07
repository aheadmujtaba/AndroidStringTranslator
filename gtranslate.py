#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import html
import os
import xml.etree.ElementTree as ET
import sys
import shutil
from pathlib import Path
import re
import urllib.parse
import aiohttp
import asyncio


async def translate_internal(to_translate, to_language="auto", language="auto"):
    to_translate = serialize_text(to_translate, language)
    session_timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(trust_env=True, timeout=session_timeout) as session:
        translate_url = "https://translate.google.com/m?sl=%s&tl=%s&q=%s&op=translate" % (
            language, to_language, to_translate.replace(" ", "+"))
        async with session.get(translate_url) as r:
            translation = await extract_translation_from_html(await r.text())
            print("Translation: " + to_translate + " -> " + translation)
            return translation


async def extract_translation_from_html(html_text):
    before_trans = 'class="result-container">'
    after_trans = '</div>'
    parsed1 = html_text[html_text.find(before_trans) + len(before_trans):]
    parsed2 = parsed1[:parsed1.find(after_trans)]
    parsed3 = re.sub('% ([ds])', r' %\1', parsed2)
    parsed4 = re.sub('% ([\d]) \$ ([ds])', r' %\1$\2', parsed3).strip()
    return deserialize_text(html.unescape(parsed4).replace("'", r"\'"))


def serialize_text(text, language):
    tag_match_regex = re.compile('<.*?>')
    text = re.sub(tag_match_regex, '', text)
    text = re.sub(r'\\', r'\\\\', text)
    text = text.replace("\n", "\\n")
    text = text.replace("@", "\\@")
    text = text.replace("?", "\\?")
    text = text.replace("\"", "\\\"")
    return urllib.parse.quote_plus(text)


def deserialize_text(text):
    text = text.replace('\\ ', '\\').replace('\\ n ', '\\n').replace('\\n ', '\\n').replace('/ ', '/')
    text = text.replace("\n", "\\n")
    text = text.replace("@", "\\@")
    text = text.replace("?", "\\?")
    text = text.replace("\"", "\\\"")
    return text


async def perform_translate(OUTPUTLANGUAGE):
    os.makedirs("out/values-{OUTPUTLANGUAGE}".format(OUTPUTLANGUAGE=OUTPUTLANGUAGE))
    OUTFILE = "out/values-{OUTPUTLANGUAGE}/strings.xml".format(OUTPUTLANGUAGE=OUTPUTLANGUAGE)
    tree = ET.parse(INFILE)
    root = tree.getroot()
    for i in range(len(root)):
        isTranslatable = root[i].get('translatable')
        if (root[i].tag == 'string') & (isTranslatable != 'false'):
            totranslate = root[i].text
            if (totranslate != None):
                root[i].text = await translate_internal(totranslate, OUTPUTLANGUAGE, INPUTLANGUAGE)
            if len(root[i]) != 0:
                for element in range(len(root[i])):
                    root[i][element].text = " " + await translate_internal(root[i][element].text, OUTPUTLANGUAGE,
                                                                           INPUTLANGUAGE)
                    root[i][element].tail = " " + await translate_internal(root[i][element].tail, OUTPUTLANGUAGE,
                                                                           INPUTLANGUAGE)
        if (root[i].tag == 'string-array'):
            for j in range(len(root[i])):
                isTranslatable = root[i][j].get('translatable')
                if (root[i][j].tag == 'item') & (isTranslatable != 'false'):
                    totranslate = root[i][j].text
                    if (totranslate != None):
                        root[i][j].text = await translate_internal(totranslate, OUTPUTLANGUAGE, INPUTLANGUAGE)
                    if len(root[i][j]) != 0:
                        for element in range(len(root[i][j])):
                            root[i][j][element].text = " " + await translate_internal(root[i][j][element].text,
                                                                                      OUTPUTLANGUAGE, INPUTLANGUAGE)
                            root[i][j][element].tail = " " + await translate_internal(root[i][j][element].tail,
                                                                                      OUTPUTLANGUAGE, INPUTLANGUAGE)
    tree.write(OUTFILE, encoding='utf-8')


async def start_translate():
    coroutines = []
    for OUTPUTLANGUAGE in OUTPUTlangs:
        coroutines.append(perform_translate(OUTPUTLANGUAGE))
    await asyncio.gather(*coroutines)


INFILE = sys.argv[1]
INPUTLANGUAGE = sys.argv[2]
OUTPUTlangs = sys.argv[3:]

if not OUTPUTlangs:
    OUTPUTlangs = ["af", "sq", "am", "ar", "hy", "az", "eu", "be", "bn", "bs", "bg", "ca", "ceb", "ny", "zh-CN", "co",
                   "hr", "cs", "da", "nl", "en", "eo", "et", "tl", "fi", "fr", "fy", "gl", "ka", "de", "el", "gu", "ht",
                   "ha", "haw", "iw", "hi", "hmn", "hu", "is", "ig", "id", "ga", "it", "ja", "jw", "kn", "kk", "km",
                   "rw", "ko", "ku", "ky", "lo", "la", "lv", "lt", "lb", "mk", "mg", "ms", "ml", "mt", "mi", "mr", "mn",
                   "my", "ne", "no", "or", "ps", "fa", "pl", "pt", "pa", "ro", "ru", "sm", "gd", "sr", "st", "sn", "sd",
                   "si", "sk", "sl", "so", "es", "su", "sw", "sv", "tg", "ta", "tt", "te", "th", "tr", "tk", "uk", "ur",
                   "ug", "uz", "vi", "cy", "xh", "yi", "yo", "zu"]
    OUTPUTlangs.remove(INPUTLANGUAGE)
if not INFILE:
    INFILE = "strings.xml"
if not INPUTLANGUAGE:
    INPUTLANGUAGE = "en"

print("=================================================\n\n")

OUTDIRECTORY = Path('out')
if OUTDIRECTORY.exists():
    shutil.rmtree("out")
os.makedirs("out")

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(start_translate())
print("done")
