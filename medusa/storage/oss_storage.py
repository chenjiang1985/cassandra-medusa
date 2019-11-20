# -*- coding: utf-8 -*-
# Copyright 2019 Spotify AB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import configparser
import logging
import os
import io
from dateutil import parser

from libcloud.storage.providers import get_driver

from medusa.storage.abstract_storage import AbstractStorage


class OSSStorage(AbstractStorage):
    """
    Available storage providers for oss:
    ALIYUN_OSS = 'aliyun_oss'
    """
    def connect_storage(self):
        oss_config = configparser.ConfigParser(interpolation=None)
        with io.open(os.path.expanduser(self.config.key_file), 'r', encoding='utf-8') as oss_file:
            oss_config.read_file(oss_file)
            oss_profile = self.config.api_profile
            profile = oss_config[oss_profile]
            cls = get_driver(self.config.storage_provider)
            driver = cls(profile['accessKeyID'], profile['accessKeySecret'])
            #driver.get_container
            return driver

    def download_blobs(self, src, dest):
        """
        Downloads a list of files from the remote storage system to the local storage

        :param src: a list of files to download from the remote storage system
        :param dest: the path where to download the objects locally
        :return:
        """
        for src_obj in list(src):
            blob = self.get_blob(src_obj)
            index = src_obj.rfind('/')
            if index > 0:
                file_name = src_obj[src_obj.rfind('/') + 1:]
            else:
                file_name = src_obj
            blob.download(os.path.join(dest, file_name), overwrite_existing=True)

    def get_object_datetime(self, blob):
        logging.debug("Blob {} last modification time is {}".format(blob.name, blob.extra["last_modified"]))
        return parser.parse(blob.extra["last_modified"])

    def get_cache_path(self, path):
        # Full path for files that will be taken from previous backups
        return path
