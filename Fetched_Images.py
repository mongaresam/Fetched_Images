import requests
import os
import hashlib
from urllib.parse import urlparse

def get_filename_from_url(url):
    """Extract filename from URL or generate one."""
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    if not filename:
        filename = "downloaded_image.jpg"
    return filename

def is_duplicate(file_path, content):
    """Check if a file with the same content already exists."""
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            existing_hash = hashlib.md5(f.read()).hexdigest()
        new_hash = hashlib.md5(content).hexdigest()
        return existing_hash == new_hash
    return False

def fetch_image(url, folder="Fetched_Images"):
    """Download an image from a given URL and save it."""
    try:
        # Create directory if it doesn't exist
        os.makedirs(folder, exist_ok=True)

        # Fetch the image with headers for safety
        headers = {"User-Agent": "UbuntuFetcher/1.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Check Content-Type
        content_type = response.headers.get("Content-Type", "")
        if "image" not in content_type:
            print(f"✗ Skipped {url} (Not an image: {content_type})")
            return

        filename = get_filename_from_url(url)
        filepath = os.path.join(folder, filename)

        # Avoid duplicate downloads
        if is_duplicate(filepath, response.content):
            print(f"✗ Duplicate detected, skipping: {filename}")
            return

        # Save the image
        with open(filepath, "wb") as f:
            f.write(response.content)

        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")

    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
    except Exception as e:
        print(f"✗ An error occurred: {e}")

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    # Accept multiple URLs
    urls = input("Please enter one or more image URLs (comma separated): ").split(",")

    for url in [u.strip() for u in urls if u.strip()]:
        fetch_image(url)

    print("\nConnection strengthened. Community enriched.")

if __name__ == "__main__":
    main()
