import os
import sys


documents_path = os.path.expanduser("~") + "/documents"
# Define the root path for the blocks folder
blocks_root_path = os.path.expanduser("~") + "/documents/aiaistreamlit/blocks"

sys.path.append(blocks_root_path)


# Define path for static file serving
static = "static"
static_root_path = f"app/{static}"

# Define paths for various resource types
path_audio_folder = os.path.join(static, "audio")
path_css_folder = os.path.join(static, "css")
path_csv_folder = os.path.join(static, "csv")
path_html_folder = os.path.join(static, "html")
path_images_folder =  f"{static_root_path}/images"
path_notebooks_folder = os.path.join(static, "ipynb")
path_javascript_folder = os.path.join(static, "js")
path_json_folder = os.path.join(static, "json")
path_markdowns_folder = os.path.join(static, "md")
path_python_folder = os.path.join(static, "py")
path_videos_folder = os.path.join(static, "videos")


