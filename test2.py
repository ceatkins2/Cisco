import paramiko
import getpass
import time
import concurrent.futures

def download_file_to_switch(ip, username, password):
    source_url = "<URL OF FILE, include the file name>"
    destination_path = "flash:/<file name>"
    
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print(f"Starting file transfer to {ip}...")
        
        # Connect to the switch
        ssh_client.connect(ip, username=username, password=password)
        
        # Start an interactive SSH session
        ssh_session = ssh_client.invoke_shell()
        
        # Construct the "copy" command
        copy_command = f'copy {source_url} {destination_path}'
        
        # Send the "copy" command
        ssh_session.send(copy_command + "\n")
        time.sleep(2)  # Wait for the prompt
        
        # Send "Enter" to accept the prompt
        ssh_session.send("\n")
        
        # Wait for the completion message
        while True:
            output = ssh_session.recv(5000).decode()
            if "bytes copied in" in output:
                print(f"File successfully downloaded to {ip}:{destination_path}")
                break
            elif "Error" in output:
                print(f"Error on {ip}: {output}")
                break
            time.sleep(2)  # Wait for more output
        
        # Close the interactive SSH session
        ssh_session.close()
    except Exception as e:
        print(f"Error connecting to {ip}: {str(e)}")
    finally:
        ssh_client.close()

# User input
username = input("Enter your username: ")
password = getpass.getpass("Enter your password (it will be obscured): ")

# List of switch IPs
switch_ips = ["<Switch-IP-1>", "<Switch-IP-2>"]  # Replace with your switch IPs or add more IPs

# Use ThreadPoolExecutor to download the file to all switches concurrently
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(download_file_to_switch, ip, username, password) for ip in switch_ips]
    for future in concurrent.futures.as_completed(futures):
        future.result()
