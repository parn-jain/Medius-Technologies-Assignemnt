# Django File Upload and Email Summary

## Overview

This Django application allows users to upload Excel or CSV files, generate a summary report from the uploaded data, and send this summary via email.

## Views and Functionality

1. **Home View (`home`)**
   - **Purpose**: Renders the home page with a file upload form.
   - **URL**: `/`
   - **Template**: `home.html`
   - **Context**: Initializes and passes an instance of `FileUploadForm`.

2. **File Upload View (`upload_file`)**
   - **Purpose**: Handles file uploads, processes the file (Excel or CSV), generates a summary, and stores it in the session.
   - **URL**: `/upload/`
   - **Template**: `uploads.html`
   - **Context**:
     - `success`: Indicates successful upload and email status.
     - `error`: Provides error messages (e.g., unsupported file type or invalid form).
     - `summary`: Displays the generated summary.
   - **Processing**:
     - Checks file type and reads the content using Pandas.
     - Calls `generate_summary` to create an HTML summary table.
     - Stores the summary in the session for use in the email view.

3. **Summary Generation (`generate_summary`)**
   - **Purpose**: Groups data by state and pin code, then generates an HTML summary table.
   - **Parameters**: `data` (Pandas DataFrame)
   - **Returns**: HTML string of the summary table.

4. **Send Summary Email (`send_summary_email`)**
   - **Purpose**: Sends an email with the summary report attached.
   - **URL**: `/send-email/`
   - **Context**:
     - Retrieves the summary from the session.
     - Constructs an email with the summary.
   - **Email Configuration**:
     - SMTP server: `smtp.gmail.com`
     - Port: 587
     - Sender email: `pjisvgreat@gmail.com`
     - Receiver email: `tech@themedius.ai`
     - CC email: `yash@themedius.ai`
     - Subject: `'Python Assignment - Parn Jain 9399374451'`
   - **Process**:
     - Connects to the SMTP server and sends the email.
     - Handles exceptions and prints error messages if email sending fails.

## Environment Variables

- **EMAIL_PASSWORD**: The password for the email account used to send the email. It is retrieved from environment variables.

## Forms

- **FileUploadForm**: A Django form used to handle file uploads.

## Error Handling

- Errors are handled by checking file validity, form validity, and email sending exceptions. Appropriate messages are provided to users through the context.
