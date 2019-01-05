import urllib.request
import xml.etree.ElementTree as ET
import os
import requests
from lib import short_url
directory = "./sources/onsen/"
onsen_program_url = "http://www.onsen.ag/app/programs.xml"




class OnsenRadio():

    def __init__(self, dir=directory):
        self._dir = directory
        self._url = onsen_program_url
        self._request = urllib.request.Request(self._url)
        

    def download_mp3(self, url):
        import shutil

        file_name = os.path.basename(url)


        not_finished_temp_dir = self._dir + "downloading\\"
        
        if not os.path.exists(not_finished_temp_dir):
            os.mkdir(not_finished_temp_dir)


        urllib.request.urlretrieve(url=url,
                                   filename=not_finished_temp_dir+file_name,)
        before = not_finished_temp_dir+file_name
        after = self._dir + file_name
        shutil.move(before, after)

    def listup_all_programs(self):
        """
        return parsed xml tag
        """
        with urllib.request.urlopen(self._request) as response:
            XmlData = response.read()

            root = ET.fromstring(XmlData)

            for child in root:
                for title in child.iter("title"):
                    yield title.text.replace("\u3000","")
            return None
    
    def show_program_contents(self, name):
        from bs4 import BeautifulSoup
        from pprint import pformat
        with urllib.request.urlopen(self._request) as response:
            XmlData = response.read()

            root = ET.fromstring(XmlData)

            program_contents = dict()

            for child in root:
                for title in child.iter("title"):
                    if title.text.startswith(name):
                        program_contents["id"] = child.attrib["id"]
                        program_contents["info_url"] = "http://www.onsen.ag/data/api/getMovieInfo/"+child.attrib["id"]
                        program_contents["program_url"] = "https://www.onsen.ag/program/"+child.attrib["id"]
                        for item in child:
                            program_contents[item.tag] = item.text

            # soup = BeautifulSoup(urllib.request.urlopen(program_contents["program_url"]), "html.parser")
            h = urllib.request.urlopen(program_contents["info_url"])
            d = eval(h.read().decode('utf-8')[9:-3])
            program_contents.update(d)
            return program_contents

    def search_mp3_from_folder(self, name):
        """
        return list(filename)
        """
        radio_id = self.show_program_contents(name)["id"]
        file_list = [file for file in os.listdir(self._dir)
                     if file.startswith(radio_id)]

        return sorted(file_list)


if __name__ == "__main__":

    radio = OnsenRadio()
    data = radio.search_mp3_from_folder("ほめ")
    print(data)