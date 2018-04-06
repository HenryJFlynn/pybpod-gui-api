# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging, os, hashlib
import pybpodgui_api

from pybpodgui_api.models.experiment.experiment_base import ExperimentBase

from sca.formats import json

logger = logging.getLogger(__name__)


class ExperimentIO(ExperimentBase):
    """
    Save and Load actions for Experiment
    """
    def __init__(self, project):
        super(ExperimentIO, self).__init__(project)

        # repository that will manage the project files
        self.repository = None

    ##########################################################################
    ####### FUNCTIONS ########################################################
    ##########################################################################

    def collect_data(self, data):
        data.update({'name': self.name})
        #data.update({'task': self.task.name if self.task else None})
        data.update({'setups': []})

        for setup in self.setups:
            data['setups'].append(setup.collect_data({}))

        return data

    def save(self, parent_repository):
        """
        Save experiment data on filesystem.

        :ivar dict parent_path: Project path.  
        :return: Dictionary containing the experiment info to save.  
        :rtype: dict
        """
        # if the project was loaded then it will reuse the repository otherwise create a new repository ################################
        repository = self.repository = self.repository if self.repository else parent_repository.sub_repository('experiments', self.name, uuid4=self.uuid4)
        ################################################################################################################################

        # save setups
        for setup in self.setups: setup.save(repository)
        
        repository.uuid4    = self.uuid4
        repository.software = 'PyBpod GUI API v'+str(pybpodgui_api.__version__)
        repository.def_url  = 'http://pybpod.readthedocs.org'
        repository.def_text = 'This file contains information about a PyBpod gui experiment.'
        repository.name     = self.name
        
        repository.commit()

        return repository


    def load(self, repository):
        """
        Load experiment data from filesystem

        :ivar str experiment_path: Path of the experiment
        :ivar dict data: data object that contains all experiment info
        :return: Dictionary with loaded experiment info.
        """       
        self.repository = repository
        
        self.uuid4= repository.uuid4 if repository.uuid4 else self.uuid4
        self.name = repository.name
        
        setups_repos = repository.find('setups')
        if setups_repos is not None:
            for repo in setups_repos.list():
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