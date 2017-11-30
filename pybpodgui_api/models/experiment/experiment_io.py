# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging, os, hashlib
import pybpodgui_api
from pybpodgui_api.utils.send2trash_wrapper import send2trash
from pybpodgui_api.models.experiment.experiment_base import ExperimentBase

from sca.formats import json

logger = logging.getLogger(__name__)


class ExperimentIO(ExperimentBase):
    """
    Save and Load actions for Experiment
    """

    def __init__(self, project):
        super(ExperimentIO, self).__init__(project)

    ##########################################################################
    ####### FUNCTIONS ########################################################
    ##########################################################################

    def collect_data(self, data):
        data.update({'name': self.name})
        data.update({'task': self.task.name if self.task else None})
        data.update({'setups': []})

        for setup in self.setups:
            data['setups'].append(setup.collect_data({}))

        return data

    def save(self, repository):
        """
        Save experiment data on filesystem.

        :ivar dict parent_path: Project path.  
        :return: Dictionary containing the experiment info to save.  
        :rtype: dict
        """
        # save setups
        for setup in self.setups:
            setup.save(repository.sub_repository('setups', setup.name, uuid4=setup.uuid4))

        repository.uuid4    = self.uuid4
        repository.software = 'PyBpod GUI API v'+str(pybpodgui_api.__version__)
        repository.def_url  = 'http://pybpod.readthedocs.org'
        repository.def_text = 'This file contains information about a PyBpod gui experiment.'
        repository['name']  = self.name
        repository['task']  = self.task.name if self.task else None

        repository.add_parent_ref(self.project.uuid4)
        if self.task:
            repository.add_external_ref(self.task.uuid4)

        self.path = repository.save()
        return repository


    def load(self, repository):
        """
        Load experiment data from filesystem

        :ivar str experiment_path: Path of the experiment
        :ivar dict data: data object that contains all experiment info
        :return: Dictionary with loaded experiment info.
        """       
        self.uuid4= repository.uuid4 if repository.uuid4 else self.uuid4
        self.name = repository.get('name', None)
        self.task = repository.get('task', None)
        self.path = repository.path

        for repo in repository.find('setups').list():
            setup = self.create_setup()
            setup.load(repo)

        



    def __clean_setups_path(self, experiment_path):
        # remove from the setups directory the unused setup files
        setups_paths = [setup.path for setup in self.setups]
        for path in self.__list_all_setups_in_folder(experiment_path):
            if path not in setups_paths:
                logger.debug("Sending directory [{0}] to trash".format(path))
                send2trash(path)

    def __generate_experiments_path(self, project_path):
        return os.path.join(project_path, 'experiments')

    def __generate_experiment_path(self, experiments_path):
        return os.path.join(experiments_path, self.name)

    def __list_all_setups_in_folder(self, experiment_path):
        search_4_dirs_path = os.path.join(experiment_path, 'setups')
        if not os.path.exists(search_4_dirs_path):
            return []
        return sorted([os.path.join(search_4_dirs_path, d) for d in os.listdir(search_4_dirs_path) if
                       os.path.isdir(os.path.join(search_4_dirs_path, d))])
