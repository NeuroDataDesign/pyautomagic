import pytest
from pyautomagic.src import Block, Project, Subject, Config

name = 'Stupid project'
d_folder = r"C:\Users\saul__000\OneDrive\Escritorio\Johns Hopkins\NeuroData Design I\Project_Test_Folder"
ext = 'something.edf'


def test_data_folder():
    test_Project = Project.Project(name, d_folder, ext)
    assert(test_Project.data_folder == r"C:\Users\saul__000\OneDrive\Escritorio\Johns Hopkins\NeuroData Design I\Project_Test_Folder")


def test_results_folder():
    test_Project = Project.Project(name, d_folder, ext)
    assert(test_Project.results_folder == r"C:\Users\saul__000\OneDrive\Escritorio\Johns Hopkins\NeuroData Design I\Project_Test_Folder\derivatives\automagic")


def test_file_extension():
    test_Project = Project.Project(name, d_folder, ext)
    assert(test_Project.file_extension == ".edf")

