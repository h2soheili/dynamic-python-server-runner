import shutil
from typing import Any, List
from random import randint
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas
from app.template.generate_script import generate_script_for_image
from app.utils.global_log import log_factory
from pathlib import Path
import subprocess
import os
import docker
import sys
import uuid

router = APIRouter()
logger = log_factory.get_logger(__name__)


@router.get("/", response_model=List[schemas.DockerImageInDB])
def read_instances() -> Any:
    return []


@router.post("/", response_model=Any)
def create_instance(
        *,
        instance_in: schemas.DockerImageCreate
) -> Any:
    try:
        user_id = 10
        script_name = instance_in.script_name + '-' + str(uuid.uuid4())[:8]
        script_content = instance_in.script_content or ""

        def audit(event, args):
            if event == 'compile':
                raise Exception('malicious code!')

        sys.addaudithook(audit)
        from_folder_dir = "app/template"
        destination_folder_dir = f"temp_images/{user_id}/{script_name}"
        files_to_copy = ['Dockerfile', '.env', 'requirements.txt', 'main.py', 'sdk.py', 'logger.py']
        '''
        create temp folder
        '''
        Path(f"{destination_folder_dir}").mkdir(parents=True, exist_ok=True)
        '''
        copy files to temp folder
        '''
        for file_name in files_to_copy:
            shutil.copyfile(f"{from_folder_dir}/{file_name}", f"{destination_folder_dir}/{file_name}",
                            follow_symlinks=True)
        '''
        update user specific script and env
        '''
        file_name = f"{destination_folder_dir}/script.py"
        env_file_name = f"{destination_folder_dir}/.env"
        with open(file_name, 'x', encoding='utf-8') as f:
            f.write(generate_script_for_image(script_content))
        with open(env_file_name, 'a', encoding='utf-8') as f:
            env_content = f"USER_ID={user_id}\n" \
                          f"SCRIPT_NAME={script_name}\n"
            f.write(env_content)
        '''
        build image
        '''
        image_name = f"user-{user_id}/{script_name}"
        image_tag = '1.0.0'
        container_name = f"user-{user_id}-{script_name}-{image_tag}"
        build_command = f"docker build -t {image_name}:{image_tag} {destination_folder_dir}"
        os.system(build_command)
        '''
        run container
        '''
        run_command = f"docker container run -d -p 7000:7000 --name {container_name} {image_name}:{image_tag}"
        os.system(run_command)
        return {"status": 200, "image_name": image_name, "container_name": container_name}
    except Exception as error:
        logger.error('docker_image create_instance', error=error)
        return error


'''
docker sdk
https://docs.docker.com/engine/api/sdk/examples/
'''


class ContainerObject:
    def __init__(self, container_id: str, container_name: str, container_status: str):
        self.id = container_id
        self.name = container_name
        self.status = container_status


class ImageObject:
    def __init__(self, image_id: str, image_name: str, ):
        self.id = image_id
        self.name = image_name


@router.get("/container", response_model=List[ContainerObject])
def get_containers() -> Any:
    try:
        res = []
        client = docker.from_env()
        for container in client.containers.list():
            res.append(ContainerObject(container.id, container.name, container.status))
        return res
    except Exception as error:
        logger.error('docker_image get_containers', error=error)
        return error


@router.get("/container/stop-all", response_model=Any)
def stop_all_containers() -> Any:
    try:
        client = docker.from_env()
        for container in client.containers.list():
            container.stop()
    except Exception as error:
        logger.error('docker_image stop_all_containers', error=error)
        return error


@router.get("/container/{container_id}/logs", response_model=Any)
def get_container_logs(
        container_id: str,
) -> Any:
    try:
        client = docker.from_env()
        container = client.containers.get(container_id)
        return container.logs()
    except Exception as error:
        logger.error('docker_image get_container_logs', error=error)
        return error


@router.post("/container/run", response_model=Any)
def run_container(
        image_name: str, args: List[str]
) -> Any:
    try:
        client = docker.from_env()
        container = client.containers.run(image_name, detach=True)
        return container.id
    except Exception as error:
        logger.error('docker_image run_container', error=error)
        return error


@router.post("/container/stop", response_model=Any)
def stop_container(
        container_id: str, args: List[str]
) -> Any:
    try:
        client = docker.from_env()
        client.containers.run(container_id, args)
    except Exception as error:
        logger.error('docker_image stop_container', error=error)
        return error


@router.get("/image", response_model=List[ImageObject])
def get_image(

) -> Any:
    try:
        res = []
        client = docker.from_env()
        for image in client.images.list():
            res.append(ImageObject(image.id, image.short_id))
    except Exception as error:
        logger.error('docker_image stop_container', error=error)
        return error
