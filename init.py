import subprocess
import sys


def install_package(package_name):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"✅ '{package_name}' installed successfully.")
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install '{package_name}'.")


def main():
    # List of packages to install
    packages = [
        "django",               # Django for web development
        "djangorestframework",  # Django Rest Framework for building APIs
        "pymysql",              # MySQL connector for Python (if you are using PyMySQL)
        "pandas",               # Pandas for data manipulation
        "mysqlclient",           # MySQL client (alternative to PyMySQL, recommended for performance)
        "django-cors-headers",
        "selenium",
        "webdriver-manager"
    ]

    for package in packages:
        install_package(package)


if __name__ == "__main__":
    main()
