import os

# Get all txt files in current directory
txt_files = [f for f in os.listdir() if f.endswith('.txt')]

# Collect addresses from all txt files
all_addresses = []
for txt_file in txt_files:
   with open(txt_file, 'r') as f:
       addresses = f.readlines()
       all_addresses.extend([addr.strip() for addr in addresses if addr.strip()])

# Format unique addresses
formatted = [f"- '{addr}'" for addr in set(all_addresses)]

# Append to yaml file 
with open('addresses.yaml', 'a') as f:
   f.write('\n'.join(formatted) + '\n')