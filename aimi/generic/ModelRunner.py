"""
    -------------------------------------------------
    AIMI Generic - 
    -------------------------------------------------
    
    -------------------------------------------------
    Author: Leonard Nürnberg
    Email:  leonard.nuernberg@maastrichtuniversity.nl
    -------------------------------------------------
    
"""

from typing import List
import os, subprocess
from Config import Module, Instance, InstanceData, DataType, FileType, Meta, SEG


class ModelRunner(Module):

    # TODO: since the ModelRunner is always customized, we could consider adding an additional layer of support here. E.g. we could define the required data formats and then already pre-filter instances accordingly. Extending this further, we could even add pre-checks etc. However, it might be equally valid or even better for transparency to have all pre-checks and filtering steps present in the run.py script.
    
    # TODO: standardize "model" meta type and auto-set to all exported instance data

    def task(self) -> None:
        for instance in self.config.data.instances:
            self.runModel(instance)

    def runModel(self, instance: Instance) -> None:
        pass

class TotalSegmentatorRunner(ModelRunner):
    def runModel(self, instance: Instance) -> None:
        
        # model config
        # TODO: we should implement sth. like .getConfiguration(key) on the base module.
        #       but keep it simple for now, one change at a time 
        c = self.config[self.__class__]

        # data
        inp_data = instance.getData(DataType(FileType.NIFTI))

        # define model output folder
        out_dir = self.config.data.requestTempDir()
        
        # create out dir if required
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir)

        # build command
        bash_command  = ["TotalSegmentator"]
        bash_command += ["-i", inp_data.abspath]
        bash_command += ["-o", out_dir]

        # 
        if c["use_fast_mode"]:
            self.v("Running TotalSegmentator in fast mode ('--fast', 3mm): ")
            bash_command += ["--fast"]
        else:
            self.v("Running TotalSegmentator in default mode (1.5mm)")

        print(">> run ts: ", bash_command)

        # run the model
        bash_return = subprocess.run(bash_command, check=True, text=True)

        # add output data
        for out_file in os.listdir(out_dir):

            # ignore non nifti files
            if out_file[-7:] != ".nii.gz":
                print(f"IGNORE OUTPUT FILE {out_file}")
                continue

            # meta
            meta = {
                "model": "TotalSegmentator",
                "roi": out_file[:-7]            # TODO: standardize (as with the whole DataType usecase & filtering!)
            }

            # create output data
            seg_data_type = DataType(FileType.NIFTI, SEG + meta)           
            seg_path = os.path.join(out_dir, out_file)
            seg_data = InstanceData(seg_path, type=seg_data_type)
            seg_data.base = "" # required since path is external (will be fixed soon)
            instance.addData(seg_data)  