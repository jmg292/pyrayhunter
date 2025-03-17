import io
import logging
import requests
import urllib.parse

from .manifest import QmdlManifest


class RayhunterApi:

    @property
    def active_capture(self) -> bool:
        manifest = self.get_manifest()
        return manifest.current_entry is not None

    def __init__(self, hostname: str, port: int):
        self._url = f"http://{hostname}:{port}/"

    def _get_file_content(self, api_endpoint: str) -> bytes:
        file_content = io.BytesIO()
        file_url = urllib.parse.urljoin(self._url, api_endpoint)
        logging.info(f"Downloading file from: {file_url}")
        response = requests.get(file_url, stream=True)
        response.raise_for_status()
        for chunk in response.iter_content(chunk_size=4096):
            file_content.write(chunk)
        file_content.seek(0)
        return file_content.read()

    def get_manifest(self) -> QmdlManifest:
        manifest_url = urllib.parse.urljoin(self._url, "/api/qmdl-manifest")
        logging.info(f"Fetching manifest from: {manifest_url}")
        response = requests.get(manifest_url)
        response.raise_for_status()
        return QmdlManifest.from_dict(response.json())
    
    def get_pcap_file(self, filename: str) -> io.BytesIO:
        logging.info(f"Fetching PCAP file for capture: {filename}")
        api_endpoint = f"/api/pcap/{filename}"
        return self._get_file_content(api_endpoint)

    def get_qmdl_file(self, filename: str):
        logging.info(f"Fetching QDML file for capture: {filename}")
        api_endpoint = f"/api/qmdl/{filename}"
        return self._get_file_content(api_endpoint)
    
    def start_recording(self):
        start_recording_url = urllib.parse.urljoin(self._url, "/api/start-recording")
        logging.info(f"Starting recording with POST request to: {start_recording_url}")
        response = requests.post(start_recording_url)
        response.raise_for_status()
    
    def stop_recording(self):
        stop_recording_url = urllib.parse.urljoin(self._url, "/api/stop-recording")
        logging.info(f"Stopping recording with POST request to: {stop_recording_url}")
        response = requests.post(stop_recording_url)
        response.raise_for_status()
