"""
    -------------------------------------------------
    AIMI beta - run the PP pipeline locally
    -------------------------------------------------
    
    -------------------------------------------------
    Author: Leonard Nürnberg
    Email:  leonard.nuernberg@maastrichtuniversity.nl
    -------------------------------------------------
"""

import sys, os
sys.path.append('.')

from aimi.generic.Config import Config, DataType, FileType, CT, SEG
from aimi.generic.modules.importer.DataSorter import DataSorter
from aimi.generic.modules.convert.NiftiConverter import NiftiConverter
from aimi.generic.modules.convert.DsegConverter import DsegConverter
from aimi.generic.modules.organizer.DataOrganizer import DataOrganizer
from aimi.platipy.utils.PlatipyRunner import PlatipyRunner

# clean-up
import shutil
shutil.rmtree("/app/data/sorted", ignore_errors=True)
shutil.rmtree("/app/data/nifti", ignore_errors=True)
shutil.rmtree("/app/tmp", ignore_errors=True)
shutil.rmtree("/app/data/output_data", ignore_errors=True)

# config
config = Config('/app/aimi/platipy/config/config.yml')
config.verbose = True  # TODO: define levels of verbosity and integrate consistently. 

# sort
DataSorter(config).execute()

# convert (ct:dicom -> ct:nifti)
NiftiConverter(config).execute()

# execute model (ct:nifti -> seg:nifti)
PlatipyRunner(config).execute()

# convert (seg:nifti -> seg:dicomseg)
DsegConverter(config).execute()

# organize data into output folder
organizer = DataOrganizer(config)
organizer.setTarget(DataType(FileType.NIFTI, CT), "/app/data/output_data/[i:SeriesID]/[path]")
organizer.setTarget(DataType(FileType.DICOMSEG, SEG), "/app/data/output_data/[i:SeriesID]/Platipy.seg.dcm")
organizer.execute()