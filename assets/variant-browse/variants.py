import json
import os

# Load JSON data from the files
# with open('/CollectionState.json') as f:
#     collection_state = json.load(f)

# with open('/GameState.json') as f:
#     game_state = json.load(f)

# with open('/ProfileState.json') as f:
#     profile_state = json.load(f)

# # Define file paths
profileFilePath = (
    "~/AppData/Locallow/Second Dinner/SNAP/Standalone/States/nvprod/ProfileState.json"
)
shopFilePath = (
    "~/AppData/Locallow/Second Dinner/SNAP/Standalone/States/nvprod/ShopState.json"
)
collectionFilePath = "~/AppData/Locallow/Second Dinner/SNAP/Standalone/States/nvprod/CollectionState.json"
gameFilePath = (
    "~/AppData/Locallow/Second Dinner/SNAP/Standalone/States/nvprod/GameState.json"
)

# region - original code for system type
# ## funs for handling system type
# if isSystemLinux():
# 	profileFilePath = "~/.steam/steam/steamapps/compatdata/1997040/pfx/drive_c/users/steamuser/AppData/LocalLow/Second Dinner/SNAP/Standalone/States/nvprod/ProfileState.json"
# if isSystemMobile():
# 	profileFilePath = "/sdcard/Android/data/com.nvsgames.snap/files/Standalone/States/nvprod/ProfileState.json"
# # profilePath = os.path.expanduser(profileFilePath)

# if isSystemLinux():
# 	shopFilePath = "~/.steam/steam/steamapps/compatdata/1997040/pfx/drive_c/users/steamuser/AppData/LocalLow/Second Dinner/SNAP/Standalone/States/nvprod/ShopState.json"
# if isSystemMobile():
# 	shopFilePath = "/sdcard/Android/data/com.nvsgames.snap/files/Standalone/States/nvprod/ShopState.json"
# # shopPath = os.path.expanduser(shopFilePath)

# if isSystemLinux():
# 	collectionFilePath = "~/.steam/steam/steamapps/compatdata/1997040/pfx/drive_c/users/steamuser/AppData/LocalLow/Second Dinner/SNAP/Standalone/States/nvprod/CollectionState.json"
# if isSystemMobile():
# 	collectionFilePath = "/sdcard/Android/data/com.nvsgames.snap/files/Standalone/States/nvprod/CollectionState.json"
# # collectionPath = os.path.expanduser(collectionFilePath)

# if isSystemLinux():
# 	gameFilePath = "~/.steam/steam/steamapps/compatdata/1997040/pfx/drive_c/users/steamuser/AppData/LocalLow/Second Dinner/SNAP/Standalone/States/nvprod/GameState.json"
# if isSystemMobile():
# 	gameFilePath = "/sdcard/Android/data/com.nvsgames.snap/files/Standalone/States/nvprod/GameState.json"
# # gamePath = os.path.expanduser(gameFilePath)
# endregion

###################


# Load JSON data from the files
def load_json(file_path):
    try:
        # Expand the user path and open the file with utf-8-sig encoding to handle BOM
        with open(os.path.expanduser(file_path), "r", encoding="utf-8-sig") as f:
            # Read file content
            content = f.read()
            # Check if file is empty
            if not content.strip():
                raise ValueError(f"The file {file_path} is empty.")
            # Parse JSON content
            jsonContent = json.loads(content)
            return jsonContent
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from file {file_path}: {e}")
        return None
    except Exception as e:
        print(f"Error loading file {file_path}: {e}")
        return None


game_state = load_json(gameFilePath)
collection_state = load_json(collectionFilePath)
profile_state = load_json(profileFilePath)
shop_state = load_json(shopFilePath)

# Check if the data was loaded successfully
if not game_state or not collection_state or not profile_state or not shop_state:
    print(
        "One or more JSON files could not be loaded. Please check the file paths and content."
    )

if game_state and collection_state and profile_state and shop_state:
    # Extract relevant data
    cards = collection_state["ServerState"]["AvatarInventory"]["OwnedAvatars"]
    unlocked_cards = []
    invalidCards = []
    # Filter for unlocked cards
    try:
        for card in cards:
            # if card["CardArtAvatar"]["CardDefId"] == "CardDefID":
            # if 'CardDefId' in card['CardArtAvatar']:
            unlocked_cards.append(
                {
                    "card_name": card["CardArtAvatar"]["CardDefId"],
                    "variants": card.get("ArtVariantDefId", "Default Variant"),
                }
            )
            
    except KeyError as e:
        invalidCards.append(card)
        print(f"Error extracting card data: {e}")

    # unlocked_cards = [
    #     {
    #         "card_name": card["CardArtAvatar"]["CardDefId"],
    #         "variants": card.get("ArtVariantDefId", "Default Variant")
    #     }
    #     for card in cards
    # ]

    # Generate HTML
    def generate_html_table(cards):
        # Generate the HTML structure
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Unlocked Marvel Snap Cards</title>
            <style>
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                table, th, td {
                    border: 1px solid black;
                }
                th, td {
                    padding: 10px;
                    text-align: left;
                }
                th {
                    background-color: #f2f2f2;
                }
            </style>
        </head>
        <body>
            <h1>Unlocked Marvel Snap Cards</h1>
            <input type="text" id="search" placeholder="Search for cards..." onkeyup="filterCards()">
            <table id="cardsTable">
                <thead>
                    <tr>
                        <th>Card Name</th>
                        <th>Variants</th>
                    </tr>
                </thead>
                <tbody>
        """

        # Generate the table rows
        for card in cards:
            html += f"""
                    <tr>
                        <td>{card['card_name']}</td>
                        <td>{card['variants']}</td>
                    </tr>
            """
        return html

    html_content = generate_html_table(unlocked_cards)

    # Write the HTML content to a file
    with open("unlocked_cards.html", "w") as file:
        file.write(html_content)
        
else:
    print("Data not available to generate the HTML.")
