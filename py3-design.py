import sys
import os
import msvcrt  # Windows file locking
import time
import traceback
from bs4 import BeautifulSoup
from datetime import datetime
sys.stdout.reconfigure(encoding="utf-8")

# HTML file names
HTML_FILE_DEV = "database.html"
HTML_FILE_DES = "database-design.html"

# Define table headers
HEADERS = ["S.no", "DESCRIPTION", "URL", "RELEVANT_LINKS", "EMAILS", "TITLE", "APPLICATION", "TEMPLATE", "SOURCES", "COMMON_NAME_PART", "DOMAIN_PARTS", "MATCHING_LOGS", "TIME"]  # Removed "DATE"

# Define the templates
TEMPLATE_DEV = """
<div style="font-size: medium; margin-bottom: 20px; padding: 15px; border-radius: 8px; background-color: #333333; color: #ffffff; font-family: Arial, sans-serif;">
  <p>Hello {common_name_part}, I saw your job gig listed on Upwork regarding how you wanted to {title}. I'm Saif Anees, a professional website developer. I develop websites for Upwork clients and industry-leading experts that are as premium as their brand. {application} I will not only {title} for you. I also have some great ideas for enhancement of your website and I'd love to share them with you. If you're interested in getting your work done, let me know.</p>
</div>
<div style="margin-bottom: 20px; padding: 15px; border-radius: 8px; background-color: #333333; font-family: Arial, sans-serif;">
  <h2 style="color: #ffffff; margin: 0px;">
    <span style="font-size: 12pt;">Portfolio:</span>
    <a href="https://saifanees.vercel.app/" rel="noopener" target="_blank" style="font-size: medium; font-weight: normal; color: #00bfff; text-decoration-line: none;">https://saifanees.vercel.app/</a>
    <br>
  </h2>
  <br>
  <h2 style="color: #ffffff; margin: 0px;">
    <span style="font-size: large;">
      <span style="font-size: 14pt;">Most Recent Works</span>
      <br>
    </span>
  </h2>
  <p style="color: #ffffff; font-size: medium;">
    <strong>MS Real Estate Redesign</strong>
  </p>
  <p style="font-size: medium;">
    <span style="color: #ffffff;">I redesigned the MS Real Estate website to modernize its look and user experience. The aim was to create a visually appealing website that sets it apart from competitors. The project modernized design, integrated Property Finder XML for listings, added advanced search filters, property comparison, agent profiles, WhatsApp contact, and responsive design. It balanced aesthetics with usability, overcoming outdated systems to deliver a user-focused, functional solution. 
      <br>
    </span> 
    <a href="https://www.msrealestate.ae/" rel="noopener" target="_blank" style="color: #00bfff; text-decoration-line: none;">https://www.msrealestate.ae/</a>
  </p>
  <span style="color: #ffffff; font-size: medium;">
    <img class="gmail-CToWUd gmail-a6T" style="cursor: pointer; outline: 0px; margin-right: 25px;" tabindex="0" src="https://ci3.googleusercontent.com/meips/ADKq_NbKZbHEbqy1wNVeetmzjy1RhuB2DdeLjl8I1veybTkD45tJGziZ_BJKSrTRvdfM5rIT0i41o3tHn0PPMbeRT_8XVvVBEnc2G5NxneKqCp0FfWsEQDZfn2ccKh58d1FlQCmgGw=s0-d-e1-ft#https://saif-anees.vercel.app/_next/image?url=%2Fmsre%2Fcover.png&amp;w=1920&amp;q=75" width="464" height="348">
  </span> 
  <br>
  <strong style="color: #ffffff; font-size: medium;">
    <br>Ohghad - Fundraiser Web Design &amp; Development 
    <br>
  </strong>
  <p style="color: #ffffff; font-size: medium;">I designed &amp; developed a donation website for "Oh Ghad," a non-profit organization dedicated to boosting Ghana's economy through the construction of amusement parks and recreational facilities. This project involved designing a user-friendly, secure, and visually appealing platform to facilitate donations and raise awareness about the organization's mission. 
    <br>
    <a href="https://ohghad.org/" rel="noopener" target="_blank" style="color: #00bfff; text-decoration-line: none;">https://ohghad.org/</a>
  </p>
  <span style="color: #ffffff; font-size: medium;">
    <img class="gmail-CToWUd gmail-a6T" style="cursor: pointer; outline: 0px;" tabindex="0" src="https://ci3.googleusercontent.com/meips/ADKq_NaqGwVmi0lB6ZbjJzqMKmzcrcasEqljup7Z53RpeiKdd1Y8L8Rxey7e4_nz_RdkzXefn3-l=s0-d-e1-ft#https://i.imgur.com/PFdz9Gg.png" alt="image.png" width="472" height="354">
  </span> 
  <br>
  <strong style="color: #ffffff; font-size: medium;">
    <br>Luxury Booking Site
  </strong>
  <p style="color: #ffffff; font-size: medium;">I transformed the website from an outdated yellow theme to a modern blue, black, and white scheme, redesigned it to align with the client's brand, and sourced all necessary content and images. The project included detailed UI/UX design with animations, a robust CRUD system for car listings management, a functional contact form, and secure admin authentication. The final result is a modern, luxurious website with engaging features and seamless management capabilities. 
    <br>
    <a href="https://modernstandards.ae/" rel="noopener" target="_blank" style="color: #00bfff; text-decoration-line: none;">https://modernstandards.ae</a> 
    <br>
  </p>
  <span style="color: #ffffff; outline-color: initial; outline-style: initial;">
    <img class="gmail-CToWUd gmail-a6T" style="cursor: pointer; outline: 0px; box-sizing: border-box; border-width: 0px; border-style: solid; display: block; vertical-align: middle; object-fit: cover; opacity: 1; font-family: ClashGrotesk-Variable, sans-serif; font-size: medium; color: transparent; margin-right: 25px;" tabindex="0" src="https://ci3.googleusercontent.com/meips/ADKq_NZa_8XkJ1SDMWBpHTb6AeoOJF0R6rSEwdlsj3-Q-88wQz-JfJGDS5CsS_4GpLBzZUVT1mWP=s0-d-e1-ft#https://i.imgur.com/EYro8kd.png" alt="image.png" width="472" height="354">
  </span> 
  <br>
  <strong style="color: #ffffff; font-size: medium;">
    <br>Noble Soft Agency 
    <br>
  </strong>
  <p style="color: #ffffff; font-size: medium;">Noblesoft showcases IT solutions, consulting expertise, and successful projects with a professional, responsive design.&nbsp; The website showcases high performance with fast loading speeds, leveraging Vercel for reliable deployment. Built with a modern framework like Next.js, it ensures server-side rendering and smooth navigation. The design is minimalist and professional, delivering a user-centric experience with full responsiveness across all devices. Basic SEO practices are implemented to enhance discoverability, making it both visually appealing and functional for users. 
    <br>
    <a href="https://noblesoft.vercel.app/" rel="noopener" target="_blank" style="color: #00bfff; text-decoration-line: none;">https://noblesoft.vercel.app/</a>
  </p>
  <span style="color: #ffffff; outline-color: initial; outline-style: initial;">
    <img class="gmail-CToWUd gmail-a6T" style="cursor: pointer; outline: 0px; box-sizing: border-box; border-width: 0px; border-style: solid; display: block; vertical-align: middle; object-fit: cover; opacity: 1; font-family: ClashGrotesk-Variable, sans-serif; font-size: medium; color: transparent; margin-right: 25px;" tabindex="0" src="https://saifanees.vercel.app/_next/image?url=%2Fnew%2Fnoblesoft.jpg&amp;w=2048&amp;q=75" width="472" height="354">
  </span>
</div>
"""

TEMPLATE = """
Hello {common_name_part}, I saw your job gig listed on Upwork regarding how you wanted to {title}. I'm Saif Anees. {application} I will not only {title} for you. I also have some great ideas for enhancement of your project and I'd love to share them with you. If you're interested in getting your work done, let me know.
"""

def acquire_file_lock(file_path, max_wait_time=120):
    """
    Attempts to acquire a lock on the file for exclusive access.
    Will retry for up to max_wait_time seconds (default 2 minutes).
    
    Returns file handle if successful, None if timed out.
    """
    start_time = time.time()
    
    # Create file if it doesn't exist
    if not os.path.exists(file_path):
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                pass  # Just create an empty file
        except Exception as e:
            print(f"Error creating file: {e}")
            return None
    
    while time.time() - start_time < max_wait_time:
        try:
            file_handle = open(file_path, "r+b")  # Open for read and write in binary mode
            msvcrt.locking(file_handle.fileno(), msvcrt.LK_NBLCK, 1)  # Try to lock the first byte
            return file_handle
        except IOError:  # Lock could not be acquired
            print(f"File {file_path} is locked by another process. Waiting 10 seconds...")
            time.sleep(10)
            continue
    
    print(f"Timed out after {max_wait_time} seconds waiting for file lock.")
    return None

def release_file_lock(file_handle):
    """Releases the lock on the file."""
    if file_handle:
        try:
            msvcrt.locking(file_handle.fileno(), msvcrt.LK_UNLCK, 1)  # Unlock
            file_handle.close()
        except Exception as e:
            print(f"Error releasing file lock: {e}")

def initialize_html(html_file):
    """Creates an HTML file with a table if it doesn't exist."""
    if not os.path.exists(html_file):
        file_handle = None
        try:
            file_handle = acquire_file_lock(html_file)
            if file_handle:
                # Need to reopen in text mode for writing HTML
                file_handle.close()
                with open(html_file, "w", encoding="utf-8") as f:
                    f.write(f"""
                    <html>
                    <head>
                        <title>Database</title>
                        <style>
                            table {{ width: 100%; border-collapse: collapse; }}
                            th, td {{ border: 1px solid black; padding: 8px; text-align: left; }}
                            th {{ background-color: #f2f2f2; }}
                        </style>
                    </head>
                    <body>
                        <h2>Database Records</h2>
                        <table>
                            <tr>{"".join(f"<th>{header}</th>" for header in HEADERS)}</tr>
                        </table>
                    </body>
                    </html>
                    """)
        except Exception as e:
            print(f"Error initializing HTML file: {e}")
            traceback.print_exc()
        finally:
            if file_handle and not file_handle.closed:
                release_file_lock(file_handle)

def get_next_sno(html_file):
    """Fetches the next serial number based on the existing rows."""
    file_handle = None
    try:
        file_handle = acquire_file_lock(html_file)
        if not file_handle:
            return 1  # Default if can't access file
        
        # Reopen in text mode for reading
        file_handle.close()
        with open(html_file, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
        
        table = soup.find("table")
        if not table:
            return 1
        
        rows = table.find_all("tr")[1:]  # Exclude header row
        return len(rows) + 1  # Next S.No (count existing rows + 1)
    
    except Exception as e:
        print(f"Error getting next serial number: {e}")
        traceback.print_exc()
        return 1  # Default if error
    
    finally:
        if file_handle and not file_handle.closed:
            release_file_lock(file_handle)

def get_current_time():
    """Returns the current date and time in YYYY-MM-DD HH:MM AM/PM format."""
    return datetime.now().strftime("%Y-%m-%d %I:%M %p")

def update_table(html_file, field, value, row_number=None, env=None):
    """Updates the HTML table based on the given field and value."""
    file_handle = None
    try:
        file_handle = acquire_file_lock(html_file)
        if not file_handle:
            print("Failed to acquire file lock for updating table.")
            return
        
        # Reopen in text mode for reading
        file_handle.close()
        file_handle = None
        
        # Read the HTML file
        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Check if file is empty or corrupt
        if not content.strip():
            print(f"HTML file {html_file} is empty. Reinitializing...")
            initialize_html(html_file)
            with open(html_file, "r", encoding="utf-8") as f:
                content = f.read()
        
        soup = BeautifulSoup(content, "html.parser")
        
        table = soup.find("table")
        if table is None:
            print(f"Table not found in {html_file}. Reinitializing...")
            initialize_html(html_file)
            with open(html_file, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "html.parser")
            table = soup.find("table")
            
            if table is None:
                print("Failed to find or create table element.")
                return
        
        rows = table.find_all("tr")
        
        if field == "DESCRIPTION":
            # Create new row with next S.No
            new_row = soup.new_tag("tr")
            
            for index, header in enumerate(HEADERS):
                td = soup.new_tag("td")
                if header == "S.no":
                    td.string = str(get_next_sno(html_file))  # Auto-increment S.No
                elif header == "DESCRIPTION":
                    td.string = value  # Set description
                elif header == "TIME":
                    td.string = get_current_time()  # Set current date and time
                new_row.append(td)
            
            table.append(new_row)
        
        else:
            # Update specified row or latest row
            if row_number is None:
                row_number = len(rows) - 1  # Default to the latest row
            
            if row_number > len(rows):
                print(f"Row number {row_number} does not exist.")
                return
            
            if row_number > 0 and row_number < len(rows):
                target_row = rows[row_number]
                cells = target_row.find_all("td")
                
                if field in HEADERS:
                    index = HEADERS.index(field)
                    cells[index].string = value  # Update the corresponding column
                
                # If the TITLE field is updated, fill the template using the same row's fields
                if field == "TITLE":
                    common_name_part = cells[9].get_text(strip=True)  # "COMMON_NAME_PART" column
                    application = cells[6].get_text(strip=True)  # "APPLICATION" column
                    template_filled = fill_template(common_name_part, value, application, env)
                    cells[7].string = template_filled  # Update the "TEMPLATE" column
        
        # Acquire lock again for writing
        file_handle = acquire_file_lock(html_file)
        if not file_handle:
            print("Failed to acquire file lock for writing updated table.")
            return
        
        # Reopen in text mode for writing
        file_handle.close()
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(str(soup.prettify()))
    
    except Exception as e:
        print(f"Error updating table: {e}")
        traceback.print_exc()
    
    finally:
        if file_handle and not file_handle.closed:
            release_file_lock(file_handle)

def get_latest_row_data(html_file):
    """Fetches the latest row's data for common_name_part and application."""
    file_handle = None
    try:
        file_handle = acquire_file_lock(html_file)
        if not file_handle:
            return "", ""  # Default if can't access file
        
        # Reopen in text mode for reading
        file_handle.close()
        with open(html_file, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
        
        table = soup.find("table")
        if not table:
            return "", ""
        
        rows = table.find_all("tr")
        
        if len(rows) > 1:
            latest_row = rows[-1]
            cells = latest_row.find_all("td")
            
            common_name_part = cells[9].get_text(strip=True)  # "COMMON_NAME_PART" column
            application = cells[6].get_text(strip=True)  # "APPLICATION" column
            
            return common_name_part, application
        return "", ""  # Default empty values if no rows exist
    
    except Exception as e:
        print(f"Error getting latest row data: {e}")
        traceback.print_exc()
        return "", ""  # Default if error
    
    finally:
        if file_handle and not file_handle.closed:
            release_file_lock(file_handle)

def fill_template(common_name_part, title, application, env):
    """Fills the template with provided values."""
    if env == "dev":
        return TEMPLATE_DEV.format(common_name_part=common_name_part, title=title, application=application)
    else:
        return TEMPLATE.format(common_name_part=common_name_part, title=title, application=application)

def safe_file_operation(func, *args, **kwargs):
    """Wrapper to handle exceptions and ensure proper file cleanup"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        print(f"Error in {func.__name__}: {e}")
        traceback.print_exc()
        return None

def main():
    """Parses command-line arguments and updates the database."""
    try:
        if len(sys.argv) < 4:
            print("Usage: python py3.py [dev/des] [ROW_NUMBER] FIELD_NAME [VALUE]")
            return
        
        env = sys.argv[1].lower()
        if env not in ["dev", "des"]:
            print("Invalid environment. Use 'dev' or 'des'.")
            return
        
        html_file = HTML_FILE_DEV if env == "dev" else HTML_FILE_DES
        
        if sys.argv[2].isdigit():
            row_number = int(sys.argv[2])
            field = sys.argv[3].upper()
            value = " ".join(sys.argv[4:]) if len(sys.argv) > 4 else ""  # Empty if no value given
        else:
            row_number = None
            field = sys.argv[2].upper()
            value = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else ""  # Empty if no value given
        
        if field not in HEADERS:
            print(f"Invalid field: {field}")
            return
        
        # Initialize HTML file if it doesn't exist
        safe_file_operation(initialize_html, html_file)
        
        # Update table
        safe_file_operation(update_table, html_file, field, value, row_number, env)
        
        # Handle TITLE field special case
        if field == "TITLE":
            file_handle = None
            try:
                file_handle = acquire_file_lock(html_file)
                if file_handle:
                    # Reopen in text mode for reading
                    file_handle.close()
                    file_handle = None
                    
                    with open(html_file, "r", encoding="utf-8") as f:
                        soup = BeautifulSoup(f, "html.parser")
                    
                    table = soup.find("table")
                    rows = table.find_all("tr")
                    
                    if row_number > 0 and row_number < len(rows):
                        target_row = rows[row_number]
                        cells = target_row.find_all("td")
                        common_name_part = cells[9].get_text(strip=True)  # "COMMON_NAME_PART" column
                        application = cells[6].get_text(strip=True)  # "APPLICATION" column
                        template_filled = fill_template(common_name_part, value, application, env)
                        
                        safe_file_operation(update_table, html_file, "TEMPLATE", template_filled, row_number, env)
                        print(f"{template_filled}")
            except Exception as e:
                print(f"Error handling TITLE field: {e}")
                traceback.print_exc()
            finally:
                if file_handle and not file_handle.closed:
                    release_file_lock(file_handle)
        
        elif field == "DESCRIPTION":
            row_number = safe_file_operation(get_next_sno, html_file) - 1  # Get the current row number
            print(f"{row_number}")
        
        elif field == "EMAILS":
            print(f"{value}")
        
        else:
            print(f"Updated {field} with: {value if value else '(empty)'} at row {row_number if row_number is not None else 'latest'}")
    
    except Exception as e:
        print(f"Unexpected error in main function: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()