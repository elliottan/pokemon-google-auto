# Pokémon Google Search Automator

This script automates searching for Gen 1 Pokémon on Google and clicking the interactive Poké Ball element that sometimes appears in the search results. It keeps track of completed Pokémon to avoid duplicates.

## Prerequisites

*   **Python 3:** Make sure you have Python 3 installed. You can check by running `python3 --version` in your terminal.
*   **pip:** Python's package installer. Usually comes with Python 3.
*   **Git:** For cloning the repository.
*   **macOS:** The script uses AppleScript to position the Chrome window, so it's currently macOS-specific.
*   **Google Chrome:** The script is designed to work with Google Chrome.

## Setup

1.  **Clone the Repository:**
    Open your terminal and navigate to the directory where you want to store the project. Then run:
    ```bash
    git clone <your-repository-url> # Replace <your-repository-url> with the actual URL
    cd pokemon-google-auto
    ```

2.  **Install Dependencies:**
    This script requires several Python libraries. Install them using pip:
    ```bash
    pip3 install opencv-python numpy pyautogui selenium
    ```
    *   `opencv-python`: Used for image recognition (finding the Poké Ball).
    *   `numpy`: A dependency for OpenCV.
    *   `pyautogui`: Used for controlling the mouse and keyboard to automate browser actions.
    *   `selenium`: Used for UI automation.

## Browser Preparation

1.  **Open Google Chrome:** Make sure Google Chrome is running.
2.  **Open devtools and set to mobile view mode:**
    *   Open the Chrome devtools by right-clicking on the page and selecting "Inspect".
    *   Click the "Toggle device toolbar" button in the top-right corner of the devtools.
    *   In the device toolbar, select "Mobile" from the dropdown.
    *   Select a mobile device from the list (e.g., iPhone 12 Pro).
    *   Set the resolution as "fit to screen"
3.  **Window Positioning:** The script will automatically attempt to position the *frontmost* Chrome window to the left half of your screen using AppleScript. Ensure the Chrome window you want to use is active *before* running the script.
    *   *Note:* The script clicks near the top-left (coordinates 10, 50) to focus the window and uses `Cmd+L` to focus the address bar. Ensure these actions are appropriate for your screen setup and don't interfere with other elements.

## Running the Script

1.  **Navigate to Directory:** Open your terminal and make sure you are in the `pokemon-google-auto` directory (the one containing `run.py`).
2.  **Execute the Script:** Run the script using Python 3:
    ```bash
    python3 run.py
    ```
3.  **Grant Permissions (If Prompted):** On the first run, macOS may ask for permission to allow your terminal or Python to control the computer (Accessibility) and record the screen (Screen Recording) because `pyautogui` needs these permissions. You'll need to grant these in System Settings > Privacy & Security for the script to function correctly.

The script will then:
*   Position the Chrome window.
*   Iterate through the `pokemon_list` defined in <mcfile name="run.py" path="/Users/elliottan/Developer/pokemon-google-auto/run.py"></mcfile>.
*   Skip Pokémon already listed in <mcfile name="completed_pokemon.txt" path="/Users/elliottan/Developer/pokemon-google-auto/completed_pokemon.txt"></mcfile>.
*   Search for the current Pokémon on Google.
*   Attempt to find the Poké Ball image (specified by `template_path`, e.g., `assets/pokeball.png`) on the screen (up to 5 tries).
*   If found, click the Poké Ball and add the Pokémon name to <mcfile name="completed_pokemon.txt" path="/Users/elliottan/Developer/pokemon-google-auto/completed_pokemon.txt"></mcfile>.
*   Wait for 15 seconds before searching for the next Pokémon.
*   If not found after 5 tries, it skips to the next Pokémon without saving it as completed.

## How It Works

*   **Automation:** Uses `pyautogui` to simulate keyboard shortcuts (`Cmd+L`), typing, mouse movements, and clicks.
*   **Image Recognition:** Uses `opencv-python` to take screenshots and find the template image (e.g., `assets/pokeball.png`) within the screenshot.
*   **State Tracking:** Uses `completed_pokemon.txt` to keep track of which Pokémon have been successfully processed, allowing the script to be stopped and resumed.

## Included Files

*   `run.py`: The main Python script.
*   `completed_pokemon.txt`: A text file listing the Pokémon for which the Poké Ball has been successfully clicked. This file is created/updated automatically.