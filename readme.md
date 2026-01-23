
# 小说抓取

```
# mac 安装 chromedriver
# https://formulae.brew.sh/cask/chromedriver
brew install --cask chromedriver
```

```
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt 
```

```
browser = await playwright.chromium.launch(headless=False, executable_path="/Users/linzhiji/Library/Caches/ms-playwright/chromium-1155/chrome-mac/Chromium.app/Contents/MacOS/Chromium")

browser = await playwright.webkit.launch(headless=False, executable_path="/Users/linzhiji/Library/Caches/ms-playwright/webkit-2123/pw_run.sh")
```