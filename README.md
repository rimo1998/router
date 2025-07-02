Interactive Web Login Brute-ForcerAuthored by: [Your Name Here]A user-friendly, interactive Python script designed for ethical hackers and penetration testers to audit the password strength of web login portals, such as those found on routers and IoT devices.⚠️ Disclaimer: For Educational & Ethical Use OnlyThis tool is intended for use on networks and devices that you own or have explicit, written permission to test. Unauthorized access to computer systems is illegal. The author is not responsible for any misuse or damage caused by this script. Always act responsibly and ethically.DescriptionMany IoT devices and routers have simple web-based login portals. This script provides an interactive framework to perform a dictionary-based brute-force attack against these portals to test for weak or default passwords.Instead of requiring users to edit code, this tool launches an interactive wizard that guides you through the configuration process, making it accessible to users of all skill levels.FeaturesInteractive Setup Wizard: No code editing required! The script asks you for all the necessary target information.Universal Compatibility: Can be configured to work with almost any web login form.Multiple Encoding Methods: Supports both plain-text and base64 encoded passwords.Flexible Success Detection: Can identify a successful login by checking for either a page redirect or specific text in the server's response.Clean & User-Friendly Interface: Provides clear instructions and feedback during the attack.Step 1: Reconnaissance (Finding the Login Details)Before running the script, you need to investigate how your target's login process works.Open your target's login page in a web browser (e.g., Chrome or Firefox).Press F12 to open the Developer Tools.Click on the "Network" tab.Try to log in with any incorrect password (e.g., "test").A new entry will appear in the Network log. It might be named LoginCheck, login.cgi, goform/login, etc. Click on this entry.Now, look at the details on the right side to find the following information for the wizard:Target IP Address: The IP of the device (e.g., 192.168.0.1).Login URL Path: In the "Headers" tab, find the "Request URL". The part after the IP address is the path (e.g., /LoginCheck).Payload / Form Data: Scroll down to the "Payload" or "Form Data" section. Note all the field names and their values (e.g., Username: admin). This is what you'll enter in the wizard.Password Encoding: Look at the value for the password field in the payload. If it's a long string of random-looking characters, the encoding is base64. Otherwise, it's plain.Success Condition: How do you know a login works?Redirect: After a successful login, look at the network log. If you see a status of 302 and a "Location" header pointing to a new page like index.asp, the type is redirect.Text in Response: If the page doesn't redirect, look at the "Response" tab after a successful login. If it contains unique text like {"error":0}, the type is text_in_response.Step 2: Running the ToolOnce you have the information from Step 1, you're ready to run the tool.Make sure you have Python installed.Install the required library:pip install requests
Prepare your password wordlist file (e.g., passwords.txt).Run the script from your terminal:python your_script_name.py
The interactive wizard will start. Answer each question using the details you gathered.Example Interactive Session:--- Interactive Target Configuration ---

I will now ask for details about your target. Find this info using your
browser's F12 Developer Tools in the 'Network' tab after a login attempt.

1. Target IP Address
   (e.g., 192.168.0.1, 192.168.1.1)
   > Enter IP: 192.168.0.1

2. Login URL Path
   (This is the end part of the 'Request URL', e.g., /LoginCheck, /goform/login)
   > Enter URL Path: /LoginCheck

3. Payload / Form Data
   (Enter all fields sent with the login. For the password field's value,
   type the special word '{password}' exactly as shown.)
   > Enter Field Name (or press Enter to finish): Username
   > Enter Value for 'Username': admin
   > Enter Field Name (or press Enter to finish): Password
   > Enter Value for 'Password': {password}
   > Enter Field Name (or press Enter to finish):

4. Password Encoding Method
   (How the password is sent. Check the 'Payload' tab. If it looks like
   random letters and numbers, it's likely base64.)
   > Enter Encoding ('plain' or 'base64'): base64

5. Success Condition
   (How do we know a login was successful?)
   - 'redirect': The browser is sent to a new page (e.g., index.asp).
   - 'text_in_response': The server sends back a specific message (e.g., '{"error":0}').
   > Enter Condition Type ('redirect' or 'text_in_response'): redirect

   (For a 'redirect', what text should we look for?)
   > Enter Success Value: index.asp

--- Configuration Complete! ---

📂 Enter the path to your password wordlist file: passwords.txt
The attack will now begin with your custom configuration.
