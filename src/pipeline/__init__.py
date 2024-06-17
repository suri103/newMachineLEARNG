from src.constants import *
from src.config.configuration import *
import os, sys
from dataclasses import dataclass
from src.logger import logging
from src.exception import CustomException
from src.components.data_transformation import DataTransformation, DataTransformationConfig
from src.components.model_trainer import ModelTrainer

class Train:
    def __init__(self):
        self.c=0
        print(f'{self.c}*********************')