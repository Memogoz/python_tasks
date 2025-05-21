# Python Tasks

This repository contains several Python scripts for various tasks. Below are the instructions for running each script.

---

## Task 1

### 1. File Extension (`1_FileExtension.py`)
This script extracts the file extension from a given filename.

**Usage:**
```bash
./1_FileExtension.py <filename>
```

**Example:**
```bash
./1_FileExtension.py example.txt
```

---

### 2. Remove Duplicates (`2_RemoveDuplicates.py`)
This script removes duplicates from a list, creates a tuple, and finds the minimum and maximum values.

**Usage:**
```bash
./2_RemoveDuplicates.py "[<list>]"
```

**Example:**
```bash
./2_RemoveDuplicates.py "[1, 2, 2, 3, 4, 4, 5]"
```

---

### 3. Log Analysis (`3_LogAnalisis.py`)
This script analyzes a log file and provides statistics on User Agents.

**Usage:**
```bash
./3_LogAnalisis.py <filename>
```

**Example:**
```bash
./3_LogAnalisis.py access.log.5
```

---

### 4. Character Count (`4_CharCount.py`)
This script counts the number of characters in a given string.

**Usage:**
```bash
./4_CharCount.py <string>
```

**Example:**
```bash
./4_CharCount.py "hello world"
```

---

### 5. System Info (`5_SysInfo.py`)
This script retrieves system information from a Linux system.

**Usage:**
```bash
./5_SysInfo.py [options]
```

**Options:**
- `-d`, `--distro`: Get Linux distribution information.
- `-m`, `--memory`: Get memory information.
- `-c`, `--cpu`: Get CPU information.
- `-u`, `--user`: Get user information.
- `-l`, `--load`: Get load average.
- `-i`, `--ip`: Get IP address.

**Example:**
```bash
./5_SysInfo.py -d -m -c
```

---

## Task 2

### Send Survey (`sendsurvey.py`)
This script creates and sends a survey to a list of emails using the SurveyMonkey API.

**Prerequisites:**
1. Install dependencies:
   ```bash
   pip install python-dotenv requests
   ```
2. Set the `TOKEN` environment variable in a `.env` file:
   ```
   TOKEN=<your_surveymonkey_api_token>
   ```

**Usage:**
```bash
./sendsurvey.py <questions.json> <emails.txt>
```

**Example:**
```bash
./sendsurvey.py questions.json emails.txt
```
---

## Advanced task

### Pizzeria Web Server and client CLI 
The command-line tool allows you to interact with the Pizza Ordering API server. You can view the menu, place orders, check order status, and perform admin operations such as managing the menu and orders.

Aditional information can be found inside the `/Advanced Task` folder.

---

## General Notes
- Ensure all scripts have executable permissions:
  ```bash
  chmod +x <script_name>.py
  ```
- Run the scripts using Python 3.
- For Task 2, ensure you have a valid SurveyMonkey API token and internet access.

---