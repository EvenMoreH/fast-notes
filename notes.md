# Port:
5001

# Docker image build command:
docker build -t image-name-img .

# Docker image run command:
docker run -p 5001:5001 image-name-img
<!-- To run without a console use -d argument -->
docker run -d -p 5001:5001 image-name-img
hub
# Project Tree
📦fastHTML_Template
 ┣ 📂app
 ┃ ┣ 📂static
 ┃ ┃ ┗ 📂css
 ┃ ┃ ┃ ┣ 📜input.css
 ┃ ┃ ┃ ┗ 📜tailwind.css
 ┃ ┗ 📜main.py
 ┣ 📜.gitignore
 ┣ 📜Dockerfile
 ┣ 📜LICENSE
 ┣ 📜notes.md
 ┣ 📜README.md
 ┣ 📜requirements.txt
 ┗ 📜tailwind.config.js

# Tailwind
<!-- initialize tailwind config for given project -->
C:\Compilers\Tailwind\tailwindcss-windows-x64.exe init

<!-- build tailwind.css output from specified input.css with --watch flag for rebuilding -->
C:\Compilers\Tailwind\tailwindcss-windows-x64.exe -i app/static/css/input.css -o app/static/css/tailwind.css --watch

<!-- build tailwind.css output from specified input.css with --minify flag to conserve space for docker -->
C:\Compilers\Tailwind\tailwindcss-windows-x64.exe -i app/static/css/input.css -o app/static/css/tailwind.css --minify