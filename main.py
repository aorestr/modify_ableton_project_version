# -*- coding: utf-8 -*-
import os
import gzip
import typing
import shutil
import argparse
import binascii
import xml.etree.ElementTree as ET


ABLETON_VERSIONS = {
    "11.0.5": "11.0_433",
    "11.2.11": "11.0_11202"
}

# Arguments parser
parser = argparse.ArgumentParser(description="Script to change an Ableton project version")
parser.add_argument(
    "als_file", type=str,
    help="Relative or absolute path to Ableton project '.als' file."
         "It's been tested only with Ableton 10.0.5 and 11.2.11 projects."
)
parser.add_argument(
    "ableton_version_to_set", type=str, help="Version of Ableton that you would like the '.als' file to be set."
)
parser.add_argument(
    "--xml", action="store_true", default=False,
    help="If set, it does not remove the .xml file from the '.als' once created."
)
args = parser.parse_args()


def add_als_extension_if_it_is_not_set(als_file: str) -> str:
    """
    Add the extension ".als" to the selected file in case it does not have it
    :param als_file: file to check
    :return: the file with the correct extension
    """
    return als_file if als_file.endswith(".als") else f"{als_file}.als"


ALS_FILE = add_als_extension_if_it_is_not_set(args.als_file)
ABLETON_VERSION = args.ableton_version_to_set
XML = args.xml


def extract_xml_from_ableton_project(als_file: str) -> ET.ElementTree:
    """
    Extract the XML inner file from a Ableton project
    :param als_file: relative or absolute path to Ableton project ".als" file
    :return: if everything went right, it returns the project config as a XML tree
    """
    if os.path.isfile(als_file):
        with open(als_file, 'rb') as project_compressed:
            if not binascii.hexlify(project_compressed.read(2)) == b'1f8b':
                raise Exception("Nothing to do here")
        with gzip.open(als_file, 'rb') as project_uncompressed:
            project_xml_string = project_uncompressed.read().decode("utf-8")
            return ET.ElementTree(ET.fromstring(project_xml_string))
    else:
        raise FileNotFoundError(f"The Ableton project {als_file} does not exist")


def change_version(ableton_project_tree: ET.ElementTree, ableton_version: str) -> typing.NoReturn:
    """
    Modify the XML extracted from the .als file and set a different version
    :param ableton_project_tree: XML ElementTree extracted from the Ableton project
    :param ableton_version: the version you would like your Ableton project to be in
    :return:
    """
    tree_header = ableton_project_tree.getroot()
    if ableton_version not in ABLETON_VERSIONS:
        raise Exception(
            f"Version '{ableton_version}' is not valid. Please select one among the following: {ABLETON_VERSIONS}"
        )
    else:
        tree_header.set("MinorVersion", ABLETON_VERSIONS[ableton_version])
        tree_header.set("Creator", f"Ableton Live {ableton_version}")


def create_ableton_xml_file(als_file: str, ableton_project_tree: ET.ElementTree) -> str:
    """
    Write the new Ableton tree to a XML file
    :param als_file: relative or absolute path to Ableton project ".als" file
    :param ableton_project_tree: XML ElementTree extracted from the Ableton project
    :return: name of the XML file
    """
    als_xml = als_file.replace(".als", ".xml")
    ET.indent(ableton_project_tree)
    with open(als_xml, "wb+") as new_file:
        ableton_project_tree.write(new_file, encoding="UTF-8", xml_declaration=True)
    return als_xml


def generate_als(als_file: str, ableton_project_tree: ET.ElementTree, remove_xml: bool = True) -> typing.NoReturn:
    """
    Regenerate the Ableton project file with the new information
    :param als_file: relative or absolute path to Ableton project ".als" file
    :param ableton_project_tree: XML ElementTree extracted from the Ableton project
    :param remove_xml: if set to True, it removes the XML file after all is done
    :return:
    """
    als_xml = create_ableton_xml_file(als_file, ableton_project_tree)
    with open(als_xml, "rb") as f_in:
        with open(als_file, "wb") as f_out1:
            with gzip.GzipFile(als_xml, "wb", fileobj=f_out1) as f_out2:
                shutil.copyfileobj(f_in, f_out2)
    print(f"New Ableton project created in '{als_file}'")
    if remove_xml:
        print(f"Removed XML '{als_xml}'")
        os.remove(als_xml)


if __name__ == "__main__":
    ableton_xml = extract_xml_from_ableton_project(ALS_FILE)
    change_version(ableton_xml, ABLETON_VERSION)
    generate_als(ALS_FILE, ableton_xml, not XML)
