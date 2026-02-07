# OpenSearchAPI
###### Lightweight Free OpenSource Search API

A minimal Python API to get search results from Google, Bing & DuckDuckGo — **no API keys, free, lightweight**.


## Install via Curl
```bash
curl -fsL https://raw.githubusercontent.com/SudoHopeX/OpenSearchAPI/refs/heads/main/setup.sh | sudo bash
```

## Clone the Repo & install
```bash
git clone https://github.com/SudoHopeX/OpenSearchAPI.git && cd OpenSearchAPI
sudo bash setup.sh
```

## start the app
```bash
opensearchapi        # Runs in foreground
opensearchapi --bg   # Runs in background   
```

## 🌐 API Endpoints

### Read Detailed Documentation
```
http://127.0.0.1:5000/
```

### Single engine search
```
http://127.0.0.1:5000/search?q=python&engine=duckduckgo
```

### Multiple engine search
```
http://127.0.0.1:5000/mega/search?engines=duckduckgo,bing&q=sudohopex
```

## ✅ Engines Supported
- `google`
- `duckduckgo`
- `bing`

##  
<div align="center">
  <a href="https://hope.is-a.dev">
    <img src="https://hope.is-a.dev/img/made-with-love-by-sudohopex.png" style="width:300px;height:auto;" alt="Made with L0V3 by SudoHopeX">
  </a>
</div>   
