import subprocess
import re

def get_all_wifi_passwords():
    try:
        result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'],
                                capture_output=True, text=True, encoding='utf-8')
        profiles = re.findall(r"(?:All User Profile)\s*:\s*(.*)", result.stdout)

        if not profiles:
            return "No Wi-Fi profiles found."

        wifi_passwords = {}

        for profile in profiles:
            profile = profile.strip()
            result = subprocess.run(['netsh', 'wlan', 'show', 'profile', f'name={profile}', 'key=clear'],
                                    capture_output=True, text=True, encoding='utf-8')

            password_match = re.search(r'(?:Key Content)\s*:\s*(.*)', result.stdout)
            password = password_match.group(1) if password_match else "No password found"

            wifi_passwords[profile] = password

        return wifi_passwords


    except Exception as e:
        return f"Error: {e}"

wifi_passwords = get_all_wifi_passwords()
if isinstance(wifi_passwords, dict):
    print("\nSaved Wi-Fi Passwords:\n")
    for wifi, password in wifi_passwords.items():
        print(f"Wi-Fi Name: {wifi}  |  Password: {password}")
else:
    print(wifi_passwords)