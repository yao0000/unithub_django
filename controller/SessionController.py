import json
import time
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sql.DAL.DraftDAL import Draft
from selenium.common.exceptions import TimeoutException, WebDriverException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Log to console
        logging.FileHandler('reserve_requests.log')  # Log to file
    ]
)
logger = logging.getLogger(__name__)

@csrf_exempt
def run_reserve(request):
    if request.method == "POST":
        try:
            # Extract draft_guid and retry_minutes from POST
            draft_guid = request.POST.get('draft_guid')
            retry_minutes = request.POST.get('retry_minutes', '5')

            # Log the received POST data
            logger.info(f"Received POST data: draft_guid='{draft_guid}', retry_minutes='{retry_minutes}'")
            logger.info(f"Full POST data: {dict(request.POST)}")

            # Prepare received data for response
            received_data = {
                "draft_guid": draft_guid,
                "retry_minutes": retry_minutes,
                "full_post_data": dict(request.POST)
            }

            # Validate inputs
            if not draft_guid:
                logger.error("Missing draft_guid")
                return JsonResponse({
                    "status": "error",
                    "message": "Missing draft_guid",
                    "received_data": received_data
                }, status=400)

            try:
                retry_minutes_float = float(retry_minutes)
                if retry_minutes_float <= 0:
                    logger.error(f"Invalid retry_minutes: {retry_minutes}")
                    return JsonResponse({
                        "status": "error",
                        "message": "Retry minutes must be positive",
                        "received_data": received_data
                    }, status=400)
            except ValueError:
                logger.error(f"Invalid retry_minutes format: '{retry_minutes}'")
                return JsonResponse({
                    "status": "error",
                    "message": f"Invalid retry minutes format: '{retry_minutes}'",
                    "received_data": received_data
                }, status=400)

            # Retrieve draft details
            logger.info(f"Retrieving draft details for draft_guid: {draft_guid}")
            try:
                draft_result = Draft.get_draft_details(draft_guid)
                logger.info(f"Draft result: {draft_result}")
            except Exception as e:
                logger.error(f"Failed to retrieve draft details: {str(e)}")
                return JsonResponse({
                    "status": "error",
                    "message": f"Failed to retrieve draft details: {str(e)}",
                    "received_data": received_data
                }, status=500)

            # Extract draft_details
            try:
                if isinstance(draft_result, JsonResponse):
                    draft_result = json.loads(draft_result.content.decode('utf-8'))
                if not isinstance(draft_result, dict):
                    raise ValueError(f"Expected dictionary, got {type(draft_result)}")
                draft_details_list = draft_result.get('data', [])
                if not draft_details_list:
                    logger.error(f"No draft found for draft_guid: {draft_guid}")
                    return JsonResponse({
                        "status": "error",
                        "message": f"No draft found for draft_guid: {draft_guid}",
                        "received_data": received_data
                    }, status=404)
                draft_details = draft_details_list[0]
                if not isinstance(draft_details, dict):
                    raise ValueError(f"Expected dictionary for draft details, got {type(draft_details)}")
            except Exception as e:
                logger.error(f"Failed to parse draft details: {str(e)}")
                return JsonResponse({
                    "status": "error",
                    "message": f"Invalid draft details format: {str(e)}",
                    "received_data": received_data
                }, status=500)

            # Validate draft fields
            required_fields = [
                'MhubEmail', 'MhubPassword', 'ProjectName', 'BlockName', 'UnitName',
                'IdentityType', 'IdentityNumber', 'Title', 'FullName', 'PreferredName',
                'ClientEmail', 'Mobile', 'Address', 'PostCode', 'City', 'State',
                'FirstTime', 'PaymentDate', 'AgencyCmp', 'AgentName', 'AgentPhone', 'Remarks'
            ]
            missing_fields = [field for field in required_fields if field not in draft_details or draft_details[field] is None or draft_details[field] == '']
            if missing_fields:
                logger.error(f"Missing or empty draft fields: {', '.join(missing_fields)}")
                return JsonResponse({
                    "status": "error",
                    "message": f"Missing or empty required draft fields: {', '.join(missing_fields)}",
                    "received_data": received_data
                }, status=400)

            # Assign draft data
            email = draft_details['MhubEmail']
            password = draft_details['MhubPassword']
            project_name = draft_details['ProjectName']
            block_name = draft_details['BlockName']
            unit_name = draft_details['UnitName']
            identity_type = draft_details['IdentityType']
            identity_number = draft_details['IdentityNumber']
            title = draft_details['Title']
            full_name = draft_details['FullName']
            preferred_name = draft_details['PreferredName']
            client_email = draft_details['ClientEmail']
            mobile = draft_details['Mobile']
            address = draft_details['Address']
            postcode = draft_details['PostCode']
            city = draft_details['City']
            state = draft_details['State']
            first_time = 'Yes' if draft_details['FirstTime'] == 'Y' else 'No'
            payment_date = draft_details['PaymentDate']
            agency_cmp = draft_details['AgencyCmp']
            agent_name = draft_details['AgentName']
            agent_phone = draft_details['AgentPhone']
            remarks = draft_details['Remarks']

            # Log draft data
            logger.info(f"Parsed draft data: email='{email}', project_name='{project_name}', block_name='{block_name}', unit_name='{unit_name}'")

            # Set up Selenium WebDriver
            logger.info("Initializing Selenium WebDriver")
            options = webdriver.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            try:
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=options)
            except Exception as e:
                logger.error(f"Failed to initialize WebDriver: {str(e)}")
                return JsonResponse({
                    "status": "error",
                    "message": f"Failed to initialize WebDriver: {str(e)}",
                    "received_data": received_data
                }, status=500)

            try:
                # Start timing for the entire process
                time_limit = retry_minutes_float * 60  # Convert to seconds
                start_time = time.time()
                wait = WebDriverWait(driver, 3)

                def is_browser_open(driver):
                    """Check if the browser is still open by attempting to access the page title."""
                    try:
                        _ = driver.title  # Attempt to access the page title
                        return True
                    except WebDriverException as e:
                        logger.error(f"Browser window is closed: {str(e)}")
                        return False

                # Define a custom exception for browser closure
                class BrowserClosedException(Exception):
                    pass

                def retry_action(action_name, action_func, error_message, status_code=400, refresh_on_fail=True):
                    """Reusable function to retry an action within the global time limit with immediate refresh on 'No projects found'."""
                    while (time.time() - start_time) < time_limit:
                        try:
                            result = action_func()
                            return result if result else True  # Return result if provided, else True
                        except Exception as e:
                            # Check if the browser is still open before proceeding
                            if not is_browser_open(driver):
                                raise BrowserClosedException("Browser window was closed, terminating process")

                            # CHANGE: Added "Unit not found in results" to the condition to trigger refresh
                            if "No projects found" in str(e) or "Project not found in results" in str(e) or "Unit not found in results" in str(e):
                                logger.warning(f"{action_name} encountered '{str(e)}', retrying until time limit")
                                if refresh_on_fail:
                                    if not is_browser_open(driver):
                                        raise BrowserClosedException("Browser window was closed, terminating process")
                                    try:
                                        driver.refresh()
                                        time.sleep(2)  # Post-refresh delay
                                    except:
                                        logger.warning("Failed to refresh page, continuing")
                                time.sleep(0.5)  # Retry delay
                                continue
                            # Handle other failures
                            if (time.time() - start_time) >= time_limit:
                                logger.error(f"{action_name} failed after time limit: {str(e)}")
                                try:
                                    if "Available" in error_message:
                                        elements = driver.find_elements(By.XPATH, action_func.fallback_xpath)
                                        logger.info(f"{error_message.split(':')[0]}: {[el.text for el in elements]}")
                                except:
                                    logger.info(f"No elements found for {action_name}")
                                return JsonResponse({
                                    "status": "error",
                                    "message": f"{error_message}: {str(e)}",
                                    "received_data": received_data
                                }, status=status_code)
                            logger.warning(f"{action_name} failed, retrying: {str(e)}")
                            if refresh_on_fail:
                                if not is_browser_open(driver):
                                    raise BrowserClosedException("Browser window was closed, terminating process")
                                try:
                                    driver.refresh()
                                    time.sleep(2)  # Post-refresh delay
                                except:
                                    logger.warning("Failed to refresh page, continuing")
                            time.sleep(0.5)  # Retry delay
                    logger.error(f"{action_name} failed after time limit")
                    return JsonResponse({
                        "status": "error",
                        "message": error_message,
                        "received_data": received_data
                    }, status=status_code)  
                # Navigate to login page
                driver.get("https://secure.mhub.my/login")
                time.sleep(2)
                driver.find_element(By.NAME, "email").send_keys(email)
                driver.find_element(By.NAME, "password").send_keys(password)
                driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)
                time.sleep(5)

                # Navigate to projects page
                driver.get("https://exs.mhub.my/projects/")
                time.sleep(3)

                # Project search with retry
                logger.info(f"Searching for project '{project_name}' with {retry_minutes_float} minutes total limit")
                def search_project():
                    search_box = driver.find_element(By.NAME, "search")
                    search_box.clear()
                    search_box.send_keys(project_name)
                    search_box.send_keys(Keys.RETURN)
                    # CHANGE: Reduced post-search delay from 1s to 0.5s
                    time.sleep(0.5)  # Reduced delay after search (message appears immediately)

                    # CHANGE: Added short_wait with 1s timeout for faster checks
                    short_wait = WebDriverWait(driver, 1)  # Short timeout for checks
                    try:
                        # Check for "No projects found" message
                        no_projects_xpath = "//div[@class='ui center aligned segment' and contains(text(), 'No projects found')]"
                        # CHANGE: Using short_wait (1s) instead of previous 2s timeout
                        no_projects_message = short_wait.until(EC.visibility_of_element_located((By.XPATH, no_projects_xpath)))
                        raise Exception(f"No projects found: '{no_projects_message.text}'")  # Trigger retry with refresh
                    except:
                        logger.info("No 'No projects found' message detected, checking project presence")

                    # CHANGE: Simplified project check to a single XPath with 1s timeout
                    # Removed the two-step XPath approach (original + fallback) to save time
                    try:
                        project_xpath = f"//a[contains(@href, '/projects/') and contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{project_name.lower()}')]"
                        first_result = short_wait.until(EC.visibility_of_element_located((By.XPATH, project_xpath)))
                        driver.execute_script("arguments[0].scrollIntoView();", first_result)
                        time.sleep(1)
                        first_result.click()
                        logger.info(f"Clicked project '{project_name}'")
                        # Verify navigation to project page
                        wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='ui horizontal divider' and text()='Layouts']")))
                        logger.info("Confirmed project page loaded")
                    except:
                        # CHANGE: Added new exception to trigger immediate refresh
                        raise Exception(f"Project not found in results")  # Trigger retry with refresh
                search_project.fallback_xpath = "//a[contains(@href, '/projects/')]"

                result = retry_action(
                    action_name=f"Project '{project_name}' search",
                    action_func=search_project,
                    error_message=f"Project '{project_name}' not found. Available projects",
                    status_code=400
                )
                if isinstance(result, JsonResponse):
                    return result
                time.sleep(3)

                # Scroll to "Layouts" section (optional, no retry needed)
                try:
                    divider = driver.find_element(By.XPATH, "//div[@class='ui horizontal divider' and text()='Layouts']")
                    driver.execute_script("arguments[0].scrollIntoView();", divider)
                    time.sleep(1)
                    logger.info("Found Layouts section")
                except Exception as e:
                    logger.warning(f"Layouts section not found, continuing: {str(e)}")

                # Find and select the block with retry
                logger.info(f"Searching for block '{block_name}'")
                def find_block():
                    block_div = wait.until(EC.presence_of_element_located((
                        By.XPATH,
                        f"//div[@class='ui header' and text()='{block_name}']"
                    )))
                    driver.execute_script("arguments[0].scrollIntoView();", block_div)
                    time.sleep(1)
                    logger.info(f"Found block '{block_name}'")
                    # Click "Reserve" button for the block
                    reserve_button = driver.find_element(By.XPATH,
                        f"//div[contains(@class, 'ui header') and text()='{block_name}']//following::button[contains(@class, 'button-reduce-spacing')]"
                    )
                    driver.execute_script("arguments[0].scrollIntoView();", reserve_button)
                    time.sleep(1)
                    try:
                        reserve_button.click()
                    except:
                        driver.execute_script("arguments[0].click();", reserve_button)
                    logger.info(f"Clicked Reserve button for block '{block_name}'")
                    time.sleep(3)  # Allow unit selection page to load
                    # Verify navigation to unit search page
                    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='search' and not(@disabled)]")))
                    logger.info("Confirmed unit search page loaded")
                find_block.fallback_xpath = "//div[@class='ui header']"

                result = retry_action(
                    action_name=f"Block '{block_name}' search and reserve",
                    action_func=find_block,
                    error_message=f"Block '{block_name}' or its reserve button not found. Available blocks",
                    status_code=400
                )
                if isinstance(result, JsonResponse):
                    return result

                # Search for the unit with retry
                logger.info(f"Current URL before unit search: {driver.current_url}")
                logger.info(f"Searching for unit '{unit_name}'")
                def search_unit():
                    unit_search_box = wait.until(EC.element_to_be_clickable((
                        By.XPATH,
                        "//input[@name='search' and not(@disabled)]"
                    )))
                    logger.info(f"Unit search input state: displayed={unit_search_box.is_displayed()}, enabled={unit_search_box.is_enabled()}, HTML={unit_search_box.get_attribute('outerHTML')}")
                    driver.execute_script("arguments[0].scrollIntoView();", unit_search_box)
                    time.sleep(1)  # Allow scrolling
                    unit_search_box.clear()
                    unit_search_box.send_keys(unit_name)
                    unit_search_box.send_keys(Keys.RETURN)
                    # CHANGE: Reduced post-search delay from 1s to 0.5s
                    time.sleep(0.5)  # Reduced delay after search (message appears immediately after Enter)

                    # CHANGE: Added short_wait with 1s timeout for faster checks
                    short_wait = WebDriverWait(driver, 1)  # Short timeout for checks
                    try:
                        # Check for "No projects found" message
                        no_units_xpath = "//div[@class='ui center aligned segment' and contains(text(), 'No projects found')]"
                        # CHANGE: Using short_wait (1s) instead of previous 2s timeout
                        no_units_message = short_wait.until(EC.visibility_of_element_located((By.XPATH, no_units_xpath)))
                        raise Exception(f"No projects found: '{no_units_message.text}'")  # Trigger retry with refresh
                    except:
                        logger.info("No 'No projects found' message detected, checking unit presence")

                    # CHANGE: Simplified unit check to a single XPath with 1s timeout
                    # Removed the three-step XPath approach to save time
                    try:
                        # Check unit availability
                        status_xpath = "//td[@class='two wide mobile-hide capitalize']"
                        try:
                            status_element = wait.until(EC.visibility_of_element_located((By.XPATH, status_xpath)))
                            status = status_element.text.strip().lower()
                            logger.info(f"Unit '{unit_name}' status: {status}")
                            if status == "unavailable":
                                logger.error(f"Unit '{unit_name}' is unavailable, terminating process")
                                return JsonResponse({
                                    "status": "error",
                                    "message": f"Unit '{unit_name}' is unavailable",
                                    "received_data": received_data
                                }, status=400)
                            elif status == "available":
                                logger.info(f"Unit '{unit_name}' is available, proceeding with reservation")
                            else:
                                logger.error(f"Unknown unit status '{status}' for unit '{unit_name}'")
                                return JsonResponse({
                                    "status": "error",
                                    "message": f"Unknown unit status '{status}' for unit '{unit_name}'",
                                    "received_data": received_data
                                }, status=400)
                        except Exception as e:
                            logger.error(f"Failed to determine unit status for '{unit_name}': {str(e)}")
                            return JsonResponse({
                                "status": "error",
                                "message": f"Failed to determine unit status for '{unit_name}': {str(e)}",
                                "received_data": received_data
                            }, status=400)

                        unit_xpath = f"//a[contains(@href, '/units/') and contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{unit_name.lower()}')]"
                        first_unit_result = short_wait.until(EC.visibility_of_element_located((By.XPATH, unit_xpath)))
                        driver.execute_script("arguments[0].scrollIntoView();", first_unit_result)
                        time.sleep(1)
                        first_unit_result.click()
                        logger.info(f"Clicked unit '{unit_name}'")
                        time.sleep(3)


                    except:
                        # CHANGE: Added new exception to trigger immediate refresh
                        raise Exception(f"Unit not found in results")  # Trigger retry with refresh
                search_unit.fallback_xpath = "//a[contains(@href, '/units/')]"

                result = retry_action(
                    action_name=f"Unit '{unit_name}' search",
                    action_func=search_unit,
                    error_message=f"Unit '{unit_name}' not found. Available units",
                    status_code=400
                )
                if isinstance(result, JsonResponse):
                    driver.save_screenshot('unit_search_failure.png')
                    logger.info("Saved screenshot: unit_search_failure.png")
                    return result

                # Click the "Reserve" button for the unit (only reached if unit is available)
                logger.info("Attempting to click unit reserve button")
                def click_unit_reserve():
                    reserve_button = wait.until(EC.element_to_be_clickable((
                        By.XPATH,
                        "//a[contains(@class, 'positive button') and contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'reserve')]"
                    )))
                    logger.info(f"Unit reserve button HTML: {reserve_button.get_attribute('outerHTML')}")
                    driver.execute_script("arguments[0].scrollIntoView();", reserve_button)
                    time.sleep(1)
                    try:
                        reserve_button.click()
                    except:
                        driver.execute_script("arguments[0].click();", reserve_button)
                    logger.info("Clicked Reserve button for unit")
                    time.sleep(3)  # Allow form page to load
                click_unit_reserve.fallback_xpath = "//a[contains(@class, 'button')]"

                result = retry_action(
                    action_name="Unit reserve button click",
                    action_func=click_unit_reserve,
                    error_message="Reserve button for unit not found. Available buttons",
                    status_code=400
                )
                if isinstance(result, JsonResponse):
                    return result

                # Select Identity Type
                logger.info(f"Selecting Identity Type: {identity_type}")
                def select_identity_type():
                    identity_dropdown = wait.until(EC.element_to_be_clickable((
                        By.XPATH,
                        "//div[@name='identityType' and contains(@class, 'dropdown')] | //select[@name='identityType'] | //input[@name='identityType']"
                    )))
                    logger.info(f"Identity dropdown HTML: {identity_dropdown.get_attribute('outerHTML')}")
                    driver.execute_script("arguments[0].scrollIntoView();", identity_dropdown)
                    time.sleep(1)
                    try:
                        identity_dropdown.click()
                    except:
                        driver.execute_script("arguments[0].click();", identity_dropdown)
                    time.sleep(1)
                    nric_option = wait.until(EC.element_to_be_clickable((
                        By.XPATH,
                        f"//div[@tin_code='{identity_type}' or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{identity_type.lower()}') or @value='{identity_type}' or contains(@data-value, '{identity_type}')]"
                    )))
                    driver.execute_script("arguments[0].scrollIntoView();", nric_option)
                    time.sleep(1)
                    try:
                        nric_option.click()
                    except:
                        driver.execute_script("arguments[0].click();", nric_option)
                    logger.info(f"Selected Identity Type: {identity_type}")
                select_identity_type.fallback_xpath = "//div[@role='option'] | //option | //div[contains(@class, 'menu')]//div"

                result = retry_action(
                    action_name=f"Identity Type '{identity_type}' selection",
                    action_func=select_identity_type,
                    error_message=f"Error selecting Identity Type '{identity_type}'. Available options",
                    status_code=400,
                    refresh_on_fail=False
                )
                if isinstance(result, JsonResponse):
                    return result

                # Fill in Identity Number
                logger.info("Entering Identity Number")
                def enter_identity_number():
                    identity_number_input = wait.until(EC.element_to_be_clickable((
                        By.XPATH,
                        "//input[@name='identity' and not(@disabled)]"
                    )))
                    logger.info(f"Identity input state: displayed={identity_number_input.is_displayed()}, enabled={identity_number_input.is_enabled()}")
                    driver.execute_script("arguments[0].scrollIntoView();", identity_number_input)
                    time.sleep(1)
                    identity_number_input.clear()
                    identity_number_input.send_keys(identity_number)
                    logger.info("Entered Identity Number")
                enter_identity_number.fallback_xpath = "//input[@name='identity']"

                result = retry_action(
                    action_name="Identity Number entry",
                    action_func=enter_identity_number,
                    error_message="Error entering Identity Number",
                    status_code=400,
                    refresh_on_fail=False
                )
                if isinstance(result, JsonResponse):
                    return result

                # Select Title
                logger.info(f"Selecting Title: {title}")
                def select_title():
                    title_dropdown = wait.until(EC.element_to_be_clickable((
                        By.XPATH,
                        "//label[contains(text(), 'Title')]//following::input[contains(@class, 'search')][1]"
                    )))
                    driver.execute_script("arguments[0].scrollIntoView();", title_dropdown)
                    time.sleep(1)
                    title_dropdown.click()
                    time.sleep(1)
                    title_dropdown.send_keys(title)
                    time.sleep(1)
                    title_dropdown.send_keys(Keys.RETURN)
                    logger.info(f"Selected Title: {title}")
                select_title.fallback_xpath = "//div[contains(@class, 'menu')]//div[@role='option']"

                result = retry_action(
                    action_name=f"Title '{title}' selection",
                    action_func=select_title,
                    error_message=f"Error selecting Title '{title}'. Available options",
                    status_code=400,
                    refresh_on_fail=False
                )
                if isinstance(result, JsonResponse):
                    return result

                # Fill in Buyer Details
                logger.info("Filling buyer details")
                def fill_buyer_details():
                    fields = [
                        ("name", full_name),
                        ("preferredName", preferred_name),
                        ("email", client_email),
                        ("mobile", mobile),
                        ("address1", address),
                        ("address6", city),
                        ("address5", postcode)
                    ]
                    for field_name, value in fields:
                        field = wait.until(EC.element_to_be_clickable((By.NAME, field_name)))
                        driver.execute_script("arguments[0].scrollIntoView();", field)
                        time.sleep(0.5)
                        field.clear()
                        field.send_keys(value)
                        logger.info(f"Filled field '{field_name}' with '{value}'")
                fill_buyer_details.fallback_xpath = "//input"

                result = retry_action(
                    action_name="Buyer details entry",
                    action_func=fill_buyer_details,
                    error_message="Error filling buyer details",
                    status_code=400,
                    refresh_on_fail=False
                )
                if isinstance(result, JsonResponse):
                    return result

                # Select State
                logger.info(f"Selecting State: {state}")
                def select_state():
                    state_dropdown = wait.until(EC.element_to_be_clickable((
                        By.XPATH,
                        "//label[contains(text(), 'State')]//following::input[contains(@class, 'search')][1]"
                    )))
                    driver.execute_script("arguments[0].scrollIntoView();", state_dropdown)
                    time.sleep(1)
                    state_dropdown.click()
                    time.sleep(1)
                    state_dropdown.send_keys(state)
                    time.sleep(1)
                    state_dropdown.send_keys(Keys.RETURN)
                    logger.info(f"Selected State: {state}")
                select_state.fallback_xpath = "//div[contains(@class, 'menu')]//div[@role='option']"

                result = retry_action(
                    action_name=f"State '{state}' selection",
                    action_func=select_state,
                    error_message=f"Error selecting State '{state}'. Available options",
                    status_code=400,
                    refresh_on_fail=False
                )
                if isinstance(result, JsonResponse):
                    return result

                # Fill in Payment Date
                logger.info(f"Entering Payment Date: {payment_date}")
                def enter_payment_date():
                    payment_date_input = wait.until(EC.element_to_be_clickable((By.NAME, "_payment_date")))
                    driver.execute_script("arguments[0].scrollIntoView();", payment_date_input)
                    time.sleep(1)
                    payment_date_input.clear()
                    payment_date_input.send_keys(payment_date)
                    logger.info(f"Entered Payment Date: {payment_date}")
                enter_payment_date.fallback_xpath = "//input[@name='_payment_date']"

                result = retry_action(
                    action_name="Payment Date entry",
                    action_func=enter_payment_date,
                    error_message="Error filling Payment Date",
                    status_code=400,
                    refresh_on_fail=False
                )
                if isinstance(result, JsonResponse):
                    return result

                # Select First Time Buyer
                logger.info(f"Selecting First Time Buyer: {first_time}")
                def select_first_time_buyer():
                    first_time_buyer_dropdown = wait.until(EC.element_to_be_clickable((
                        By.XPATH,
                        "//div[@name='firstTimeBuyer']"
                    )))
                    driver.execute_script("arguments[0].scrollIntoView();", first_time_buyer_dropdown)
                    time.sleep(1)
                    driver.execute_script("arguments[0].click();", first_time_buyer_dropdown)
                    time.sleep(1)
                    buyer_option = wait.until(EC.element_to_be_clickable((
                        By.XPATH,
                        f"//div[@name='firstTimeBuyer']//div[@role='option' and contains(translate(span/text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{first_time.lower()}')]"
                    )))
                    driver.execute_script("arguments[0].scrollIntoView();", buyer_option)
                    time.sleep(1)
                    driver.execute_script("arguments[0].click();", buyer_option)
                    logger.info(f"Selected First Time Buyer: {first_time}")
                select_first_time_buyer.fallback_xpath = "//div[@name='firstTimeBuyer']//div[@role='option']"

                result = retry_action(
                    action_name=f"First Time Buyer '{first_time}' selection",
                    action_func=select_first_time_buyer,
                    error_message=f"Error selecting First Time Buyer '{first_time}'. Available options",
                    status_code=400,
                    refresh_on_fail=False
                )
                if isinstance(result, JsonResponse):
                    return result

                # Fill in Agency Details
                logger.info("Filling agency details")
                def fill_agency_details():
                    fields = [
                        ("agent_company_name_", agency_cmp),
                        ("agent_tel_", agent_phone),
                        ("agency_admin_email", client_email),
                        ("agent_name_", agent_name),
                        ("remark", remarks)
                    ]
                    for field_name, value in fields:
                        field = wait.until(EC.element_to_be_clickable((By.NAME, field_name)))
                        driver.execute_script("arguments[0].scrollIntoView();", field)
                        time.sleep(0.5)
                        field.clear()
                        field.send_keys(value)
                        logger.info(f"Filled field '{field_name}' with '{value}'")
                fill_agency_details.fallback_xpath = "//input"

                result = retry_action(
                    action_name="Agency details entry",
                    action_func=fill_agency_details,
                    error_message="Error filling agency details",
                    status_code=400,
                    refresh_on_fail=False
                )
                if isinstance(result, JsonResponse):
                    return result

                # Click Save and Continue
                logger.info("Clicking Save and Continue")
                def click_save_continue():
                    save_button = wait.until(EC.element_to_be_clickable((
                        By.XPATH,
                        "//button[contains(@class, 'ui positive button saveBtn') and contains(text(), 'Save and Continue')]"
                    )))
                    driver.execute_script("arguments[0].scrollIntoView();", save_button)
                    time.sleep(1)
                    driver.execute_script("arguments[0].click();", save_button)
                    time.sleep(3)
                    logger.info("Clicked Save and Continue")
                click_save_continue.fallback_xpath = "//button[contains(@class, 'button')]"

                result = retry_action(
                    action_name="Save and Continue click",
                    action_func=click_save_continue,
                    error_message="Error clicking Save and Continue",
                    status_code=400,
                    refresh_on_fail=False
                )
                if isinstance(result, JsonResponse):
                    return result

                # Get page title
                page_title = driver.title
                logger.info("Reservation completed successfully")
                return JsonResponse({
                    "status": "success",
                    "message": "Reservation completed",
                    "page_title": page_title,
                    "received_data": received_data
                })

            finally:
                driver.quit()

        # CHANGE: Added specific handling for BrowserClosedException
        except BrowserClosedException as e:
            logger.error(f"Process terminated: {str(e)}")
            return JsonResponse({
                "status": "error",
                "message": str(e),
                "received_data": received_data
            }, status=400)

        except json.JSONDecodeError:
            logger.error("Invalid JSON format in POST data")
            return JsonResponse({
                "status": "error",
                "message": "Invalid JSON format",
                "received_data": received_data
            }, status=400)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return JsonResponse({
                "status": "error",
                "message": f"Unexpected error: {str(e)}",
                "received_data": received_data
            }, status=500)

    logger.error("Invalid request method")
    return JsonResponse({
        "status": "error",
        "message": "Invalid request method",
        "received_data": dict(request.POST)
    }, status=405)