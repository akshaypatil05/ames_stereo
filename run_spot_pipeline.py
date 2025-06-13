import os
import sys
import json
import argparse
from src.stereo import *
from src.postprocess import *

def load_config(config_path):
    """Load configuration from JSON file"""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"Error: Config file '{config_path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in config file: {e}")
        sys.exit(1)

def validate_paths(config):
    """Validate that input files exist"""
    required_files = ['left_img', 'right_img', 'left_rpc', 'right_rpc', 'dem_ref']
    
    for file_key in required_files:
        if file_key in config and not os.path.exists(config[file_key]):
            print(f"Warning: {file_key} file not found: {config[file_key]}")
    
    # Create output directories if they don't exist
    output_dirs = [
        os.path.dirname(config.get('stereo_prefix', '')),
        os.path.dirname(config.get('front_map_proj', '')),
        os.path.dirname(config.get('back_map_proj', ''))
    ]
    
    for dir_path in output_dirs:
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
            print(f"Created directory: {dir_path}")

def print_config(config):
    """Print configuration summary"""
    print("\n" + "="*50)
    print("STEREO PIPELINE CONFIGURATION")
    print("="*50)
    print(f"Left Image: {config['left_img']}")
    print(f"Right Image: {config['right_img']}")
    print(f"Left RPC: {config['left_rpc']}")
    print(f"Right RPC: {config['right_rpc']}")
    print(f"DEM Reference: {config['dem_ref']}")
    print(f"Stereo Output Prefix: {config['stereo_prefix']}")
    print(f"Front Map Projection: {config['front_map_proj']}")
    print(f"Back Map Projection: {config['back_map_proj']}")
    print(f"MPP (Meters Per Pixel): {config['mpp']}")
    print("="*50 + "\n")

def main():
    """Main function to run the stereo pipeline"""
    parser = argparse.ArgumentParser(description='Run stereo pipeline with configuration file')
    parser.add_argument('config', help='Path to configuration JSON file')
    parser.add_argument('--validate-only', action='store_true', 
                       help='Only validate configuration without running pipeline')
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Validate paths
    validate_paths(config)
    
    # Print configuration
    print_config(config)
    
    if args.validate_only:
        print("Configuration validation complete.")
        return
    
    try:
        print("Starting stereo pipeline...")
        
        # Step 1: Map projection
        print("\n1. Running map projection...")
        map_project(
            config['mpp'], 
            config['dem_ref'], 
            config['left_img'], 
            config['left_rpc'], 
            config['right_img'], 
            config['right_rpc'], 
            config['front_map_proj'], 
            config['back_map_proj']
        )
        print("Map projection completed.")
        
        # Step 2: Stereo processing
        print("\n2. Running stereo processing...")
        stereo_process(
            config['front_map_proj'], 
            config['back_map_proj'], 
            config['left_rpc'], 
            config['right_rpc'], 
            config['stereo_prefix'], 
            config['dem_ref']
        )
        print("Stereo processing completed.")
        
        # Step 3: Point cloud to DEM
        print("\n3. Converting point cloud to DEM...")
        point2dem_process(config['stereo_prefix'])
        print("Point2DEM processing completed.")
        
        # Step 4: Generate hillshade
        print("\n4. Generating hillshade...")
        generate_hillshade(config['stereo_prefix'])
        print("Hillshade generation completed.")
        
        print("\n" + "="*50)
        print("STEREO PIPELINE COMPLETED SUCCESSFULLY!")
        print("="*50)
        
    except Exception as e:
        print(f"\nError during pipeline execution: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()