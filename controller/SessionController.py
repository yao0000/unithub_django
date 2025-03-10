import json
import time
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

@csrf_exempt
def run_reserve(request):
    if request.method == "POST":
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            # project_name = request_data.get("project_name")
            # unit_name = request_data.get("unit_name")

            # Validate input data
            # if not email or not password or not project_name or not unit_name:
            #     return JsonResponse({"status": "error", "message": "Missing required parameters"}, status=400)
            
            if not email or not password:
                return JsonResponse({"status": "error", "message": "Missing required parameters"}, status=400)
            # Automatically get the latest ChromeDriver
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service)

            try:
                # Navigate to the login page
                driver.get("https://secure.mhub.my/login")
                time.sleep(2)  # Allow page to load

                # Find and fill in login fields
                driver.find_element(By.NAME, "email").send_keys(email)
                driver.find_element(By.NAME, "password").send_keys(password)
                driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)

                # Wait for login process
                time.sleep(5)

                # Navigate to the projects page
                driver.get("https://exs.mhub.my/projects/")
                time.sleep(3)

                # Find and click the project link
                # try:
                #     project_link = driver.find_element(By.LINK_TEXT, project_name)
                #     ActionChains(driver).move_to_element(project_link).click().perform()
                #     time.sleep(3)
                # except Exception as e:
                    # return JsonResponse({"status": "error", "message": f"Project '{project_name}' not found: {str(e)}"})

                # Scroll to "Layouts" divider
                # divider = driver.find_element(By.XPATH, "//div[@class='ui horizontal divider' and text()='Layouts']")
                # driver.execute_script("arguments[0].scrollIntoView();", divider)
                # time.sleep(2)

                # Find and click on the unit name
                # try:
                #     unit_div = driver.find_element(By.XPATH, f"//div[@class='ui header' and text()='{unit_name}']")
                #     ActionChains(driver).move_to_element(unit_div).click().perform()
                #     time.sleep(3)
                # except Exception as e:
                #     return JsonResponse({"status": "error", "message": f"Unit '{unit_name}' not found: {str(e)}"})

                # # Find and click the "Reserve" button
                # try:
                #     reserve_button = driver.find_element(By.XPATH, f"//div[contains(@class, 'ui header') and text()='{unit_name}']//following::button[@class='ui button button-reduce-spacing']")
                #     reserve_button.click()
                #     time.sleep(5)
                # except Exception as e:
                #     return JsonResponse({"status": "error", "message": "Reserve button not found"})

                # # Get page title after the action
                # page_title = driver.title

            finally:
                driver.quit()

            # return JsonResponse({"status": "success", "message": "Reservation completed", "page_title": page_title})

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON format"}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)
