import json
import requests
import os
import csv



# GitHub API URL for the releases of the repository
url = "https://api.github.com/repos/ChrGri/DIY-Sim-Racing-FFB-Pedal/releases"
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Deserialize JSON response
    releases = response.json()


#######################################################################################
# make csv file
#######################################################################################

# Initialize a dictionary to store asset URLs
release_names = []
asset_names = set()
asset_urls = {}

# Step 1: Collect all unique asset names and prepare asset URLs per release
releaseStartIdx = 85
for release in reversed(releases):
#for release in releases:

    isPreRelease = release.get("prerelease")

    if not isPreRelease:
        release_name = release.get("name", "No name provided")
        versionString = release_name[17:]
        releaseStartIdx = int( versionString )


    if 1:#(isPreRelease):

        release_name = release.get("name", "No name provided")
        release_names.append(release_name)

        # Iterate over each asset in the release
        for asset in release.get("assets", []):
            asset_name = asset.get("name", "No name provided")
            asset_url = asset.get("browser_download_url", "")

            # Add the asset name to the set of unique asset names
            asset_names.add(asset_name)

            # Store the URL for this asset under the release name
            if release_name not in asset_urls:
                asset_urls[release_name] = {}

            asset_urls[release_name][asset_name] = asset_url

# Step 2: Write data to a CSV file
csv_filename = "release_assets.csv"

with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
    # Create a CSV writer object
    csv_writer = csv.writer(csvfile)

    # Write the header row (release names followed by asset names)
    header = ["Release Name"] + sorted(asset_names)
    csv_writer.writerow(header)

    # Write the data rows (each release name with corresponding asset URLs)
    for release_name in release_names:
        row = [release_name]

        # For each asset name, add the corresponding URL to the row
        for asset_name in sorted(asset_names):
            asset_url = asset_urls.get(release_name, {}).get(asset_name, "")
            row.append(asset_url)

        csv_writer.writerow(row)

print(f"CSV file '{csv_filename}' generated successfully.")
