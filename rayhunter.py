import argparse
import os
import logging
import pathlib
import sys


class PyRayHunter:

    def __init__(self, output_folder: pathlib.Path):
        self._output_folder = output_folder
        
    def cleanup_files(self, device_id: str):
        logging.info(f"Cleaning up all files on {device_id} via ADB.")

    def get_ndjson_files(self, device_id: str):
        logging.info(f"Fetching all NDJSON files on {device_id} via ADB.")

    def get_pcap_files(self, device_id: str):
        logging.info(f"Fetching all PCAP files on {device_id} via API.")

    def get_qmdl_files(self, device_id: str):
        logging.info(f"Fetching all QMDL files on {device_id} via API.")

    def list_devices(self):
        logging.info(f"Listing all connected ADB devices.")


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
    parser.add_argument("-o", "--output", default=os.path.expandvars("~/rayhunter"), help="Path to write data (default: %(default)s)")
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

            rayhunter.get_pcap_files(arguments.device_id)

        if arguments.qmdl:

            rayhunter.get_qmdl_files(arguments.device_id)

        if arguments.ndjson:

            rayhunter.get_ndjson_files(arguments.device_id)

        if arguments.cleanup:

            rayhunter.cleanup_files(arguments.device_id)

    else:
        
        logging.error("No actions specified. Please specify --list flag or provide a --device with the appropriate action flags. See --help for more info.")