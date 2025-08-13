import requests
import configparser

def get_emby_data(base_url, api_key):
    """
    Fetches server info and library counts from Emby API.
    """
    headers = {
        'X-Emby-Token': api_key,
        'Content-Type': 'application/json'
    }
    
    system_info = None
    libraries = []

    try:
        # Get System Info
        system_info_url = f"{base_url}/System/Info"
        system_info_response = requests.get(system_info_url, headers=headers, verify=False)
        system_info_response.raise_for_status()
        system_info = system_info_response.json()

        # Get Library Info
        library_url = f"{base_url}/Library/VirtualFolders"
        library_response = requests.get(library_url, headers=headers, verify=False)
        library_response.raise_for_status()
        raw_libraries = library_response.json()

        for lib in raw_libraries:
            library_info = {
                "Name": lib.get("Name"),
                "TotalCount": 0
            }
            
            items_url = f"{base_url}/Items?ParentId={lib.get('ItemId')}&Recursive=true&IncludeItemTypes=Movie,Series,MusicAlbum&Fields=ParentId"
            items_response = requests.get(items_url, headers=headers, verify=False)
            items_response.raise_for_status()
            items = items_response.json()
            library_info["TotalCount"] = items.get("TotalRecordCount", 0)
            libraries.append(library_info)
            
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Emby: {e}")
        return None, None

    return system_info, libraries

def format_as_markdown(system_info, libraries):
    """
    Formats the data into a single code block for maximum compatibility with Telegram.
    """
    if not system_info or not libraries:
        return "```\nError: Could not retrieve data from Emby.\n```"

    # Start the code block
    md = "```\n"
    
    # System Info
    md += "--- Emby Server Status ---\n"
    md += f"Server Name : {system_info.get('ServerName', 'N/A')}\n"
    md += f"Version     : {system_info.get('Version', 'N/A')}\n"
    md += f"OS          : {system_info.get('OperatingSystemDisplayName', 'N/A')}\n"
    md += "\n" # Add a blank line for spacing

    # Library Info
    md += "--- Media Library Stats ---\n"
    md += "Library Name      | Item Count\n"
    md += "------------------|-----------\n"
    for lib in libraries:
        name = lib.get('Name', 'N/A')
        count = lib.get('TotalCount', 0)
        # Adjust padding to ensure alignment. 18 for name, 10 for count.
        md += f"{name:<18}| {str(count):<10}\n"
    
    # End the code block
    md += "```"
    
    return md

def main():
    import os
    config = configparser.ConfigParser()
    config_path = 'config.ini'
    
    if not os.path.exists(config_path):
        print(f"Error: '{config_path}' not found in the current directory: {os.getcwd()}")
        return

    config.read(config_path)

    if 'emby' not in config:
        print(f"Error: [emby] section not found in '{config_path}'.")
        return

    base_url = config['emby'].get('url')
    api_key = config['emby'].get('api_key')

    if not base_url or not api_key or 'YOUR_EMBY_URL' in base_url or 'YOUR_API_KEY' in api_key:
        print(f"Error: Please make sure 'url' and 'api_key' are correctly set in '{config_path}'.")
        return

    system_info, libraries = get_emby_data(base_url, api_key)
    markdown_output = format_as_markdown(system_info, libraries)
    print(markdown_output)

if __name__ == "__main__":
    main()