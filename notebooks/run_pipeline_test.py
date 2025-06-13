import os
from IPython.display import Markdown
from src.stereo import *
from src.postprocess import *

# Set paths for input images and RPCs
left_img = "data/tif/front/IMG_SPOT6_P_201906210832287_SEN_7416126101_R1C1.TIF"
right_img = "data/tif/back/IMG_SPOT6_P_201906210833144_SEN_7416126101_R1C1.TIF"

left_rpc = "data/tif/front/RPC_SPOT6_P_201906210832287_SEN_7416126101.XML"
right_rpc = "data/tif/back/RPC_SPOT6_P_201906210833144_SEN_7416126101.XML"


dem_ref = "data/tif/dem.tif"
stereo_prefix = "results/out"


front_map_proj="results/front_map_proj.tif"
back_map_proj="results/back_map_proj.tif"

mpp=1.5

Markdown(f"""
### Input Configuration:
- Left Image: `{left_img}`
- Right Image: `{right_img}`
- Left RPC: `{left_rpc}`
- Right RPC: `{right_rpc}`
- DEM Reference: `{dem_ref}`
- Stereo Output Prefix: `{stereo_prefix}`
- Front Map Projection Output: `{front_map_proj}`
- Back Map Projection Output: `{back_map_proj}`
- MPP: `{mpp}`
""")

map_project(mpp, dem_ref, left_img, left_rpc, right_img, right_rpc, front_map_proj, back_map_proj)
stereo_process(front_map_proj, back_map_proj, left_rpc, right_rpc, stereo_prefix, dem_ref)
point2dem_process(stereo_prefix)
generate_hillshade(stereo_prefix)

