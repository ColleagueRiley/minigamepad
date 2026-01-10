#!/usr/bin/env python3
import sys, urllib.request

URL = "https://raw.githubusercontent.com/mdqinc/SDL_GameControllerDB/refs/heads/master/gamecontrollerdb.txt"
HEADER = "minigamepad.h"
# Match the order and macros from the main branch
PLATFORMS = [
    ("Windows", "_WIN32"),
    ("Mac OS X", "__APPLE__"),
    ("iOS", "TARGET_OS_IPHONE"),
    ("Linux", "__linux__"),
    ("Android", "__ANDROID_API__")
]

def get_content():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f: return f.read()
    print(f"Fetching {URL}...")
    with urllib.request.urlopen(URL) as r: return r.read().decode('utf-8')

def main():
    mappings = {p[0]: [] for p in PLATFORMS}
    for line in get_content().splitlines():
        line = line.strip()
        if not line or line.startswith('#'): continue
        for platform, macro in PLATFORMS:
            key = f"platform:{platform}"
            if key in line:
                if platform != "iOS":
                    # Remove platform key and cleanup commas for non-iOS
                    clean_line = line.replace(key, "").replace(",,", ",").strip(",")
                    mappings[platform].append(clean_line)
                else:
                    # main branch keeps the platform tag for iOS
                    mappings[platform].append(line)
                break

    lines = ["const char * sdl_db[] = {"]
    first = True
    for platform, macro in PLATFORMS:
        if not mappings[platform]: continue
        if first:
            lines.append(f"#ifdef {macro}")
            first = False
        else:
            lines.append(f"#elif defined({macro})")
        
        for m in mappings[platform]:
            escaped_m = m.replace('"', '\"')
            lines.append(f'"{escaped_m},",')
    
    # Add Emscripten block to match main branch
    lines.append("#elif defined(EMSCRIPTEN)")
    lines.append('"\0" /* look into at some point */')
    lines.append("#endif\n};")
    
    with open(HEADER, 'r', encoding='utf-8') as f: content = f.read()
    start = content.find("const char * sdl_db[] = {")
    end = content.find("};", start) + 2
    if start == -1 or end == 1: sys.exit(f"Error: sdl_db not found in {HEADER}")
    
    with open(HEADER, 'w', encoding='utf-8') as f:
        f.write(content[:start] + "\n".join(lines) + content[end:])
    print(f"Updated {HEADER}")

if __name__ == "__main__": main()