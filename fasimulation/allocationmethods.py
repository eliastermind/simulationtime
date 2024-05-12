import PySimpleGUI as sg
import pandas as pd  # Import pandas library

# Reading data from Excel
df = pd.read_csv('filesimsim.csv')

# Writing data to Excel
df.to_csv('filesimsim.csv', index=False)

class Disk:
    def __init__(self, size):
        self.size = size
        self.blocks = [{'status': 0, 'file_name': 'filesimsim.csv', 'file_size': 486} for _ in range(size)]  # Initialize disk blocks with file name and size

class FileAllocationSimulator:
    def __init__(self, disk_size):
        self.disk = Disk(disk_size)
        self.files = {}

    # Contiguous Allocation Functions
    def contiguous_allocate(self, file_name, file_size):
        for i in range(self.disk.size):
            if self.disk.blocks[i]['status'] == 0:
                if i + file_size <= self.disk.size:
                    if all(block['status'] == 0 for block in self.disk.blocks[i:i+file_size]):
                        for j in range(i, i + file_size):
                            self.disk.blocks[j]['status'] = 1
                            self.disk.blocks[j]['file_name'] = file_name
                            self.disk.blocks[j]['file_size'] = file_size
                        self.files[file_name] = (i, file_size)
                        return True
        return False

    def contiguous_deallocate(self, file_name):
        if file_name in self.files:
            start_block, file_size = self.files[file_name]
            for i in range(start_block, start_block + file_size):
                self.disk.blocks[i]['status'] = 0
                self.disk.blocks[i]['file_name'] = None
                self.disk.blocks[i]['file_size'] = None
            del self.files[file_name]
            return True
        return False

    def contiguous_create(self, file_name, file_size):
        if file_name not in self.files:
            if self.contiguous_allocate(file_name, file_size):
                return True
        return False

    def contiguous_delete(self, file_name):
        if file_name in self.files:
            if self.contiguous_deallocate(file_name):
                return True
        return False

    def contiguous_read(self, file_name):
        if file_name in self.files:
            start_block, file_size = self.files[file_name]
            data = []
            for i in range(start_block, start_block + file_size):
                data.append(self.disk.blocks[i]['file_name'])
            return data
        return None

    def contiguous_write(self, file_name, data):
        if file_name in self.files:
            start_block, file_size = self.files[file_name]
            if len(data) == file_size:
                for i in range(start_block, start_block + file_size):
                    self.disk.blocks[i]['file_name'] = data[i - start_block]
                return True
        return False

# PySimpleGUI window layout
layout = [
    [sg.Text("File Allocation Simulator")],
    [sg.Text("Choose Allocation Method:")],
    [sg.Button("Contiguous Allocation"), sg.Button("Linked Allocation"), sg.Button("Indexed Allocation")],
    [sg.Text("File Operations:")],
    [sg.InputText(key='-FILE_NAME-', size=(15,1)), sg.InputText(key='-FILE_SIZE-', size=(10,1)), sg.Button("Create File"), sg.Button("Delete File"), sg.Button("Read File"), sg.Button("Write File")],
    [sg.Text("Disk Layout:")],
    [sg.Canvas(size=(300, 50), key="canvas")],
    [sg.Button("Exit")]
]

# Create the PySimpleGUI window
window = sg.Window("File Allocation Simulator", layout, finalize=True)

# Create an instance of FileAllocationSimulator
simulator = FileAllocationSimulator(50)  # Adjust disk size as needed

# Function to update disk layout visualization
def update_visualization(canvas, disk_blocks):
    canvas_elem = canvas.TKCanvas
    if canvas_elem is not None:
        canvas_elem.delete("all")  # Clear the canvas
        block_size = 10  # Adjust block size as needed
        block_padding = 2  # Adjust padding between blocks as needed
        x = 10
        y = 10
        for block in disk_blocks:
            if block['status'] == 1:
                canvas_elem.create_rectangle(x, y, x + block_size, y + block_size, fill='red')
                canvas_elem.create_text(x + block_size // 2, y + block_size // 2, text=f"{block['file_name']} ({block['file_size']} bytes)", fill='white')
            else:
                canvas_elem.create_rectangle(x, y, x + block_size, y + block_size, fill='white')
            x += block_size + block_padding
            if x >= 290:  # Adjust this value based on canvas width
                x = 10
                y += block_size + block_padding

# Initial disk layout visualization
update_visualization(window["canvas"], simulator.disk.blocks)

# Event loop to handle GUI events
while True:
    event, values = window.read()

    # Exit the program if the window is closed or Exit button is clicked
    if event == sg.WINDOW_CLOSED or event == "Exit":
        break

    # Handle button clicks
    if event == "Contiguous Allocation":
        # Perform actions for contiguous allocation method
        pass
    elif event == "Linked Allocation":
        # Perform actions for linked allocation method
        pass
    elif event == "Indexed Allocation":
        # Perform actions for indexed allocation method
        pass
    elif event == "Create File":
        file_name = values['-FILE_NAME-']
        file_size = int(values['-FILE_SIZE-'])
        if simulator.contiguous_create(file_name, file_size):
            sg.popup(f"File '{file_name}' created successfully.")
            update_visualization(window["canvas"], simulator.disk.blocks)
        else:
            sg.popup("Failed to create file. Disk space not available.")
    elif event == "Delete File":
        file_name = values['-FILE_NAME-']
        if simulator.contiguous_delete(file_name):
            sg.popup(f"File '{file_name}' deleted successfully.")
            update_visualization(window["canvas"], simulator.disk.blocks)
        else:
            sg.popup(f"File '{file_name}' not found.")
    elif event == "Read File":
        # Perform file read operation
        pass
    elif event == "Write File":
        # Perform file write operation
        pass

# Close the PySimpleGUI window
window.close()
