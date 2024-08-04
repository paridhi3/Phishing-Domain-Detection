# Import necessary libraries and modules
import os
import sys
import pandas as pd
from src.PDD.utils.common import load_object  # Utility function to load saved objects

from dataclasses import dataclass

import dns.resolver
import whois
import ipwhois
import requests
import socket
import ssl
import time
from urllib.parse import urlparse, parse_qs

@dataclass
class CustomData:
    directory_length: int
    time_domain_activation: int
    qty_slash_directory: int
    qty_at_file: int
    qty_slash_file: int
    qty_equal_file: int
    qty_dot_file: int
    ttl_hostname: int
    qty_equal_directory: int
    qty_plus_file: int
    asn_ip: int
    time_response: int
    time_domain_expiration: int
    qty_underline_file: int
    domain_length: int
    qty_percent_directory: int
    qty_dot_domain: int
    qty_hyphen_file: int
    file_length: int
    qty_asterisk_directory: int
    qty_exclamation_directory: int
    qty_asterisk_file: int
    qty_tilde_file: int
    qty_at_directory: int
    qty_vowels_domain: int
    qty_plus_directory: int
    qty_exclamation_file: int
    qty_dot_directory: int
    qty_mx_servers: int
    qty_nameservers: int
    qty_underline_directory: int
    qty_hyphen_directory: int
    qty_comma_directory: int
    qty_space_file: int
    qty_and_file: int
    qty_dollar_directory: int
    qty_questionmark_directory: int
    qty_space_directory: int
    qty_ip_resolved: int
    qty_redirects: int
    tls_ssl_certificate: bool
    qty_percent_file: int
    domain_spf: bool
    qty_hyphen_domain: int
    qty_and_directory: int
    qty_questionmark_file: int
    qty_hashtag_directory: int
    params_length: int
    qty_dot_params: int
    qty_params: int
    url_shortened: bool
    qty_equal_params: int
    qty_space_params: int


    @classmethod
    def from_url(cls, url):
        features = cls.extract_url_features(url)
        return cls(**features)

    @staticmethod
    def extract_url_features(url):
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.split(':')[0]
        path = parsed_url.path
        query = parsed_url.query
        params = parsed_url.params

        def count_occurrences(string, chars):
            return {char: string.count(char) for char in chars}

        chars_to_count = ".-_/=?@&! ~,+*#$%"

        domain_counts = count_occurrences(domain, chars_to_count)
        path_counts = count_occurrences(path, chars_to_count)
        query_counts = count_occurrences(query, chars_to_count)
        params_counts = count_occurrences(params, chars_to_count)

        vowels = 'aeiou'
        qty_vowels_domain = sum(domain.lower().count(vowel) for vowel in vowels)

        def is_ip(domain):
            try:
                socket.inet_aton(domain)
                return True
            except socket.error:
                return False

        def get_time_response(domain):
            try:
                start_time = time.time()
                requests.get(f"http://{domain}", timeout=5)
                return time.time() - start_time
            except:
                return -1

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
                ip_address = domain_to_ip(domain)
                if ip_address:
                    obj = ipwhois.IPWhois(ip_address)
                    result = obj.lookup_rdap()
                    asn = result.get('asn')
                    if asn:
                        return int(asn.split(' ')[0])
                    else:
                        return -1
                else:
                    return -1
            except:
                return -1

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
                return len(ips[2])
            except:
                return -1

        def get_qty_nameservers(domain):
            try:
                answers = dns.resolver.resolve(domain, 'NS')
                return len(answers)
            except:
                return -1

        def get_qty_mx_servers(domain):
            try:
                answers = dns.resolver.resolve(domain, 'MX')
                return len(answers)
            except:
                return 0

        def get_ttl_hostname(domain):
            try:
                answers = dns.resolver.resolve(domain, 'A')
                return answers.rrset.ttl
            except:
                return -1

        def check_tls_ssl_certificate(domain):
            try:
                context = ssl.create_default_context()
                with socket.create_connection((domain, 443)) as sock:
                    with context.wrap_socket(sock, server_hostname=domain) as ssock:
                        cert = ssock.getpeercert()
                        return 1 if cert else 0
            except:
                return 0

        def get_qty_redirects(url):
            try:
                response = requests.head(url, allow_redirects=True)
                return len(response.history)
            except:
                return -1

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

        features = {
            "directory_length": len(path),
            "time_domain_activation": time_domain_activation,
            "qty_slash_directory": path_counts['/'],
            "qty_at_file": query_counts['@'],
            "qty_slash_file": query_counts['/'],
            "qty_equal_file": query_counts['='],
            "qty_dot_file": query_counts['.'],
            "ttl_hostname": ttl_hostname,
            "qty_equal_directory": path_counts['='],
            "qty_plus_file": query_counts['+'],
            "asn_ip": asn_ip,
            "time_response": time_response,
            "time_domain_expiration": time_domain_expiration,
            "qty_underline_file": query_counts['_'],
            "domain_length": len(domain),
            "qty_percent_directory": path_counts['%'],
            "qty_dot_domain": domain_counts['.'],
            "qty_hyphen_file": query_counts['-'],
            "file_length": len(query),
            "qty_asterisk_directory": path_counts['*'],
            "qty_exclamation_directory": path_counts['!'],
            "qty_asterisk_file": query_counts['*'],
            "qty_tilde_file": query_counts['~'],
            "qty_at_directory": path_counts['@'],
            "qty_vowels_domain": qty_vowels_domain,
            "qty_plus_directory": path_counts['+'],
            "qty_exclamation_file": query_counts['!'],
            "qty_dot_directory": path_counts['.'],
            "qty_mx_servers": qty_mx_servers,
            "qty_nameservers": qty_nameservers,
            "qty_underline_directory": path_counts['_'],
            "qty_hyphen_directory": path_counts['-'],
            "qty_comma_directory": path_counts[','],
            "qty_space_file": query_counts[' '],
            "qty_and_file": query_counts['&'],
            "qty_dollar_directory": path_counts['$'],
            "qty_questionmark_directory": path_counts['?'],
            "qty_space_directory": path_counts[' '],
            "qty_ip_resolved": qty_ip_resolved,
            "qty_redirects": qty_redirects,
            "tls_ssl_certificate": tls_ssl_certificate,
            "qty_percent_file": query_counts['%'],
            "domain_spf": domain_spf,
            "qty_hyphen_domain": domain_counts['-'],
            "qty_and_directory": path_counts['&'],
            "qty_questionmark_file": query_counts['?'],
            "qty_hashtag_directory": path_counts['#'],
            "params_length": len(params),
            "qty_dot_params": params_counts['.'],
            "qty_params": len(parse_qs(query)),
            "url_shortened": 1 if len(url) < 20 else 0,
            "qty_equal_params": params_counts['='],
            "qty_space_params": params_counts[' ']
        }

        return features

    def get_data_as_data_frame(self):
        """
        Convert the custom data attributes (entered by user) into a DataFrame.
        Returns: DataFrame containing the custom data
        """
        try:
            # Create a dictionary from the custom data attributes
            custom_data_input_dict = {
                "directory_length": [self.directory_length],
                "time_domain_activation": [self.time_domain_activation],
                "qty_slash_directory": [self.qty_slash_directory],
                "qty_at_file": [self.qty_at_file],
                "qty_slash_file": [self.qty_slash_file],
                "qty_equal_file": [self.qty_equal_file],
                "qty_dot_file": [self.qty_dot_file],
                "ttl_hostname": [self.ttl_hostname],
                "qty_equal_directory": [self.qty_equal_directory],
                "qty_plus_file": [self.qty_plus_file],
                "asn_ip": [self.asn_ip],
                "time_response": [self.time_response],
                "time_domain_expiration": [self.time_domain_expiration],
                "qty_underline_file": [self.qty_underline_file],
                "domain_length": [self.domain_length],
                "qty_percent_directory": [self.qty_percent_directory],
                "qty_dot_domain": [self.qty_dot_domain],
                "qty_hyphen_file": [self.qty_hyphen_file],
                "file_length": [self.file_length],
                "qty_asterisk_directory": [self.qty_asterisk_directory],
                "qty_exclamation_directory": [self.qty_exclamation_directory],
                "qty_asterisk_file": [self.qty_asterisk_file],
                "qty_tilde_file": [self.qty_tilde_file],
                "qty_at_directory": [self.qty_at_directory],
                "qty_vowels_domain": [self.qty_vowels_domain],
                "qty_plus_directory": [self.qty_plus_directory],
                "qty_exclamation_file": [self.qty_exclamation_file],
                "qty_dot_directory": [self.qty_dot_directory],
                "qty_mx_servers": [self.qty_mx_servers],
                "qty_nameservers": [self.qty_nameservers],
                "qty_underline_directory": [self.qty_underline_directory],
                "qty_hyphen_directory": [self.qty_hyphen_directory],
                "qty_comma_directory": [self.qty_comma_directory],
                "qty_space_file": [self.qty_space_file],
                "qty_and_file": [self.qty_and_file],
                "qty_dollar_directory": [self.qty_dollar_directory],
                "qty_questionmark_directory": [self.qty_questionmark_directory],
                "qty_space_directory": [self.qty_space_directory],
                "qty_ip_resolved": [self.qty_ip_resolved],
                "qty_redirects": [self.qty_redirects],
                "tls_ssl_certificate": [self.tls_ssl_certificate],
                "qty_percent_file": [self.qty_percent_file],
                "domain_spf": [self.domain_spf],
                "qty_hyphen_domain": [self.qty_hyphen_domain],
                "qty_and_directory": [self.qty_and_directory],
                "qty_questionmark_file": [self.qty_questionmark_file],
                "qty_hashtag_directory": [self.qty_hashtag_directory],
                "params_length": [self.params_length],
                "qty_dot_params": [self.qty_dot_params],
                "qty_params": [self.qty_params],
                "url_shortened": [self.url_shortened],
                "qty_equal_params": [self.qty_equal_params],
                "qty_space_params": [self.qty_space_params]
            }

            # Convert the dictionary to a DataFrame and return it
            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise e




class PredictPipeline:
    """
    A class to handle the prediction pipeline.
    Contains methods to generate predictions based on user input values.
    """

    def __init__(self):
        pass

    def predict(self, features):
        """
        Load the model, then predict the target using the provided features by the user.

        features: DataFrame containing the input features provided by the user
        Returns: Array of predictions
        """
        try:
            # Define paths to the saved model and preprocessor objects
            model_path = os.path.join("artifacts", "model.pkl")

            print("Before Loading Model Object")

            # Load the saved model and preprocessor objects
            model = load_object(file_path=model_path)
            print("After Loading Model Object")

            # Predict the target using the loaded model
            preds = model.predict(features)

            return preds
        
        
        except Exception as e:
            raise e