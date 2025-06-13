# 📡 Stereo DSM Generation Pipelines for SPOT and Pleiades

## Overview
This repository provides a streamlined way to generate a Digital Surface Model (DSM) from SPOT 6 and Pleiades stereo imagery using NASA's Ames Stereo Pipeline.

## 🐍 Setup 
Refer to Section 2.6 for ASP installation using Conda and for general guidelines of installation https://stereopipeline.readthedocs.io/en/latest/installation.html#conda-intro

or use the .yml file for recreating the environment. 
```bash
conda env create -f asp_environment.yml
```

Ensure `stereo`, `point2dem`, and other ASP tools are available in your system PATH.

## Usage
1. Place all stereo images in `data` 📂
    - SPOT raw files should be in `data/tif`
    - Pleiades raw files should be in `data/jp2` (Plieades data has JP2 images that needs to be converted into tif)
2. Define input and output path, variables in config.json file. A sample file for both the sensors is provided (config_spot.json,config_plieades.json)
3. The data directory structure is captured in data_directory_structure.json file
4. Run the pipeline:
```bash
python run_pipeline.py config.json 
```

Outputs will be saved in `results/`.

##  💾 Data
Data can be accessed at https://drive.google.com/drive/folders/1Ez28ofTNtGOb15zQEIN2xMGfpFva3_nC?usp=sharing (access restricted to Solafune)
