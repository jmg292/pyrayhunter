import requests
import logging
import json
import urllib.parse

from .manifest import QmdlManifest


class RayhunterApi:

    @property
    def active_capture(self) -> bool:
        raise NotImplementedError()

    def __init__(self, hostname: str, port: int):
        self._url = f"http://{hostname}:{port}/"

    def get_manifest(self) -> QmdlManifest:
        manifest_url = urllib.parse.urljoin(self._url, "/api/qmdl-manifest")
        logging.info(f"Fetching manifest from: {manifest_url}")
        response = requests.get(manifest_url)
        return QmdlManifest.from_dict(response.json())
    
    def get_pcap_file(self, filename: str):
        raise NotImplementedError()
    
    def get_qmdl_file(self, filename: str):
        raise NotImplementedError()
    
    def start_recording(self):
        raise NotImplementedError()
    
    def stop_recording(self):
        raise NotImplementedError()
