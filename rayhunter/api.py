import requests
import logging


class RayhunterApi:

    @property
    def active_capture(self) -> bool:
        raise NotImplementedError()

    def __init__(self, hostname: str, port: int):
        self._url = f"http://{hostname}:{port}/api"

    def get_manifest(self):
        raise NotImplementedError()
    
    def get_pcap_file(self, filename: str):
        raise NotImplementedError()
    
    def get_qmdl_file(self, filename: str):
        raise NotImplementedError()
    
    def start_recording(self):
        raise NotImplementedError()
    
    def stop_recording(self):
        raise NotImplementedError()
