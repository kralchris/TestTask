# Test Task

### Requirements

Python<br>
Command line

### Setup

I highly recommend using a virtual environment. For Linux:
```bash
python -m venv venv
./venv/bin/activate
```

### Running the app


Run the app in the console:
```command line:
1. Navigate to the directory where main.py and tools.py are located.
2. Run the following command:

python main.py <path_to_source> <path_to_replica> <interval> <path_to_log>

examples:
python main.py ./source ./replica 25 ./log_file.log
python main.py ./source ./copy 60 ./log.txt 
```

_**Note:** Of course, you are allowed to use absolute paths too._
