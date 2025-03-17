import argparse
import os
import logging
import pathlib
import sys

from rayhunter import RayhunterApi


class PyRayHunter:

    def __init__(self, output_folder: pathlib.Path):
        self._output_folder = output_folder
        
    def _save_http_file(self, file_contents: bytes, device_name: str, file_name: str):
        file_type = file_name.split(".")[1]
        parent_folder = self._output_folder.joinpath(*(device_name, file_type))
        if not parent_folder.exists():
            logging.info(f"Creating directory structure: {parent_folder}")
            parent_folder.mkdir(parents=True)
        output_path = parent_folder.joinpath(file_name)
        logging.info(f"Writing {len(file_contents)} bytes to path: {output_path}")
        with output_path.open(mode="wb") as outfile:
            bytes_written = outfile.write(file_contents)
        logging.info(f"Wrote {bytes_written} bytes to path: {output_path}")

    def cleanup_files(self, device_id: str):
        logging.info(f"Cleaning up all files on {device_id} via ADB.")

    def get_ndjson_files(self, device_id: str):
        logging.info(f"Fetching all NDJSON files on {device_id} via ADB.")

    def get_pcap_files(self, device_id: str):
        logging.info(f"Fetching all PCAP files on {device_id} via API.")
        api = self._get_http_api("127.0.0.1", 8000)
        manifest = api.get_manifest()
        for pcap_file in manifest.entries:
            logging.info(f"Downloading PCAP file for entry: {pcap_file.name}")
            pcap_file_contents = api.get_pcap_file(pcap_file.name)
            logging.info(f"PCAP: Downloaded {len(pcap_file_contents)} bytes")
            self._save_http_file(pcap_file_contents, device_id, f"{pcap_file.name}.pcap")

    def get_qmdl_files(self, device_id: str):
        logging.info(f"Fetching all QMDL files on {device_id} via API.")
        api = self._get_http_api("127.0.0.1", 8000)
        manifest = api.get_manifest()
        for qmdl_file in manifest.entries:
            logging.info(f"Downloading QMDL file for entry: {qmdl_file.name}")
            qmdl_file_contents = api.get_qmdl_file(qmdl_file.name)
            logging.info(f"QMDL: Expected {qmdl_file.qmdl_size_bytes} bytes, got {len(qmdl_file_contents)} bytes")
            self._save_http_file(qmdl_file_contents, device_id, f"{qmdl_file.name}.qmdl")

    def list_devices(self):
        logging.info(f"Listing all connected ADB devices.")

    @staticmethod
    def _get_http_api(hostname: str, port: int) -> RayhunterApi:
        api = RayhunterApi(hostname, port)
        if api.active_capture:
            logging.info("Stopping active capture before continuing")
            api.stop_recording()
        return api


def setup_logging(output_folder: pathlib.Path):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handlers = [
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(filename=output_folder.joinpath("pyrayhunter.log"))
    ]
    for handler in handlers:
        handler.setFormatter(formatter)
        logger.addHandler(handler)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog=__file__, description="Automated bulk data extraction and maintentance tool for Rayhunter (usb-only)")
    parser.add_argument("-o", "--output", default=os.path.expandvars("$HOME/rayhunter"), help="Path to write data (default: %(default)s)")
    parser.add_argument("-l", "--list", default=False, action="store_true", help="List connected USB devices and exit.")
    parser.add_argument("-c", "--cleanup", default=False, action="store_true", help="Remove all analysis files using ADB to free up disk space")
    parser.add_argument("-d", "--device", default=None, help="Perform actions against this device")
    parser.add_argument("-n", "--ndjson", default=False, action="store_true", help="Extract NDJSON files using ADB")
    parser.add_argument("-p", "--pcap", default=False, action="store_true", help="Extract PCAP files using the Rayhunter API")
    parser.add_argument("-q", "--qmdl", default=False, action="store_true", help="Extract QMDL files using the Rayhunter API")
    parser.add_argument("-a", "--all", default=False, action="store_true", help="Execute all extraction and cleanup actions against target device")
    arguments = parser.parse_args()

    arguments.output = pathlib.Path(arguments.output)
    if not arguments.output.exists():
        arguments.output.mkdir(parents=True)

    setup_logging(arguments.output)

    if arguments.device and arguments.all:
        for attribute in ["pcap", "qmdl", "ndjson", "cleanup"]:
            setattr(arguments, attribute, True)

    if arguments.list:

        PyRayHunter(arguments.output).list_devices()

    elif arguments.device is not None:

        rayhunter = PyRayHunter(arguments.output)
        
        if arguments.pcap:

            rayhunter.get_pcap_files(arguments.device)

        if arguments.qmdl:

            rayhunter.get_qmdl_files(arguments.device)

        if arguments.ndjson:

            rayhunter.get_ndjson_files(arguments.device)

        if arguments.cleanup:

            rayhunter.cleanup_files(arguments.device)

    else:
        
        logging.error("No actions specified. Please specify --list flag or provide a --device with the appropriate action flags. See --help for more info.")