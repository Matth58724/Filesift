from textx import metamodel_from_file  # Import textX
import os  # For file system operations
import shutil  # For moving files/folders
import sys  # For command-line argument handling

# Load the DSL grammar from the filesift.tx file
filesift_mm = metamodel_from_file('filesift.tx')

# Check if a .flst file was given as a command line argument
if len(sys.argv) != 2:
    print("Usage: python FileSift.py <file.flst>")
    sys.exit(1)

# Get the provided file name
flst_file = sys.argv[1]
model = filesift_mm.model_from_file(flst_file)


class FileSift:
    def __init__(self):
        # Counter to keep track of how many files are moved
        self.moved_count = 0  
        # This will store the source folder path for operations like sorting and move back
        self.source = None    

        # Main interpreter function that processes each statement in the model
        # The program can contain multiple statements like print, fizzbuzz, sort, etc.
    def interpret(self, model):
        # Loop through each statement in the DSL file.
        for stmt in model.statements:
            stmt_type = stmt.__class__.__name__
            # Check if the statement is a Print command
            if stmt_type == "PrintCommand":
                self._execute_print(stmt.messages)
            # Check if the statement is a FizzBuzz command
            elif stmt_type == "FizzBuzzCommand":
                start = int(stmt.start)
                end = int(stmt.end)
                dest = stmt.dest.path
                self._execute_fizzbuzz(start, end, dest)
            # Check if the statement is a Sort command
            elif stmt_type == "SortCommand":
                self._execute_sort(stmt)
            else:
                print("Unrecognized command:", stmt_type)

        # Executes a Print command.
        # It takes a list of string messages and strips the enclosing quotes
        # joins the messages with a space and prints the output
    def _execute_print(self, messages):
        # Remove the enclosing quotes from each string literal
        clean_messages = [
            m[1:-1] if m.startswith('"') and m.endswith('"') else m 
            for m in messages
        ]
        # Join the messages together with a space in between them
        output = " ".join(clean_messages)
        print(output)

        # Executes a FizzBuzz command
        # It writes the FizzBuzz sequence from start to end into a file named "FizzBuzz.txt"
        # in the destination folder given in the flst file
    def _execute_fizzbuzz(self, start, end, dest):
        os.makedirs(dest, exist_ok=True)  # Makes sure the destination folder exists before anything else
        output_file = os.path.join(dest, "FizzBuzz.txt")
        with open(output_file, "w") as fout:
            # Generate the fizzbuzz output line by line
            for i in range(start, end + 1):
                if i % 15 == 0:
                    fout.write("FizzBuzz\n")
                elif i % 3 == 0:
                    fout.write("Fizz\n")
                elif i % 5 == 0:
                    fout.write("Buzz\n")
                else:
                    fout.write(f"{i}\n")
        print(f"Created FizzBuzz output at {output_file}")

        # Executes a file sorting command
        # It supports normal sorting based on file extension rules or a move_back operation
    def _execute_sort(self, sort_command):
        # Get the source folder from the SortCommand
        source = sort_command.source.path

        # If the sort command contains a move_back command then
        # execute the move back function instead
        if sort_command.move_back is not None:
            print("Moving all files back from sorted subfolders to the destination folder...")
            dest = sort_command.move_back.dest.path
            self.source = source  # Set the source folder for move_back operations
            self._move_back(dest)
            print(f"Total files moved back: {self.moved_count}")
            return

        # Otherwise, proceed with the regular file sorting
        self.source = source  # Set the source folder where files are to be sorted
        rules = sort_command.rules
        fallback = sort_command.fallback.dest if sort_command.fallback else None

        # Loop over each file in the source folder
        for file in os.listdir(source):
            full_path = os.path.join(source, file)
            # Skip if it is not a file and its something else like a folder/directory
            if not os.path.isfile(full_path):
                continue

            moved = False  # Marks if the file has been moved
            # Get the file extension without the dot and convert it to lowercase
            ext = os.path.splitext(file)[1][1:].lower()

            # Loop over each defined rule in the DSL to check for matching file extension
            for rule in rules:
                # Process each extension in the rule by stripping quotes and converting to lowercase
                rule_extensions = [
                    e[1:-1].lower() if e.startswith('"') and e.endswith('"') else e.lower()
                    for e in rule.extensions
                ]
                # If the file's extension is found in the rule then move the file
                if ext in rule_extensions:
                    self._move(full_path, rule.dest.path)
                    moved = True
                    break

            # If no rule matched and a fallback folder is defined then move the file to the fallback
            if not moved and fallback:
                self._move(full_path, fallback.path)

        print(f"Total files sorted: {self.moved_count}")

        # Moves files from all subfolders and the source folder back to a single destination
        # This method recursively looks into subfolders of the source and moves files
    def _move_back(self, destination):
        os.makedirs(destination, exist_ok=True)  # Make sure the destination folder actually exists
        # Iterate through each item in the source folder
        for item in os.listdir(self.source):
            full_item_path = os.path.join(self.source, item)
            if os.path.isdir(full_item_path):
                # If the item is a directory then move each file from that subdirectory
                for file in os.listdir(full_item_path):
                    file_path = os.path.join(full_item_path, file)
                    if os.path.isfile(file_path):
                        self._move(file_path, destination)
            elif os.path.isfile(full_item_path):
                # If the item is a file in the source folder then move it as well.
                self._move(full_item_path, destination)

        # Moves a single file from the source path src to the destination folder dest
        # It creates the destination folder if it doesn't exist, moves the file, and then increments the counter by +1
    def _move(self, src, dest):
        os.makedirs(dest, exist_ok=True)
        shutil.move(src, os.path.join(dest, os.path.basename(src)))
        self.moved_count += 1
        print(f"Moved {os.path.basename(src)} to {dest}")


# Instantiate the interpreter and run it on the loaded model
flst = FileSift()
flst.interpret(model)
