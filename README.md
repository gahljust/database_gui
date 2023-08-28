
# ShowerMax Data Manager

The ShowerMax Data Manager is a user-friendly GUI for managing data in the ShowerMax database. With this manager, users can view table data, dynamically generate entry fields based on table structure, add new data, and visualize data attributes using histograms.

## Features

- **Dynamic Table Selection**: Select any table from the database and view its data.
- **Dynamic Entry Fields**: Based on the table selected, generate entry fields to allow data insertion.
- **Data Insertion**: Add new data entries to the selected table.
- **Data Visualization**: Select an attribute/column and visualize its distribution using histograms.

## Installation

### Prerequisites

Ensure you have Python (3.6 or later) installed on your system. You can check using:

```bash
python --version
```

or 

```bash
python3 --version
```

### Required Packages

The ShowerMax Data Manager requires the following Python packages:

- `tkinter`
- `sqlite3`
- `pandas`
- `matplotlib`

### Installing Required Packages

#### For all Operating Systems

You can install all required packages using `pip`. Run the following command:

```bash
pip install pandas matplotlib
```

Note: `tkinter` and `sqlite3` are part of the Python standard library and do not need separate installation.

### Mac, Windows, and Linux

1. **Clone the Repository**

   First, clone the ShowerMax Data Manager repository to your local machine:

   ```bash
   git clone [URL of your GitHub repository]
   ```

2. **Navigate to the Project Directory**

   ```bash
   cd path_to_directory/ShowerMaxDataManager
   ```

3. **Run the GUI**

   ```bash
   python showermax_gui.py
   ```

   or

   ```bash
   python3 showermax_gui.py
   ```

## Usage

1. **Select a Table**: Use the dropdown menu to select a table. The table data will be displayed in a new window.

2. **Add Data to the Table**: Below the table dropdown, the GUI will generate entry fields corresponding to the columns of the selected table. Fill in the data and click "Add Entry" to insert the data into the database.

3. **Visualize Data**: Use the "Select Attribute to Plot" dropdown to select an attribute/column from the table. Click "Plot Histogram" to visualize the distribution of the selected attribute.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

Make sure to replace `[URL of your GitHub repository]` with the actual URL of your GitHub repository. And adjust the folder name `ShowerMaxDataManager` in the `cd` command if you have a different directory structure or repository name.
