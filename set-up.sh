# I consider you already have installed python3 in your machine

# Install virtual environments
echo "Installing virtual environments..."
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt

# Create repository structure
echo "Creating repository structure..."
mkdir data
mkdir logs

# Execute programs and write to log files
echo "Executing programs..."
echo "Running q1_memory.py and saving the result to the log file..."
.venv/bin/python3 src/q1_memory.py >> logs/q1.log
.venv/bin/python3 src/q1_time.py >> logs/q1.log

echo "Running q2_memory.py and saving the result to the log file..."
.venv/bin/python3 src/q2_memory.py >> logs/q2.log
.venv/bin/python3 src/q2_time.py >> logs/q2.log

echo "Running q3_memory.py and saving the result to the log file..."
.venv/bin/python3 src/q3_memory.py >> logs/q3.log
.venv/bin/python3 src/q3_time.py >> logs/q3.log

echo "All done. Bye Bye."
