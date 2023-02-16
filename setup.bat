mkdir adb
mkdir tesseract
mkdir save
mkdir download
cd download
curl https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe --output python.exe
curl https://dl.google.com/android/repository/platform-tools_r29.0.5-windows.zip --output adb.zip
curl https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.2.0.20220712.exe --output tesseract.exe
curl https://objects.githubusercontent.com/github-production-release-asset-2e65be/23216272/feedcd26-ed37-474b-9c28-bbe47ae4fb35?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20221105%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20221105T062634Z&X-Amz-Expires=300&X-Amz-Signature=ce49cd65059ffd5c79edb4fde4560ea68bbe3e0da34d5d5abd495106278b6991&X-Amz-SignedHeaders=host&actor_id=0&key_id=0&repo_id=23216272&response-content-disposition=attachment%3B%20filename%3DGit-2.38.1-64-bit.exe&response-content-type=application%2Foctet-stream --output gitbash.exe