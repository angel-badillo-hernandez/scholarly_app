# Scholarly App

## Overview

Scholarly is a Windows application designed to streamline the process of managing scholarships and academic awards for the Midwestern State University (MSU) Department of Computer Science. The app provides functionality for the scholarship committee to efficiently filter and evaluate student data, generate personalized scholarship award letters, and create polls for the selection of Outstanding Student Award candidates. It allows for easy importation of student application data from CSV files, and helps facilitate the approval process for scholarships and awards.

The primary user of Scholarly is the Chair of the MSU Computer Science Scholarship Committee. Scholarly does not include students or applicants as users, but instead focuses on helping the committee make decisions by simplifying data filtering, award letter generation, and voting processes. 

Scholarly is a self-contained system and does not rely on integration with other larger systems, offering a dedicated solution to MSU’s scholarship and award selection processes.

---

## **Technologies Used**  
- **Python 3.12**  
- **PyQt6**  
- **SQLite3**  
- **Google Forms API**
- **GMail API**
- **Google Auth API**

---

## Software Requirements Specification Document
[![Software Demo](https://github.com/user-attachments/assets/58d98cce-e682-4589-9a08-5de7458d7b1a)](/scholarly_app_srs.pdf)

---
## **Python Virtual Environment Setup**  

1. Download **Python 3.12** (easily available on the Microsoft Store).  
2. Navigate to the **scholarly_app** directory.  
3. Run the following command in PowerShell:  

   ```powershell
   python3.12 -m venv venv
   ```

4. To activate the virtual environment, use this command:  

   ```powershell
   venv\Scripts\Activate.ps1
   ```

5. To install the required packages, run:  

   ```powershell
   pip install -r requirements.txt
   ```

---

## **Opening and Closing the Python Virtual Environment**  

- To open the virtual environment, run this command in PowerShell:  

   ```powershell
   venv\Scripts\Activate.ps1
   ```

- To close the virtual environment, run this command in PowerShell:  

   ```powershell
   deactivate
   ```

---

## **Running Python Source Files**  

- To run the script, execute:  

   ```powershell
   python main.py
   ```

---

## **Turning the Project into a Distributable EXE with Included Dependencies**  

- Coming soon...

---

## **Resources**  

- [SQLite3 Documentation](https://docs.python.org/3/library/sqlite3.html)  
- [PyQt6 Documentation](https://pypi.org/project/PyQt6/)  
- [Google Forms API](https://developers.google.com/forms/api/quickstart/python)  

---

## **Video Demonstrations**  

### 1. **Project Presentation**  
[![Project Presentation](https://img.youtube.com/vi/rPxEUYlOVX0/0.jpg)](https://www.youtube.com/watch?v=rPxEUYlOVX0)

### 2. **Software Demo**  
[![Software Demo](https://img.youtube.com/vi/Z3uo21HEc4s/0.jpg)](https://www.youtube.com/watch?v=Z3uo21HEc4s)
