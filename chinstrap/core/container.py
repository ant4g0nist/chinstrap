from importlib.metadata import files
import io
from operator import truediv
import docker
import tarfile
from typing import List
from os.path import split
from chinstrap import Helpers
from chinstrap.Helpers import fatal

SmartPyImage = "ant4g0nist/smartpy"
SmartPyImageTag = "latest"

LigoImage    = "ligolang/ligo"
LigoImageTag = "0.34.0"

def getDockerClient():
    return docker.from_env()

def pullImage(image, tag):
    client = getDockerClient()
    try:
        client.api.pull(image, tag=tag, stream=False, decode=True)
        return True, ""
    except docker.errors.ImageNotFound:
        return False, f"\n{image}:{tag}, repository does not exist or may require 'docker login'"

def addFilesToContainer(container, files, location):
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode='w:gz') as archive:
        for filename in files:
            with open(filename, 'rb') as current_file:
                current_file_data = current_file.read()
                current_file_buffer = io.BytesIO(initial_bytes=current_file_data)
                _, short_filename = split(filename)
                archive.add(filename, arcname=short_filename)
    buffer.seek(0)
    container.put_archive(
        location,
        buffer,
    )

def runLigoContainer(command, files_to_add = [], detach=True, volumes={}, image=LigoImage, tag=LigoImageTag):
    try:
        return runCommandInContainer(image, tag, command, files_to_add, detach, volumes)
    except docker.errors.ImageNotFound:
        fatal('\nLigo docker image not found. Please run "chinstrap install -c ligo" to download Ligo image.')

def runSmartPyContainer(command, files_to_add = [], detach=True, volumes = {}, image=SmartPyImage, tag=SmartPyImageTag):
    try:
        return runCommandInContainer(image, tag, command, files_to_add, detach, volumes)
    except docker.errors.ImageNotFound:
        fatal('\nSmartPy docker image not found. Please run "chinstrap install -c smartpy" to download SmartPy image.')

def runCommandInContainer(image, tag, command, files_to_add = [], detach=True, volumes = {}, auto_remove=True):
    client = getDockerClient()
    container = client.containers.create( 
        image=f'{image}:{tag}',
        command=command,
        detach=detach,
        volumes=volumes,
        auto_remove=auto_remove
    )

    if files_to_add:
        addFilesToContainer(container, files_to_add, '/root/')

    container.start()
    return container