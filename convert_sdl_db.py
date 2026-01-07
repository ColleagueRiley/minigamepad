import os

INPUT_FILE = "../SDL_GameControllerDB/gamecontrollerdb.txt"
OUTPUT_FILE = "minigamepad.h"

platforms = {
    "Windows": "MG_WINDOWS",
    "Mac OS X": "MG_MACOS",
    "Linux": "MG_LINUX",
    "Android": "__ANDROID_API__",
    "iOS": "TARGET_OS_IPHONE",
}

mappings = {k: [] for k in platforms}

try:
    if not os.path.exists(INPUT_FILE):
        print(f"Error: Could not find {INPUT_FILE}")
        exit(1)

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Find which platform this line belongs to
            platform_found = False
            for p_name in platforms:
                if f"platform:{p_name}" in line:
                    mappings[p_name].append(line)
                    platform_found = True
                    break
            
            # If no platform found, ignore or handle as needed
            if not platform_found:
               pass

    # Generate the new content
    new_content_lines = []
    new_content_lines.append("const char * sdl_db[] = {")
    
    first_block = True
    for p_name, macro in platforms.items():
        lines = mappings[p_name]
        if not lines:
            continue
            
        if first_block:
            new_content_lines.append(f"#if defined({macro})")
            first_block = False
        else:
            new_content_lines.append(f"#elif defined({macro})")
            
        for l in lines:
            # Escape double quotes just in case
            l_escaped = l.replace('"', '\\"') 
            new_content_lines.append(f'"{l_escaped}",')

    if not first_block:
        new_content_lines.append("#endif")
        
    new_content_lines.append("};")

    # Read minigamepad.h
    with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
        header_lines = f.readlines()

    # Find start and end of sdl_db
    start_index = -1
    end_index = -1
    
    for i, line in enumerate(header_lines):
        if "const char * sdl_db[] = {" in line:
            start_index = i
            break
            
    if start_index != -1:
        for i in range(start_index, len(header_lines)):
            if "};" in header_lines[i]:
                end_index = i
                break

    if start_index != -1 and end_index != -1:
        print(f"Found sdl_db at lines {start_index + 1}-{end_index + 1}")
        
        # Construct the new file content
        final_lines = header_lines[:start_index] + [l + '\n' for l in new_content_lines] + header_lines[end_index+1:]
        
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.writelines(final_lines)
            
        print(f"Successfully updated {OUTPUT_FILE}")
    else:
        print(f"Error: Could not find sdl_db definition in {OUTPUT_FILE}")

except FileNotFoundError:
    print(f"Error: Could not find file")
except Exception as e:
    print(f"An error occurred: {e}")
