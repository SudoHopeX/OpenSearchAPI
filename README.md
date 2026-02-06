# OpenSearchAPI
###### Lightweight Free OpenSource Search API

A minimal Python API to get search results from Google, Bing & DuckDuckGo — **no API keys, free, lightweight**.


## Clone the Repo
```bash
git clone https://github.com/SudoHopeX/OpenSearchAPI.git
```

## 🛠️ Setup
```bash
bash setup.sh
```

## start the app
```bash
opensearchapi        # Runs in foreground
opensearchapi --bg   # Runs in background   
```

## 🌐 API Endpoints

### Single engine search
```
http://localhost:5000/search?q=python&engine=duckduckgo
```

### Multiple engine search
```
http://localhost:5000/mega/search?engines=duckduckgo,bing&q=sudohopex
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
