import os
import requests
import zipfile
import shutil
import tempfile

def main():
    url = 'https://p.yusukekamiyamane.com/icon/downloads/fugue-icons-3.5.6.zip'
    zip_filename = 'fugue-icons-3.5.6.zip'
    project_root = os.path.abspath(os.getcwd())

    # Download the zip file
    print('Downloading icons...')
    response = requests.get(url)
    with open(zip_filename, 'wb') as f:
        f.write(response.content)

    # Create a temporary directory to extract the zip file
    with tempfile.TemporaryDirectory() as tmpdirname:
        print('Extracting zip file...')
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall(tmpdirname)

        # The icons folder is inside 'fugue-icons-3.5.6' directory
        extracted_folder = os.path.join(tmpdirname, 'fugue-icons-3.5.6')
        icons_folder = os.path.join(extracted_folder, 'icons')

        # Copy the icons folder to the project root directory
        print('Copying icons folder to project root...')
        destination = os.path.join(project_root, 'icons')
        if os.path.exists(destination):
            shutil.rmtree(destination)
        shutil.copytree(icons_folder, destination)

    # Clean up the zip file
    os.remove(zip_filename)
    print('Icons have been successfully set up in your project root directory.')

if __name__ == '__main__':
    main()
