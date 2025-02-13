# Pre-Requisites
## Software 
- python3.10
- pip
- git
- java

### Windows
error: Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/

- Note: This isn't supported on ARM

### MAC
- Manually Install XCode Developer from App Store
```bash
sudo xcode-select -s /Applications/Xcode.app/Contents/Developer
```

### Third Party Packages
```bash
sudo apt install build-essentials
pip install flask openai spacy transformers
python -m spacy download en_core_web_sm
```

## Manual Set Up
- Creation of a Git Repository
   ```bash 
   git remote add origin https://github.com/{repo_owner}/{rep_name}.git
   ```
- Set Permissions for GITHUB_TOKEN


