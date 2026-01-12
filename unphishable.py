import sys
import uuid
import os
from datetime import datetime

# ============================================
# ENHANCED AUTO-INSTALL WITH CONSOLE FALLBACKS
# ============================================

class ConsoleManager:
    """Handle console output with fallbacks"""
    def __init__(self):
        self.has_colorama = False
        self.has_rich = False
        self.setup_consoles()
    
    def setup_consoles(self):
        """Try to load console libraries, install if missing"""
        # Try colorama first
        try:
            from colorama import init, Fore, Style
            init(autoreset=True)
            self.Fore = Fore
            self.Style = Style
            self.has_colorama = True
            self.print_message("✅ Colorama loaded", "green")
        except ImportError:
            self.install_package("colorama")
            try:
                from colorama import init, Fore, Style
                init(autoreset=True)
                self.Fore = Fore
                self.Style = Style
                self.has_colorama = True
            except:
                self.Fore = type('obj', (object,), {'RED': '', 'GREEN': '', 'YELLOW': '', 'CYAN': '', 'WHITE': ''})
                self.Style = type('obj', (object,), {'RESET_ALL': ''})
        
        # Try rich for advanced features
        try:
            from rich.console import Console
            from rich.panel import Panel
            from rich.table import Table
            self.console = Console()
            self.Panel = Panel
            self.Table = Table
            self.has_rich = True
            self.print_message("✅ Rich console loaded", "green")
        except ImportError:
            # Don't auto-install rich (optional)
            self.console = None
            self.Panel = None
            self.Table = None
    
    def install_package(self, package):
        """Install a Python package"""
        self.print_message(f"📦 Installing {package}...", "yellow")
        try:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"])
            self.print_message(f"✅ Installed: {package}", "green")
            return True
        except:
            self.print_message(f"❌ Failed to install: {package}", "red")
            return False
    
    def print_message(self, text, color="white"):
        """Print message with color if available"""
        if self.has_colorama:
            colors = {
                "red": self.Fore.RED,
                "green": self.Fore.GREEN,
                "yellow": self.Fore.YELLOW,
                "cyan": self.Fore.CYAN,
                "white": self.Fore.WHITE
            }
            print(f"{colors.get(color, self.Fore.WHITE)}{text}{self.Style.RESET_ALL}")
        else:
            print(text)
    
    def display_banner(self):
        """Display enhanced banner"""
        if self.has_rich and self.console:
            from rich.text import Text
            banner_text = Text("🔐 PHISHING DOMAIN SCANNER 🔍", style="bold cyan")
            subtitle = Text("Professional Security Analysis Tool", style="dim")
            
            self.console.print("\n")
            self.console.rule("[bold cyan]Security Scanner[/bold cyan]")
            self.console.print(banner_text, justify="center")
            self.console.print(subtitle, justify="center")
            self.console.print("[dim]Enter URL to scan or 'exit' to quit[/dim]\n")
        else:
            # Fallback banner
            print("\n" + "="*60)
            print("    🔐 PHISHING DOMAIN SCANNER 🔍")
            print("       Professional Security Tool")
            print("="*60 + "\n")
            print("Enter URL to scan or 'exit' to quit\n")
    
    def display_explanation(self, risk_score, factors):
        """Display risk explanation after verdict"""
        if self.has_rich and self.console:
            from rich.panel import Panel
            from rich.text import Text
            
            # Create explanation text
            explanation_lines = []
            
            # Score context
            if risk_score < 10:
                explanation_lines.append("📈 Minimal risk indicators detected.")
            elif risk_score < 20:
                explanation_lines.append("📈 Some low-risk factors present.")
            elif risk_score < 30:
                explanation_lines.append("⚠️ Multiple suspicious factors detected.")
            else:
                explanation_lines.append("🚨 High concentration of risk factors.")
            
            # Factor explanations
            factor_explanations = {
                "redirect": "🔄 Redirects can hide final destination",
                "privacy": "🛡️ WHOIS privacy masks domain ownership",
                "free_ssl": "🔓 Free SSL common in phishing campaigns",
                "invalid_ssl": "❌ Missing SSL indicates poor security",
                "new_domain": "🆕 New domains are riskier (often <1 year)",
                "unreachable": "📡 Domain may be fake or taken down"
            }
            
            # Add relevant factor explanations
            for factor, explanation in factor_explanations.items():
                if factor in str(factors).lower():
                    explanation_lines.append(explanation)
            
            # Create panel
            explanation_text = "\n".join(explanation_lines)
            panel = Panel(
                explanation_text,
                title="📋 Risk Analysis",
                border_style="cyan",
                padding=(1, 2)
            )
            self.console.print(panel)
        else:
            # Fallback explanation
            print(f"\n{'─'*40}")
            print("📋 RISK ANALYSIS:")
            print(f"{'─'*40}")
            
            if risk_score < 10:
                print("• Minimal risk indicators detected.")
            elif risk_score < 20:
                print("• Some low-risk factors present.")
            elif risk_score < 30:
                print("• Multiple suspicious factors detected.")
            else:
                print("• High concentration of risk factors.")
            
            # Simple factor display
            if factors:
                print("\nKey Factors:")
                for factor in str(factors).split(','):
                    if factor.strip():
                        print(f"  • {factor.strip()}")

# Initialize console manager
console_mgr = ConsoleManager()

# ============================================
# AUTO-INSTALL CORE PACKAGES
# ============================================

def install_core_packages():
    """Install essential packages"""
    required_packages = ["requests", "python-whois"]
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            console_mgr.print_message(f"✅ {package} already installed", "green")
        except ImportError:
            console_mgr.install_package(package)
    
    # Try to import after installation
    global requests, ssl, socket, whois, urlparse
    try:
        import requests
        import ssl
        import socket
        import whois
        from urllib.parse import urlparse
        console_mgr.print_message("✅ All core packages loaded", "green")
        return True
    except ImportError as e:
        console_mgr.print_message(f"❌ Critical error: {e}", "red")
        return False

# Install and import core packages
if not install_core_packages():
    sys.exit(1)

# ============================================
# YOUR EXACT MODULES (UNCHANGED - COPIED VERBATIM)
# ============================================

def parse_domain(user_input):
    try:
        if not user_input or not user_input.strip():
            return False, "❌ No input provided"
        user_input = user_input.strip()
        parsed = urlparse(user_input)
        if parsed.scheme:
            domain = parsed.netloc
        else:
            parsed = urlparse("http://" + user_input)
            domain = parsed.netloc
        if not domain:
            return False, "❌ invalid url or domain"
        if "." not in domain:
            return False, "❌ invalid domain format"
        if domain.startswith('.') or domain.endswith('.'):
            return False, "❌ invalid url pattern"
        if '..' in domain:
            return False, "❌ wrong domain format"
        return True, domain.lower()
    except Exception as e:
        return False, f"❌ unexpected parsing error: {e}"

def http_status_check(domain, timeout=5):
    if not domain.startswith(("http://", "https://")):
        domain = "https://" + domain
    try:
        response = requests.get(domain, timeout=timeout, allow_redirects=False)
        status_code = response.status_code
        if 200 <= status_code < 300:
            return "reachable", status_code
        elif 300 <= status_code < 400:
            return "redirect", status_code
        else:
            return "unreachable", status_code
    except requests.exceptions.RequestException:
        return "unreachable", None

def ssl_check(domain):
    if not domain.startswith("https://"):
        domain = "https://" + domain
    host = domain.replace("https://", "").split('/')[0]
    
    try:
        context = ssl.create_default_context()
        with socket.create_connection((host, 443), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()
                issuer = dict(x[0] for x in cert['issuer']).get('commonName', 'Unknown')
                expiry_str = cert.get('notAfter')
                expiry = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
                return "valid", issuer, expiry
    except Exception:
        return "invalid", None, None

def domain_age_whois(domain: str):
    try:
        w = whois.whois(domain)
        creation = w.creation_date
        expiry = w.expiration_date
        
        if isinstance(creation, list):
            creation = creation[0]
        if isinstance(expiry, list):
            expiry = expiry[0]
        
        if not isinstance(creation, datetime) or not isinstance(expiry, datetime):
            return None
        
        if creation.tzinfo:
            creation = creation.replace(tzinfo=None)
        if expiry.tzinfo:
            expiry = expiry.replace(tzinfo=None)
        
        now = datetime.utcnow()
        delta = now - creation
        age_months = delta.days // 30
        age_years = age_months // 12
        
        if age_months < 12:
            risk = "🔴 High: DOMAIN age to low ❗"
        elif 12 <= age_months < 36:
            risk = "🟠 medium: not to young but browse cautiously ⚠️"
        else:
            risk = "🟢 low: domain is old enough and safe ✅"
        
        return {
            "creation_date": creation,
            "expiry_date": expiry,
            "age_months": age_months,
            "age_years": age_years,
            "risk_level": risk
        }
    except Exception:
        return None

# ============================================
# MAIN DRIVER - YOUR EXACT CODE WITH ADDITIONS
# ============================================

def main():
    """Main function - your exact code wrapped"""
    console_mgr.display_banner()
    
    while True:
        try:
            # Input prompt with enhanced styling
            if console_mgr.has_colorama:
                prompt = f"{console_mgr.Fore.YELLOW}📝 Enter URL/domain (or 'exit'):{console_mgr.Style.RESET_ALL} "
            else:
                prompt = "📝 Enter URL/domain (or 'exit'): "
            
            user_input = input(prompt).strip()
            
            if user_input.lower() == "exit":
                console_mgr.print_message("\n👋 Goodbye! Stay safe on the internet.", "green")
                break
            
            if user_input.lower() == "clear":
                os.system("cls" if os.name == "nt" else "clear")
                console_mgr.display_banner()
                continue
            
            # ========== STEP 1: Parse Domain ==========
            console_mgr.print_message(f"\n📍 running parse_domain(...)", "cyan")
            success, result = parse_domain(user_input)
            
            if not success:
                console_mgr.print_message(f"  ❌ {result}", "red")
                continue
            
            domain = result
            console_mgr.print_message(f"  ✅ parse_domain result: {domain}", "green")
            
            # Generate scan ID with emoji
            scan_id = str(uuid.uuid4())
            console_mgr.print_message(f"  🆔 scan recorded! UUID:{scan_id}", "cyan")
            
            # ========== STEP 2: HTTP Check ==========
            console_mgr.print_message(f"\n🌐 HTTP CHECK starting...", "cyan")
            status, code = http_status_check(domain)
            
            if status == "unreachable":
                console_mgr.print_message(f"  🔴 HTTP UNREACHABLE: Servers down try again later..", "red")
                console_mgr.print_message(f"  🔴 domain unreachable: stopping other scans automatically..", "red")
                continue
            elif status == "redirect":
                console_mgr.print_message(f"  🟠 HTTP redirects: the domain redirects to another url 🔁", "yellow")
                console_mgr.print_message(f"  ⚠️  status code: {code}", "white")
            elif status == "reachable":
                console_mgr.print_message(f"  🟢 HTTP reachable: the domain exists and is reachable ✅", "green")
                console_mgr.print_message(f"  ✅ status code: {code}", "white")
            
            # ========== STEP 3: SSL Check ==========
            console_mgr.print_message(f"\n🔐 SSL check starting...", "cyan")
            ssl_status, issuer, expiry = ssl_check(domain)
            
            free_cert_list = ["R12", "R3 DV", "R3 EV", "R3 CA", "R3 cross-signed", 
                             "let's encrypt", "R3", "R13", "zerossl", "buypass", 
                             "cloudflare", "google trust"]
            
            risk_score = 0
            risk_factors = []
            
            if ssl_status == "valid" and issuer:
                is_free = issuer in free_cert_list
                
                if is_free:
                    console_mgr.print_message(f"  🌏  status: valid ", "yellow")
                    console_mgr.print_message(f"  📝 issuer: {issuer} ✅", "yellow")
                    console_mgr.print_message(f"  🔴 valid but free ⚠️", "yellow")
                    risk_score += 10
                    risk_factors.append("free_ssl")
                else:
                    console_mgr.print_message(f"  💲 valid and paid ✅", "green")
                    console_mgr.print_message(f"  🌏  status: valid ✅", "green")
                    console_mgr.print_message(f"  📝  issuer: {issuer} ✅", "green")
                    console_mgr.print_message(f"  ⏳ SSL certificate Expiry Date: {expiry}", "cyan")
            else:
                console_mgr.print_message(f"  ⛔ invalid: ssl not found. data not encrypted!!", "red")
                risk_score += 30
                risk_factors.append("invalid_ssl")
            
            # ========== STEP 4: WHOIS Check ==========
            console_mgr.print_message(f"\n📅 Domain age check starting...", "cyan")
            whois_result = domain_age_whois(domain)
            
            if whois_result is None:
                console_mgr.print_message(f"  ⚠️  couldn't get domain age. (privacy activated)", "yellow")
                risk_score += 10
                risk_factors.append("privacy")
            else:
                console_mgr.print_message(f"  ⌛ created: {whois_result['creation_date'].date()}", "green")
                console_mgr.print_message(f"  ⏳ Expires: {whois_result['expiry_date'].date()}", "green")
                console_mgr.print_message(f"  📜 Domain Age: {whois_result['age_years']} years ({whois_result['age_months']} months)", "cyan")
                console_mgr.print_message(f"  Risk Level: {whois_result['risk_level'].capitalize()}", "white")
                
                if whois_result['age_months'] < 12:
                    risk_score += 15
                    risk_factors.append("new_domain")
            
            # ========== STEP 5: Redirect Scoring ==========
            if status == "redirect":
                risk_score += 3
                risk_factors.append("redirect")
            
            # ========== STEP 6: Risk Score Analysis ==========
            console_mgr.print_message(f"\n📊 Risk score analysis starting...", "cyan")
            
            # Determine verdict with emojis
            if risk_score >= 20:
                final_verdict = f"{console_mgr.Fore.RED if console_mgr.has_colorama else ''}🔴 High Risk: 90% of legitimate websites used paid certificates...🚨{console_mgr.Style.RESET_ALL if console_mgr.has_colorama else ''}"
            elif risk_score >= 17:
                final_verdict = f"{console_mgr.Fore.YELLOW if console_mgr.has_colorama else ''}🟠 medium risk: manually check domain before use...⚠️{console_mgr.Style.RESET_ALL if console_mgr.has_colorama else ''}"
            else:
                final_verdict = f"{console_mgr.Fore.GREEN if console_mgr.has_colorama else ''}🟢 safe: domain is safe..✅{console_mgr.Style.RESET_ALL if console_mgr.has_colorama else ''}"
            
            console_mgr.print_message(f"  🔰 Risk Score: {risk_score}", "cyan")
            console_mgr.print_message(f"  ♻️  Verdict: {final_verdict}", "cyan")
            
            # ========== NEW: RISK EXPLANATION SECTION ==========
            console_mgr.display_explanation(risk_score, risk_factors)
            
            # ========== FINAL SEPARATOR ==========
            if console_mgr.has_colorama:
                print(f"\n{console_mgr.Fore.CYAN}{'─'*60}{console_mgr.Style.RESET_ALL}")
            else:
                print(f"\n{'─'*60}")
            
        except KeyboardInterrupt:
            console_mgr.print_message(f"\n\n⚠️  Scan interrupted", "yellow")
            break
        except Exception as e:
            console_mgr.print_message(f"\n❌ Unexpected error: {e}", "red")

if __name__ == "__main__":
    # Disable SSL warnings
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    try:
        main()
    except Exception as e:
        console_mgr.print_message(f"Fatal error: {e}", "red")
        sys.exit(1)