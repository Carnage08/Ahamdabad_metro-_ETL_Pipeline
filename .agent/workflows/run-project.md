---
description: Run the Ahmedabad Metro Scraper project
---

To execute the project, follow these steps:

1. **Active the environment**:
   ```bash
   source venv/bin/activate
   ```

2. **Run the main scraper**:
   ```bash
   python main.py
   ```

3. **Verify the results**:
   Check the database count:
   ```bash
   python check_db_completeness.py
   ```

4. **Export to CSV**:
   ```bash
   python export_to_csv.py
   ```
