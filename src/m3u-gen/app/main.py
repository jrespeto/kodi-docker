import os
import time
import requests

M3U_HEADER = "#EXTM3U\n"

def fetch_categories(url, username, password, timeout, verify, headers):
    """Fetch category mapping if enabled"""
    api_url = f"{url}/player_api.php?username={username}&password={password}&action=get_live_categories"
    try:
        resp = requests.get(api_url, timeout=timeout, verify=verify, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        return {c["category_id"]: c["category_name"] for c in data if "category_id" in c}
    except Exception as e:
        print(f"⚠️ Could not fetch categories: {e}")
        return {}

def generate_playlist():
    url = os.environ.get("URL")
    username = os.environ.get("USERNAME", "")
    password = os.environ.get("PASSWORD", "")
    output_file = os.environ.get("OUTPUT_FILE", "/data/playlist.m3u")

    refresh_seconds = int(os.environ.get("REFRESH_SECONDS", 86400))
    timeout = int(os.environ.get("REQUEST_TIMEOUT", 20))
    verify_ssl = os.environ.get("VERIFY_SSL", "true").lower() in ("1", "true", "yes")
    use_categories = os.environ.get("USE_CATEGORIES", "false").lower() in ("1", "true", "yes")
    user_agent = os.environ.get("USER_AGENT", "Mozilla/5.0 Kodi-M3U/1.0")

    if not url or not password:
        raise ValueError("URL and PASSWORD must be set in environment variables")

    headers = {"User-Agent": user_agent}

    # Fetch category mapping if enabled
    category_map = {}
    if use_categories:
        category_map = fetch_categories(url, username, password, timeout, verify_ssl, headers)

    # Pull live streams
    api_url = f"{url}/player_api.php?username={username}&password={password}&action=get_live_streams"
    resp = requests.get(api_url, timeout=timeout, verify=verify_ssl, headers=headers)
    resp.raise_for_status()
    streams = resp.json()

    lines = [M3U_HEADER]

    for stream in streams:
        name = stream.get("name", "Unknown")
        stream_id = stream.get("stream_id")
        logo = stream.get("stream_icon", "")
        category_id = stream.get("category_id", "")

        if not stream_id:
            continue

        group_title = category_map.get(category_id, f"Group {category_id}" if category_id else "General")

        extinf = (
            f'#EXTINF:-1 tvg-id="" tvg-name="{name}" '
            f'tvg-logo="{logo}" group-title="{group_title}",{name}\n'
        )
        stream_url = f"{url}/live/{username}/{password}/{stream_id}.ts"

        lines.append(extinf)
        lines.append(f"{stream_url}\n")

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"✅ Playlist written to {output_file} with {len(streams)} entries")
    return refresh_seconds


def main():
    while True:
        try:
            refresh_seconds = generate_playlist()
        except Exception as e:
            print(f"❌ Error generating playlist: {e}")
            refresh_seconds = int(os.environ.get("REFRESH_SECONDS", 86400))

        print(f"⏳ Sleeping for {refresh_seconds} seconds before next run...")
        time.sleep(refresh_seconds)


if __name__ == "__main__":
    main()
