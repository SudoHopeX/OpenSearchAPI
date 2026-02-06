from flask import Flask, request, jsonify
from engines import search

app = Flask(__name__)

ENGINES = ["google", "duckduckgo", "bing"] #, "brave"]

@app.route("/search")
def handle_search():
    query = request.args.get("q")
    engine = request.args.get("engine", "google").lower()

    if not query:
        return jsonify({"error": "Missing query parameter 'q'"}), 400

    if engine not in ENGINES:
        return jsonify({"error": f"Engine must be one of {ENGINES}"}), 400

    results = search(query, engine)
    return jsonify({
        "query": query,
        "engine": engine,
        "results": results
    })


@app.route("/mega/search")
def handle_mega_search():
    query = request.args.get("q")
    engines_param = request.args.get("engine", "google").lower()

    if not query:
        return jsonify({"error": "Missing query parameter 'q'"}), 400

    requested_engines = [e.strip() for e in engines_param.split(",")]

    invalid_engines = [e for e in requested_engines if e not in ENGINES]
    if invalid_engines:
        return jsonify({"error": f"Invalid engines: {invalid_engines}. Must be one of {ENGINES}"}), 400

    all_results = {}
    for engine in requested_engines:
        results = search(query, engine)
        all_results[engine] = results

    return jsonify({
        "query": query,
        "engines": requested_engines,
        "results": all_results
    })

@app.route("/")
def index():
    html_res = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>OpenSearchAPI API | Docs</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono&display=swap" rel="stylesheet">
  <style>
    :root {
      /* Light Glass Theme */
      --bg-gradient: radial-gradient(at 0% 0%, hsla(253,16%,7%,1) 0, transparent 50%), 
                      radial-gradient(at 50% 0%, hsla(225,39%,30%,1) 0, transparent 50%), 
                      radial-gradient(at 100% 0%, hsla(339,49%,30%,1) 0, transparent 50%);
      --glass-bg: rgba(255, 255, 255, 0.7);
      --glass-border: rgba(255, 255, 255, 0.4);
      --text-main: #1e293b;
      --text-dim: #475569;
      --accent: #6366f1;
      --code-bg: rgba(0, 0, 0, 0.05);
    }

    [data-theme="dark"] {
      --bg-gradient: radial-gradient(at 0% 0%, #0f172a 0, transparent 50%), 
                      radial-gradient(at 50% 0%, #1e1b4b 0, transparent 50%), 
                      radial-gradient(at 100% 0%, #312e81 0, transparent 50%);
      --glass-bg: rgba(15, 23, 42, 0.6);
      --glass-border: rgba(255, 255, 255, 0.1);
      --text-main: #f1f5f9;
      --text-dim: #94a3b8;
      --accent: #818cf8;
      --code-bg: rgba(0, 0, 0, 0.3);
    }

    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: 'Inter', sans-serif;
    }

    body {
      background-color: #0f172a; /* Fallback */
      background-image: var(--bg-gradient);
      background-attachment: fixed;
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      justify-content: center;
      transition: background 0.5s ease;
    }

    /* Layout Structure */
    .app-container {
      display: flex;
      width: 100%;
      max-width: 1200px;
      margin: 40px 20px;
      gap: 30px;
    }

    /* Glass Sidebar */
    .sidebar {
      width: 280px;
      height: fit-content;
      position: sticky;
      top: 40px;
      background: var(--glass-bg);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border: 1px solid var(--glass-border);
      border-radius: 24px;
      padding: 30px 20px;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    .logo {
      font-weight: 700;
      font-size: 1.4rem;
      letter-spacing: -0.5px;
      margin-bottom: 30px;
      padding-left: 10px;
      background: linear-gradient(to right, var(--accent), #f472b6);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .nav-btn {
      all: unset;
      padding: 12px 16px;
      border-radius: 12px;
      cursor: pointer;
      color: var(--text-dim);
      font-weight: 500;
      transition: 0.3s;
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .nav-btn:hover {
      background: rgba(255,255,255,0.1);
      color: var(--text-main);
    }

    .nav-btn.active {
      background: var(--accent);
      color: white;
      box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.3);
    }

    .github-link {
      margin-top: 20px;
      border-top: 1px solid var(--glass-border);
      padding-top: 20px;
      text-decoration: none;
    }

    /* Main Content Area */
    .main-content {
      flex: 1;
      background: var(--glass-bg);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border: 1px solid var(--glass-border);
      border-radius: 24px;
      padding: 50px;
      min-height: 600px;
      position: relative;
    }

    .tab-content {
      display: none;
      animation: fadeIn 0.4s ease-out;
    }

    .tab-content.active {
      display: block;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* Typography */
    h1 { font-size: 2.5rem; margin-bottom: 1rem; font-weight: 800; }
    h2 { font-size: 1.5rem; margin: 2rem 0 1rem; color: var(--accent); }
    p { color: var(--text-dim); line-height: 1.6; margin-bottom: 1.5rem; }

    /* Glass Code Blocks */
    .code-wrapper {
      background: var(--code-bg);
      border: 1px solid var(--glass-border);
      border-radius: 16px;
      padding: 20px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.9rem;
      margin: 15px 0;
      position: relative;
      cursor: pointer;
      overflow-x: auto;
      transition: transform 0.2s;
    }

    .code-wrapper:hover {
      transform: scale(1.01);
    }

    .code-wrapper::after {
      content: "Click to copy";
      position: absolute;
      right: 15px;
      top: 15px;
      font-size: 0.7rem;
      text-transform: uppercase;
      opacity: 0.4;
    }

    /* Engine Pills */
    .engine-grid {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
    }

    .engine-pill {
      padding: 8px 20px;
      background: var(--glass-border);
      border-radius: 100px;
      font-size: 0.9rem;
      font-weight: 500;
      border: 1px solid transparent;
      transition: 0.3s;
    }

    .engine-pill:hover {
      border-color: var(--accent);
      color: var(--accent);
    }

    /* Transparent & Minimalist Toggle */
    .theme-toggle {
      position: absolute;
      top: 30px;
      right: 30px;
      background: transparent; /* Removed background */
      border: none;             /* Removed border */
      cursor: pointer;
      color: var(--text-main);
      padding: 5px;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.2s;
      opacity: 0.7;
    }
    
    .theme-toggle:hover {
      opacity: 1;
      transform: rotate(15deg) scale(1.1);
    }
    
    .theme-toggle svg {
      transition: stroke 0.3s ease;
    }

    /* Mobile */
    @media (max-width: 850px) {
      .app-container { flex-direction: column; }
      .sidebar { width: 100%; position: static; }
      .main-content { padding: 30px 20px; }
    }
  </style>
</head>
<body data-theme="dark">

  <div class="app-container">
    <aside class="sidebar">
      <div class="logo">OpenSearchAPI</div>
      <button class="nav-btn active" onclick="showTab('home')">Home</button>
      <button class="nav-btn" onclick="showTab('installation')">Installation</button>
      <button class="nav-btn" onclick="showTab('requirements')">Requirements</button>
      <button class="nav-btn" onclick="showTab('endpoints')">Endpoints</button>
      <button class="nav-btn" onclick="showTab('usage')">Usage Examples</button>
      
      <a href="https://github.com/SudoHopeX/OpenSearchAPI" target="_blank" class="nav-btn github-link">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
        GitHub Repo
      </a>
    </aside>

    <main class="main-content">
      <button class="theme-toggle" onclick="toggleTheme()" id="themeBtn" aria-label="Toggle Theme">
          <svg id="themeIcon" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="5"></circle>
            <line x1="12" y1="1" x2="12" y2="3"></line>
            <line x1="12" y1="21" x2="12" y2="23"></line>
            <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
            <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
            <line x1="1" y1="12" x2="3" y2="12"></line>
            <line x1="21" y1="12" x2="23" y2="12"></line>
            <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
            <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
          </svg>
      </button>
      
      <section id="home" class="tab-content active">
      <div style="text-align: center; margin-bottom: 50px;">
        <h1 style="font-size: 3.5rem; margin-bottom: 10px;">OpenSearchAPI</h1>
        <p style="font-size: 1.2rem; max-width: 600px; margin: 0 auto;">
          A high-performance, open-source gateway to global search results. <br>
          No restrictions, just pure data.
        </p>
      </div>

      <div class="feature-grid">
        <div class="feature-card">
          <div class="feature-icon">💎</div>
          <h4>100% Free</h4>
          <p>Completely open-source and free to use for any project except Commercial Usages.</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">🔑</div>
          <h4>No API Keys</h4>
          <p>Zero registration. Start querying immediately without headers.</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">☁️</div>
          <h4>Lightweight</h4>
          <p>Small footprint, designed to run on minimal server resources.</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">⚡</div>
          <h4>Fast Scraping</h4>
          <p>Optimized with headless drivers for rapid data retrieval.</p>
        </div>
      </div>
    
      <div class="dev-card">
        <div style="display: flex; align-items: center; gap: 20px;">
          <div class="dev-avatar">S</div>
          <div>
            <h3 style="margin: 0; font-size: 1.2rem;">Developed by SudoHopeX</h3>
            <p style="margin: 0; font-size: 0.9rem; opacity: 0.8;">Cyber Security (Ethical Hacking) & Open Source Dev Enthusiast</p>
          </div>
        </div>
        <p style="margin-top: 15px; font-size: 0.9rem; line-height: 1.5;">
          OpenSearchAPI was built to provide developers with an easy, unrestricted way to aggregate search data without the hurdles of expensive subscriptions or rate-limited API keys.
        </p>
      </div>
    </section>
      
      <section id="installation" class="tab-content">
        <h1>Installation</h1>
        <p>Set up the OpenSearchAPI API in seconds using the command line.</p>
        
        <h2>Clone & Setup</h2>
        <div class="code-wrapper" onclick="copyCode(this)">git clone https://github.com/SudoHopeX/OpenSearchAPI.git</div>
        <div class="code-wrapper" onclick="copyCode(this)">bash setup.sh</div>
        
        <h2>Direct Download</h2>
        <div class="code-wrapper" onclick="copyCode(this)">curl -fsL https://api.example.com/setup</div>
      </section>

      <section id="requirements" class="tab-content">
  <h1>Requirements</h1>
  <p>Ensure your environment meets these specifications for optimal performance.</p>
  
  <br><br>
  <h3 style="font-size: 1.1rem; margin-bottom: 15px; color: var(--text-main); opacity: 0.9;">1. System Packages</h3>
  <div class="engine-grid" style="margin-bottom: 30px;">
    <div class="engine-pill">Python 3.13+</div>
    <div class="engine-pill">xvfb</div>
    <div class="engine-pill">Chrome / Chromium Browser</div>
  </div>

  <br><br>
  <h3 style="font-size: 1.1rem; margin-bottom: 15px; color: var(--text-main); opacity: 0.9;">2. Pip Packages</h3>
  <div class="engine-grid">
    <div class="engine-pill">requests</div>
    <div class="engine-pill">flask</div>
    <div class="engine-pill">beautifulsoup4</div>
    <div class="engine-pill">curl_cffi</div>
    <div class="engine-pill">nodriver</div>
    <div class="engine-pill">ddgs</div>
    <div class="engine-pill">pyvirtualdisplay</div>
  </div>
</section>

      <section id="endpoints" class="tab-content">
        <h1>Endpoints</h1>
        <p>Access various search engines through a unified interface.</p>
        
        <h2>Documentation</h2>
        <div class="code-wrapper" onclick="copyCode(this)">GET /</div>
        
        <h2>Standard Search</h2>
        <div class="code-wrapper" onclick="copyCode(this)">GET /search?q=query&engine=duckduckgo</div>
        
        <h2>Multi-Engine (Mega)</h2>
        <div class="code-wrapper" onclick="copyCode(this)">GET /mega/search?q=query&engines=google,bing</div>
        
        <br><br>
        <h1>Supported Engines</h1>
        <div class="engine-grid">
          <div class="engine-pill">Google</div>
          <div class="engine-pill">DuckDuckGo</div>
          <div class="engine-pill">Bing</div>
        </div>
      </section>

      <section id="usage" class="tab-content">
        <h1>Usage Examples</h1>
        <p>Integrate the API into your project using these common snippets.</p>
        
        <h2>Curl</h2>
        <div class="code-wrapper" onclick="copyCode(this)">
curl https://localhost:5000/search?q=SudoHopeX&engine=duckduckgo
        </div>
        <div class="code-wrapper" onclick="copyCode(this)">
curl https://localhost:5000/mega/search?q=SudoHopeX&engines=duckduckgo,google,bing
        </div>
        
        <h2>Python Requests</h2>
        <div class="code-wrapper" onclick="copyCode(this)">
import requests<br><br>
query = "Photography"<br>
engine = "google"<br>
url = f"http://localhost:5000/search&q={query}&engine={engine}"<br>
data = requests.get(url).json()<br>
print(data)
        </div>
      </section>
    </main>
  </div>

  <script>
    function showTab(tabId) {
      // Update buttons
      document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
      event.currentTarget.classList.add('active');

      // Update content
      document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
      document.getElementById(tabId).classList.add('active');
    }

    function toggleTheme() {
        const body = document.body;
        const current = body.getAttribute('data-theme');
        const next = current === 'dark' ? 'light' : 'dark';
        body.setAttribute('data-theme', next);
        
        const iconPath = document.getElementById('themeIcon');
        
        // Smoothly swap the SVG inner content
        if (next === 'dark') {
          iconPath.innerHTML = `
            <circle cx="12" cy="12" r="5"></circle>
            <line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line>
            <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
            <line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line>
            <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>`;
        } else {
          iconPath.innerHTML = `<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>`;
        }
    }

    async function copyCode(el) {
      const text = el.innerText.replace("Click to copy", "");
      await navigator.clipboard.writeText(text);
      const originalText = el.innerText;
      el.innerText = "Copied to clipboard!";
      setTimeout(() => { el.innerText = originalText; }, 1500);
    }
  </script>
</body>
</html>
    """
    return html_res



if __name__ == "__main__":
    app.run(port=5000, debug=True, threaded=True)