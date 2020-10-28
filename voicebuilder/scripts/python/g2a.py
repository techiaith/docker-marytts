#!/usr/bin/env python
import os
import sys

import http.client
from urllib.parse import urlencode
import xml.etree.ElementTree as ET

from argparse import ArgumentParser, RawTextHelpFormatter

DESCRIPTION = """


© Prifysgol Bangor University


"""

marytts_p2ipa_mapping = {'A':'ä','{':'æ','@':'ɐ','O':'ɔ','aU':'aʊ','AI':'aɪ','b':'b','tS':'tʃ',
'd':'d','D':'ð','E':'ɛ','r=':'ɝ','EI':'eɪ','f':'f','g':'ɡ','h':'h','I':'ɪ','i':'i','dZ':'dʒ',
'k':'k','l':'l','m':'m','n':'n','N':'ŋ','@U':'oʊ','OI':'ɔɪ','p':'p','r':'ɹ','s':'s','S':'ʃ','t':'t',
'T':'θ','U':'ʊ','u':'u','V':'ɐ','v':'v','w':'w','j':'j','z':'z','Z':'ʒ'}



class MaryTTSAPI(object):

    def __init__(self):

        self.marytts_host = "127.0.0.1"
        self.marytts_port = 59125


    def get_allophones_xml(self, lang, text):
        """Given a message in message,
           return a response in the appropriate
           format."""

        raw_params = {"INPUT_TEXT": text,
                "INPUT_TYPE": "TEXT",
                "OUTPUT_TYPE": "ALLOPHONES",
                "LOCALE": lang,
                }

        params = urlencode(raw_params)
        headers = {}

        # Open connection to self.host, self.port.
        conn = http.client.HTTPConnection(self.marytts_host, self.marytts_port)

        conn.request("POST", "/process", params, headers)
        response = conn.getresponse()
        if response.status != 200:
            #print response.getheaders()
            raise RuntimeError("{0}: {1}".format(response.status, response.reason))
        return response.read()


    def g2a(self, lang, text):
        t = ''
        ns = {'m':'http://mary.dfki.de/2002/MaryXML'}

        allophones_xml = self.get_allophones_xml(lang, text)
        root = ET.fromstring(allophones_xml)

        for syllable in root.findall('./m:p/m:s/m:phrase/m:t/m:syllable', ns):
            for phoneme in syllable.findall('./m:ph', ns):
                mp = phoneme.attrib['p']
                t = t + marytts_p2ipa_mapping[mp]


            if 'stress' in syllable.attrib:
                stress = syllable.attrib['stress']
                if (stress == "1"):
                    t = t + "'"

            t = t + "."

        t = t[:-1]
        return t



def main(wordlist_file_path, locale, output_file_path, **args):
    mtts = MaryTTSAPI()
    with open(output_file_path, "w", encoding='utf-8') as out:
        with open(wordlist_file_path, "r", encoding='utf-8') as wordlist:
            for word in wordlist:
               word = word.rstrip()
               a = mtts.g2a(locale, word)
               print (a)
               out.write("%s\t%s\n" % (word, a))


if __name__ == "__main__":
    parser = ArgumentParser(description=DESCRIPTION, formatter_class=RawTextHelpFormatter)
    parser.add_argument("-w", dest="wordlist_file_path", required=True, help="lleoliad ffeiliau geiriau / location of wordlist file")
    parser.add_argument("-l", dest="locale", required=True, help="iaith ffeil rhestr geiriau / locale of word list")    
    parser.add_argument("-o", dest="output_file_path", default="g2a.dict")    
    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))


