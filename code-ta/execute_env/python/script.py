import os

# Get the script from the environment variable
script_to_run = os.environ.get('SCRIPT_TO_RUN')

# Execute the script
exec(script_to_run)
