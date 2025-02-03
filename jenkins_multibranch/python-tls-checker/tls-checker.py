import subprocess
from datetime import datetime

def check_cert_expiration(domain, port):
    try:
        # Use openssl command to get certificate information
        command = f"openssl s_client -connect {domain}:{port} -servername {domain} 2>/dev/null | openssl x509 -noout -subject -issuer -dates"
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode == 0:
            # Decode the byte output
            output = result.stdout.decode('utf-8')

            # Parse the expiration date
            expiration_date_str = output.split("notAfter=")[1].split("\n")[0].strip()
            expiration_date = datetime.strptime(expiration_date_str, "%b %d %H:%M:%S %Y %Z")

            # Parse subject and issuer information
            subject = output.split("subject=")[1].split("\n")[0].strip()
            issuer = output.split("issuer=")[1].split("\n")[0].strip()

            # Check if the certificate is self-signed
            is_self_signed = subject == issuer

            return expiration_date, None, subject, issuer, is_self_signed
        else:
            # Decode the byte error message
            error_message = result.stderr.decode('utf-8').strip()
            return None, f"Certificate Error: {error_message}", None, None, None
    except Exception as e:
        return None, f"Error: {str(e)}", None, None, None

def main():
    file_path = "/app/tls-domains"

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            parts = line.split(":")
            if len(parts) != 2:
                print(f"Invalid format in line: {line}. Skipping.")
                continue

            domain, port = parts[0], parts[1]
            expiration_date, error_message, subject, issuer, is_self_signed = check_cert_expiration(domain, port)

            if expiration_date:
                print(f"Domain: {domain}, Port: {port}")
                print(f"Expiration Date: {expiration_date}")
                print(f"Subject: {subject}")
                print(f"Issuer: {issuer}")
                print(f"Is Self-Signed: {is_self_signed}")
                #print(f"-----------------------------------\n")
            else:
                print(f"Domain: {domain}, Port: {port}, Certificate Error: {error_message}")
                print(f"-----------------------------------\n")

if __name__ == "__main__":
    main()