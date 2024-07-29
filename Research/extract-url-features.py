import dns.resolver
import whois
import ipwhois
import requests
import socket
import ssl
import time
from urllib.parse import urlparse, parse_qs

def extract_url_features(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.split(':')[0]
    path = parsed_url.path
    query = parsed_url.query
    params = parsed_url.params
    fragment = parsed_url.fragment
    
    def count_occurrences(string, chars):
        return {char: string.count(char) for char in chars}
    
    chars_to_count = ".-_/=?@&! ~,+*#$%"
    
    # URL FEATURES
    url_counts = count_occurrences(url, chars_to_count)
    tld = domain.split('.')[-1] if '.' in domain else ''

    # URL DOMAIN FEATURES
    domain_counts = count_occurrences(domain, chars_to_count)

    vowels = 'aeiou'
    qty_vowels_domain = sum(domain.lower().count(vowel) for vowel in vowels)

    def is_ip(domain):
        try:
            socket.inet_aton(domain)
            return True
        except socket.error:
            return False
        
    # URL DIRECTORY FEATURES
    path_counts = count_occurrences(path, chars_to_count)

    # URL FILE FEATURES
    query_counts = count_occurrences(query, chars_to_count)

    # URL PARAMETERS FEATURES
    params_counts = count_occurrences(params, chars_to_count)

    # ATTRIBUTES BASED ON RESOLVING URL AND EXTERNAL SERVICES
    
    def get_time_response(domain):
        try:
            start_time = time.time()
            requests.get(f"http://{domain}", timeout=5)
            return time.time() - start_time
        except:
            return None

    def domain_has_spf(domain):
        try:
            answers = dns.resolver.resolve(domain, 'TXT')
            for rdata in answers:
                if 'v=spf1' in str(rdata):
                    return 1
            return 0
        except:
            return -1
        
    def domain_to_ip(domain):
        try:
            ip_address = socket.gethostbyname(domain)
            return ip_address
        except socket.error:
            return -1
        
    def get_asn_ip(domain):
        try:
            # Convert domain to IP address
            ip_address = domain_to_ip(domain)
            if ip_address:
                # Perform WHOIS lookup using ipwhois library
                obj = ipwhois.IPWhois(ip_address)
                result = obj.lookup_rdap()
                # Extract ASN information if available
                asn = result.get('asn')
                if asn:
                    return int(asn.split(' ')[0])  # Extract ASN number
                else:
                    return -1  # Return -1 if ASN information not found
            else:
                return -1  # Return -1 if domain to IP conversion fails

        except Exception:
            return -1  # Return -1 on error

    def get_whois_info(domain):
        try:
            domain_info = whois.whois(domain)
            creation_date = domain_info.creation_date
            expiration_date = domain_info.expiration_date
            
            if isinstance(creation_date, list):
                creation_date = creation_date[0]
            if isinstance(expiration_date, list):
                expiration_date = expiration_date[0]
            
            time_domain_activation = (time.time() - creation_date.timestamp()) / (60 * 60 * 24) if creation_date else -1
            time_domain_expiration = (expiration_date.timestamp() - time.time()) / (60 * 60 * 24) if expiration_date else -1
            return time_domain_activation, time_domain_expiration
        except:
            return -1, -1
        
    def get_qty_ip_resolved(domain):
        try:
            ips = socket.gethostbyname_ex(domain)
            return len(ips[2])  # Return the number of resolved IPs
        except socket.gaierror:
            return -1  # Return -1 if there's an error resolving IPs
        
    def get_qty_nameservers(domain):
        try:
            answers = dns.resolver.resolve(domain, 'NS')
            return len(answers)  # Return the number of resolved name servers
        except dns.resolver.NoAnswer:
            return 0  # Return 0 if no name servers found
        except dns.resolver.NXDOMAIN:
            return -1  # Return -1 if domain does not exist
        except dns.resolver.Timeout:
            return -1  # Return -1 on timeout or other DNS resolution errors

    def get_qty_mx_servers(domain):
        try:
            answers = dns.resolver.resolve(domain, 'MX')
            qty_mx_servers = len(answers)
        except:
            qty_mx_servers = 0
        return qty_mx_servers
    
    def get_ttl_hostname(domain):
        try:
            answers = dns.resolver.resolve(domain, 'A')
            return answers.rrset.ttl  # Return TTL of the hostname
        except dns.resolver.NoAnswer:
            return -1  # Return -1 if no answer found
        except dns.resolver.NXDOMAIN:
            return -1  # Return -1 if domain does not exist
        except dns.resolver.Timeout:
            return -1  # Return -1 on timeout or other DNS resolution errors
        
    def check_tls_ssl_certificate(domain):
        try:
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    return 1 if cert else 0  # Return True if valid certificate found
        except ssl.SSLError:
            return 0  # Return False if SSL error occurs or no certificate found
        except (socket.gaierror, socket.timeout):
            return 0  # Return False on connection or timeout errors

    # Function for qty_redirects (Number of Redirects)
    def get_qty_redirects(url):
        try:
            response = requests.head(url, allow_redirects=True)
            return len(response.history)  # Return the number of redirects followed
        except requests.RequestException:
            return -1  # Return -1 if there's an error in making the request

    # Function for url_google_index (Check if URL is Indexed on Google)
    def is_url_indexed_on_google(url):
        try:
            response = requests.get(f"https://www.google.com/search?q=info:{url}")
            return 1 if response.status_code == 200 and url in response.text else False
        except requests.RequestException:
            return 0  # Return False if there's an error in making the request

    # Function for domain_google_index (Check if Domain is Indexed on Google)
    def is_domain_indexed_on_google(domain):
        try:
            response = requests.get(f"https://www.google.com/search?q=site:{domain}")
            return 1 if response.status_code == 200 and domain in response.text else False
        except requests.RequestException:
            return 0  # Return False if there's an error in making the request
    
    
    time_response = get_time_response(domain)
    domain_spf = domain_has_spf(domain)
    time_domain_activation, time_domain_expiration = get_whois_info(domain)
    qty_mx_servers = get_qty_mx_servers(domain)
    qty_ip_resolved = get_qty_ip_resolved(domain)
    asn_ip = get_asn_ip(domain)
    qty_nameservers = get_qty_nameservers(domain)
    ttl_hostname = get_ttl_hostname(domain)
    tls_ssl_certificate = check_tls_ssl_certificate(domain)
    qty_redirects = get_qty_redirects(url)
    url_google_index = is_url_indexed_on_google(url)
    domain_google_index = is_domain_indexed_on_google(domain)
    
    features = {
        # URL features
        "qty_dot_url": url_counts['.'],
        "qty_hyphen_url": url_counts['-'],
        "qty_underline_url": url_counts['_'],
        "qty_slash_url": url_counts['/'],
        "qty_questionmark_url": url_counts['?'],
        "qty_equal_url": url_counts['='],
        "qty_at_url": url_counts['@'],
        "qty_and_url": url_counts['&'],
        "qty_exclamation_url": url_counts['!'],
        "qty_space_url": url_counts[' '],
        "qty_tilde_url": url_counts['~'],
        "qty_comma_url": url_counts[','],
        "qty_plus_url": url_counts['+'],
        "qty_asterisk_url": url_counts['*'],
        "qty_hashtag_url": url_counts['#'],
        "qty_dollar_url": url_counts['$'],
        "qty_percent_url": url_counts['%'],
        "qty_tld_url": len(tld),
        "length_url": len(url),
        
        # Domain features
        "qty_dot_domain": domain_counts['.'],
        "qty_hyphen_domain": domain_counts['-'],
        "qty_underline_domain": domain_counts['_'],
        "qty_slash_domain": domain_counts['/'],
        "qty_questionmark_domain": domain_counts['?'],
        "qty_equal_domain": domain_counts['='],
        "qty_at_domain": domain_counts['@'],
        "qty_and_domain": domain_counts['&'],
        "qty_exclamation_domain": domain_counts['!'],
        "qty_space_domain": domain_counts[' '],
        "qty_tilde_domain": domain_counts['~'],
        "qty_comma_domain": domain_counts[','],
        "qty_plus_domain": domain_counts['+'],
        "qty_asterisk_domain": domain_counts['*'],
        "qty_hashtag_domain": domain_counts['#'],
        "qty_dollar_domain": domain_counts['$'],
        "qty_percent_domain": domain_counts['%'],
        "qty_vowels_domain": qty_vowels_domain,
        "domain_length": len(domain),
        "domain_in_ip": 1 if is_ip(domain) else 0,
        "server_client_domain": 1 if "client" in domain or "server" in domain else 0,
        
        # Directory features
        "qty_dot_directory": path_counts['.'],
        "qty_hyphen_directory": path_counts['-'],
        "qty_underline_directory": path_counts['_'],
        "qty_slash_directory": path_counts['/'],
        "qty_questionmark_directory": path_counts['?'],
        "qty_equal_directory": path_counts['='],
        "qty_at_directory": path_counts['@'],
        "qty_and_directory": path_counts['&'],
        "qty_exclamation_directory": path_counts['!'],
        "qty_space_directory": path_counts[' '],
        "qty_tilde_directory": path_counts['~'],
        "qty_comma_directory": path_counts[','],
        "qty_plus_directory": path_counts['+'],
        "qty_asterisk_directory": path_counts['*'],
        "qty_hashtag_directory": path_counts['#'],
        "qty_dollar_directory": path_counts['$'],
        "qty_percent_directory": path_counts['%'],
        "directory_length": len(path),
        
        # File features
        "qty_dot_file": query_counts['.'],
        "qty_hyphen_file": query_counts['-'],
        "qty_underline_file": query_counts['_'],
        "qty_slash_file": query_counts['/'],
        "qty_questionmark_file": query_counts['?'],
        "qty_equal_file": query_counts['='],
        "qty_at_file": query_counts['@'],
        "qty_and_file": query_counts['&'],
        "qty_exclamation_file": query_counts['!'],
        "qty_space_file": query_counts[' '],
        "qty_tilde_file": query_counts['~'],
        "qty_comma_file": query_counts[','],
        "qty_plus_file": query_counts['+'],
        "qty_asterisk_file": query_counts['*'],
        "qty_hashtag_file": query_counts['#'],
        "qty_dollar_file": query_counts['$'],
        "qty_percent_file": query_counts['%'],
        "file_length": len(query),
        
        # Parameters features
        "qty_dot_params": params_counts['.'],
        "qty_hyphen_params": params_counts['-'],
        "qty_underline_params": params_counts['_'],
        "qty_slash_params": params_counts['/'],
        "qty_questionmark_params": params_counts['?'],
        "qty_equal_params": params_counts['='],
        "qty_at_params": params_counts['@'],
        "qty_and_params": params_counts['&'],
        "qty_exclamation_params": params_counts['!'],
        "qty_space_params": params_counts[' '],
        "qty_tilde_params": params_counts['~'],
        "qty_comma_params": params_counts[','],
        "qty_plus_params": params_counts['+'],
        "qty_asterisk_params": params_counts['*'],
        "qty_hashtag_params": params_counts['#'],
        "qty_dollar_params": params_counts['$'],
        "qty_percent_params": params_counts['%'],
        "params_length": len(params),
        "tld_present_params": 1 if tld != '' else 0,
        "qty_params": len(parse_qs(query)),
        "email_in_url": 1 if '@' in url else 0,
        
        # WHOIS and DNS features
        "time_response": time_response if time_response is not None else -1,
        "domain_spf": domain_spf if domain_spf is not None else -1,
        "asn_ip": asn_ip,
        "time_domain_activation": time_domain_activation if time_domain_activation is not None else -1,
        "time_domain_expiration": time_domain_expiration if time_domain_expiration is not None else -1,
        "qty_ip_resolved": qty_ip_resolved,  # Placeholder, requires DNS lookup
        "qty_nameservers": qty_nameservers,  # Placeholder, requires DNS lookup
        "qty_mx_servers": qty_mx_servers if qty_mx_servers  is not None else 0,
        "ttl_hostname": ttl_hostname,  # Placeholder, requires DNS lookup
        "tls_ssl_certificate": tls_ssl_certificate,  # Placeholder, requires SSL/TLS library
        "qty_redirects": qty_redirects,  # Placeholder, requires HTTP request handling
        "url_google_index": url_google_index,
        "domain_google_index": domain_google_index,
        "url_shortened": 1 if len(url) < 20 else 0,  # Example condition for shortened URL
    }
    
    return features