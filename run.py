import cv2
import numpy as np
import pyautogui
import time
import os

# Full list of Gen 1 Pokémon (you can expand this list as needed)
pokemon_list = [
    "bulbasaur", "ivysaur", "venusaur", "charmander", "charmeleon", "charizard",
    "squirtle", "wartortle", "blastoise", "caterpie", "metapod", "butterfree",
    "weedle", "kakuna", "beedrill", "pidgey", "pidgeotto", "pidgeot",
    "rattata", "raticate", "spearow", "fearow", "ekans", "arbok",
    "pikachu", "raichu", "sandshrew", "sandslash", "nidoran♀", "nidorina",
    "nidoqueen", "nidoran♂", "nidorino", "nidoking", "clefairy", "clefable",
    "vulpix", "ninetales", "jigglypuff", "wigglytuff", "zubat", "golbat",
    "oddish", "gloom", "vileplume", "paras", "parasect", "venonat",
    "venomoth", "diglett", "dugtrio", "meowth", "persian", "psyduck",
    "golduck", "mankey", "primeape", "growlithe", "arcanine", "poliwag",
    "poliwhirl", "poliwrath", "abra", "kadabra", "alakazam", "machop",
    "machoke", "machamp", "bellsprout", "weepinbell", "victreebel", "tentacool",
    "tentacruel", "geodude", "graveler", "golem", "ponyta", "rapidash",
    "slowpoke", "slowbro", "magnemite", "magneton", "farfetch'd", "doduo",
    "dodrio", "seel", "dewgong", "grimer", "muk", "shellder",
    "cloyster", "gastly", "haunter", "gengar", "onix", "drowzee",
    "hypno", "krabby", "kingler", "voltorb", "electrode", "exeggcute",
    "exeggutor", "cubone", "marowak", "hitmonlee", "hitmonchan", "lickitung",
    "koffing", "weezing", "rhyhorn", "rhydon", "chansey", "tangela",
    "kangaskhan", "horsea", "seadra", "goldeen", "seaking", "staryu",
    "starmie", "mr. mime", "scyther", "jynx", "electabuzz", "magmar",
    "pinsir", "tauros", "magikarp", "gyarados", "lapras", "ditto",
    "eevee", "vaporeon", "jolteon", "flareon", "porygon", "omanyte",
    "omastar", "kabuto", "kabutops", "aerodactyl", "snorlax", "articuno",
    "zapdos", "moltres", "dratini", "dragonair", "dragonite", "mewtwo", "mew"
]

def find_and_click_pokeball(template_path, threshold=0.6, max_tries=5):
    print(f"Finding and clicking Poké Ball (will try {max_tries} times)...")
    for attempt in range(max_tries):
        print(f"Attempt {attempt + 1}/{max_tries}...")
        # Take a screenshot
        screenshot = pyautogui.screenshot()
        screenshot_np = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        # Load the template image
        template = cv2.imread(template_path)
        if template is None:
            print(f"Could not load template image from {template_path}")
            return False # Stop if template can't load

        result = cv2.matchTemplate(screenshot_np, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold:
            print("Poké Ball found on screen!")
            template_height, template_width = template.shape[:2]
            center_x_img = max_loc[0] + template_width // 2
            center_y_img = max_loc[1] + template_height // 2

            # Map image coordinates to screen coordinates
            screen_width, screen_height = pyautogui.size()
            img_height, img_width = screenshot_np.shape[:2]
            scale_x = screen_width / img_width
            scale_y = screen_height / img_height
            center_x = int(center_x_img * scale_x)
            center_y = int(center_y_img * scale_y)

            # Move the mouse and click
            pyautogui.moveTo(center_x, center_y, duration=0.2)
            pyautogui.click()
            print("Poké Ball clicked!")
            # No need for time.sleep(5) here, it's handled in the main loop
            return True # Found and clicked, exit function

        # If not found and it's not the last attempt, wait before trying again
        if attempt < max_tries - 1:
            print("Poké Ball not found yet, trying again...")
            time.sleep(1) # Wait 1 second before next attempt

    # If loop finishes without finding the ball
    print(f"Poké Ball not found after {max_tries} attempts. Skipping.")
    return False

def search_next_pokemon(pokemon_name):
    # Click inside the browser window first to ensure focus
    print("Clicking inside browser window to ensure focus...")
    pyautogui.click(10, 50) # Click at a known safe coordinate (top-left area)
    time.sleep(0.3) # Short pause after click

    print("Running Cmd+L to go to URL bar")
    # Focus the URL bar (Cmd+L), type the new URL, and press Enter
    pyautogui.hotkey('command', 'l')
    time.sleep(0.2)

    url = f"https://www.google.com/search?q={pokemon_name}"
    pyautogui.typewrite(url)
    pyautogui.press('enter')
    print(f"Searched for {pokemon_name}")
    time.sleep(1)  # Reduced wait time for page load

def position_chrome_left():
    # Get the screen height using pyautogui
    screen_width, screen_height = pyautogui.size()
    # Set Chrome window to fill the left side (adjust width as needed)
    left = 0
    top = 0
    width = 900  # You can adjust this width if you want
    height = screen_height
    applescript = f'''
    tell application "Google Chrome"
        set bounds of front window to {{{left}, {top}, {left + width}, {top + height}}}
        activate
    end tell
    '''
    os.system(f"osascript -e '{applescript}'")
    time.sleep(1)

def load_completed(filename):
    if not os.path.exists(filename):
        return set()
    with open(filename, "r") as f:
        return set(line.strip() for line in f if line.strip())

def save_completed(filename, pokemon):
    with open(filename, "a") as f:
        f.write(pokemon + "\n")

if __name__ == "__main__":
    template_path = os.path.join(os.path.dirname(__file__), "pokeball.png")
    completed_file = os.path.join(os.path.dirname(__file__), "completed_pokemon.txt")
    completed = load_completed(completed_file)
    
    print("Positioning Chrome window...")
    position_chrome_left() # This also activates Chrome
    # Removed the call to focus_browser()
    
    print("Starting Pokémon search loop...")
    for pokemon in pokemon_list:
        if pokemon in completed:
            print(f"Skipping {pokemon}, already completed.")
            continue
        search_next_pokemon(pokemon)
        success = find_and_click_pokeball(template_path)
        if success:
            save_completed(completed_file, pokemon)

            # wait for 5 seconds
            print("Waiting before next search...")
            time.sleep(15)
        
        

    