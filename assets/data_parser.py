import json
import os
import datetime
import platform
from os import environ

is_android = "ANDROID_STORAGE" in environ


def isSystemWindows():
	return platform.system() == "Windows"


def isSystemLinux():
	return platform.system() == "Linux"


def isSystemMobile():
	if platform.system() == "Linux" and is_android:
		return True
	return False


snapId = ""
playerName = ""
rankedWins = 0
rankedLosses = 0
rankedTies = 0
rankedWinPrct = 0.0
standing = ""
skillRating = ""
rankedCurrentLevel = 0
rankedMaxLevel = 0
rankedCurrentLevelCubes = 0
rankedMaxLevelCubes = 0
rankedGamesPlayedThisSeason = 0
rankedCurrentWinStreak = 0
timeUpdated = ""
cardData = []
timeStarted = ""
concedes = 0
opponentConcedes = 0
snaps = 0
conquestPGPlayed = 0
conquestPGStreak = 0
conquestSilverPlayed = 0
conquestSilverStreak = 0
conquestGoldPlayed = 0
conquestGoldStreak = 0
conquestInfinityPlayed = 0
conquestInfinityStreak = 0
totalGoldSpent = 0
totalCreditsSpent = 0
totalCollectorsTokensSpent = 0
battlePassesBought = 0
cardsOwned = 0
cardSplits = 0
variants = 0
avatarsOwned = 0
titlesOwned = 0
cardBacksOwned = 0
collectionLvl = 0
cardUnlockHistory = {}

profileFilePath = (
	"~/AppData/Locallow/Second Dinner/SNAP/Standalone/States/nvprod/ProfileState.json"
)
if isSystemLinux():
	profileFilePath = "~/.steam/steam/steamapps/compatdata/1997040/pfx/drive_c/users/steamuser/AppData/LocalLow/Second Dinner/SNAP/Standalone/States/nvprod/ProfileState.json"
if isSystemMobile():
	profileFilePath = "/sdcard/Android/data/com.nvsgames.snap/files/Standalone/States/nvprod/ProfileState.json"
profilePath = os.path.expanduser(profileFilePath)

shopFilePath = (
	"~/AppData/Locallow/Second Dinner/SNAP/Standalone/States/nvprod/ShopState.json"
)
if isSystemLinux():
	shopFilePath = "~/.steam/steam/steamapps/compatdata/1997040/pfx/drive_c/users/steamuser/AppData/LocalLow/Second Dinner/SNAP/Standalone/States/nvprod/ShopState.json"
if isSystemMobile():
	shopFilePath = "/sdcard/Android/data/com.nvsgames.snap/files/Standalone/States/nvprod/ShopState.json"
shopPath = os.path.expanduser(shopFilePath)

collectionFilePath = "~/AppData/Locallow/Second Dinner/SNAP/Standalone/States/nvprod/CollectionState.json"
if isSystemLinux():
	collectionFilePath = "~/.steam/steam/steamapps/compatdata/1997040/pfx/drive_c/users/steamuser/AppData/LocalLow/Second Dinner/SNAP/Standalone/States/nvprod/CollectionState.json"
if isSystemMobile():
	collectionFilePath = "/sdcard/Android/data/com.nvsgames.snap/files/Standalone/States/nvprod/CollectionState.json"
collectionPath = os.path.expanduser(collectionFilePath)


def reload_file():
	with open(shopPath, encoding="utf-8-sig") as shop_json_file:
		data = json.load(shop_json_file)

		global battlePassesBought
		if (
			"BattlePassPremiumBasic"
			not in data["ServerState"]["Account"]["ProductPurchaseCount"]
		):
			battlePassesBought = 0
		else:
			battlePassesBought = data["ServerState"]["Account"]["ProductPurchaseCount"][
				"BattlePassPremiumBasic"
			]

	with open(profilePath, encoding="utf-8-sig") as profile_json_file:
		data = json.load(profile_json_file)

		global snapId
		snapId = data["ServerState"]["Account"]["SnapId"]

		global playerName
		playerName = data["ServerState"]["Account"]["Name"]

		global rankedWins
		rankedWins = data["ServerState"]["Account"]["WinsInPlaytestEnvironment"]

		global rankedLosses
		rankedLosses = data["ServerState"]["Account"]["LossesInPlaytestEnvironment"]

		global rankedTies
		if "TiesInPlaytestEnvironment" not in data["ServerState"]["Account"]:
			rankedTies = 0
		else:
			rankedTies = data["ServerState"]["Account"]["TiesInPlaytestEnvironment"]

		global standing
		if (
			"LeaderboardLog" not in data["ServerState"]
			or "InfiniteLeaderboardDetails" not in data["ServerState"]["LeaderboardLog"]
		):
			standing = "N.A."
		else:
			standing = "#" + str(
				data["ServerState"]["LeaderboardLog"]["InfiniteLeaderboardDetails"][
					"SkillRating"
				]
			)

		global skillRating
		if (
			"LeaderboardLog" not in data["ServerState"]
			or "InfiniteLeaderboardSkillRating"
			not in data["ServerState"]["LeaderboardLog"]
		):
			skillRating = "N.A."
		else:
			skillRating = data["ServerState"]["LeaderboardLog"][
				"InfiniteLeaderboardSkillRating"
			]

		global rankedMaxLevel
		rankedMaxLevel = data["ServerState"]["RankLog"]["HighWatermarkRankDetails"][
			"Rank"
		]

		global rankedMaxLevelCubes
		if "Trophies" not in data["ServerState"]["RankLog"]["HighWatermarkRankDetails"]:
			rankedMaxLevelCubes = 0
		else:
			rankedMaxLevelCubes = data["ServerState"]["RankLog"][
				"HighWatermarkRankDetails"
			]["Trophies"]

		global rankedCurrentLevel
		rankedCurrentLevel = data["ServerState"]["RankLog"]["CurrentRankDetails"][
			"Rank"
		]

		global rankedCurrentLevelCubes
		if "Trophies" not in data["ServerState"]["RankLog"]["CurrentRankDetails"]:
			rankedCurrentLevelCubes = 0
		else:
			rankedCurrentLevelCubes = data["ServerState"]["RankLog"][
				"CurrentRankDetails"
			]["Trophies"]

		global rankedGamesPlayedThisSeason
		if "GamesPlayedInSeason" not in data["ServerState"]["RankLog"]:
			rankedGamesPlayedThisSeason = 0
		else:
			rankedGamesPlayedThisSeason = data["ServerState"]["RankLog"][
				"GamesPlayedInSeason"
			]

		global rankedCurrentWinStreak
		if "HistoryPerLeague" in data["ServerState"]["MatchHistory"]:
			allLeagueData = data["ServerState"]["MatchHistory"]["HistoryPerLeague"]

		global conquestPGPlayed
		global conquestPGStreak
		global conquestSilverPlayed
		global conquestSilverStreak
		global conquestGoldPlayed
		global conquestGoldStreak
		global conquestInfinityPlayed
		global conquestInfinityStreak
		rankedData = None

		for item in allLeagueData:
			if item["LeagueDefId"] == "Ranked":
				rankedData = item
			if item["LeagueDefId"] == "ConquestProvingGrounds":
				conquestPGPlayed = item["NumberOfGamesPlayed"]
				conquestPGStreak = winstreakAddPlusSign(item["WinningStreak"])
			if item["LeagueDefId"] == "ConquestSilver":
				conquestSilverPlayed = item["NumberOfGamesPlayed"]
				conquestSilverStreak = winstreakAddPlusSign(item["WinningStreak"])
			if item["LeagueDefId"] == "ConquestGold":
				conquestGoldPlayed = item["NumberOfGamesPlayed"]
				conquestGoldStreak = winstreakAddPlusSign(item["WinningStreak"])
			if item["LeagueDefId"] == "ConquestInfinity":
				conquestInfinityPlayed = item["NumberOfGamesPlayed"]
				conquestInfinityStreak = winstreakAddPlusSign(item["WinningStreak"])

		if (
			allLeagueData != None
			and rankedData != None
			and "WinningStreak" in rankedData
		):
			rankedCurrentWinStreak = rankedData["WinningStreak"]

		global timeUpdated
		timeUpdated = data["ServerState"]["Account"]["TimeUpdated"]

		global timeStarted
		timeStarted = data["ServerState"]["Account"]["TimeCreated"]

		global cardData
		cardData = data["ServerState"]["Account"]["CardStats"]

		global concedes
		concedes = data["ServerState"]["Account"]["Concedes"]

		global opponentConcedes
		opponentConcedes = data["ServerState"]["Account"]["OpponentConcedes"]

		global snaps
		snaps = data["ServerState"]["Account"]["Snaps"]

		global totalGoldSpent
		totalGoldSpent = data["ServerState"]["Wallet"]["_goldCurrency"]["SpentAmount"]

		global totalCreditsSpent
		totalCreditsSpent = data["ServerState"]["Wallet"]["_creditsCurrency"][
			"SpentAmount"
		]

		global totalCollectorsTokensSpent
		totalCollectorsTokensSpent = data["ServerState"]["Wallet"][
			"_collectorsTokensCurrency"
		]["SpentAmount"]

	with open(collectionPath, encoding="utf-8-sig") as collection_json_file:
		data = json.load(collection_json_file)

		global collectionLvl
		collectionLvl = data["ServerState"]["CollectionScore"]["Amount"]

		global avatarsOwned
		avatarsOwned = len(data["ServerState"]["AvatarInventory"]["OwnedAvatars"])

		global titlesOwned
		titlesOwned = len(data["ServerState"]["TitleInventory"]["OwnedTitles"])

		global cardsOwned
		global cardSplits
		global variants
		allCardsData = data["ServerState"]["Cards"]
		for card in allCardsData:
			if "ArtVariantDefId" not in card and "Split" not in card:
				cardsOwned += 1
			if "Split" in card:
				cardSplits += 1
			if "ArtVariantDefId" in card and "Split" not in card:
				variants += 1

		global cardBacksOwned
		cardBacksOwned = len(data["ServerState"]["CardBacks"])

		global cardUnlockHistory
		cardUnlockHistory = data["ServerState"]["CollectionScoreRewardsClaimedHistory"][
			"ClaimedCards"
		]


def get_snapId():
	return snapId


def get_PlayerName():
	return playerName


def get_standing():
	return standing


def get_skillRating():
	return skillRating


def get_rankedMaxLevel():
	return rankedMaxLevel


def get_rankedMaxLevelCubes():
	return (
		str(rankedMaxLevelCubes) + " cubes"
		if rankedMaxLevelCubes != 1
		else str(rankedMaxLevelCubes) + " cube"
	)


def get_rankedCurrentLevel():
	return rankedCurrentLevel


def get_rankedCurrentLevelCubes():
	return (
		str(rankedCurrentLevelCubes) + " cubes"
		if rankedCurrentLevelCubes != 1
		else str(rankedCurrentLevelCubes) + " cube"
	)


def get_rankedGamesPlayedThisSeason():
	return rankedGamesPlayedThisSeason


def get_rankedWins():
	return rankedWins


def get_rankedLosses():
	return rankedLosses


def get_rankedTies():
	return rankedTies


def get_rankedGames():
	return rankedWins + rankedLosses + rankedTies


def get_rankedWinPrct():
	return "{:.2f}".format(
		(rankedWins / (rankedWins + rankedLosses + rankedTies) * 100)
	)


def get_rankedCurrentWinStreak():
	return winstreakAddPlusSign(rankedCurrentWinStreak)


def get_timeUpdated():
	timestamp = os.path.getmtime(os.path.expanduser(profileFilePath))
	return datetime.datetime.fromtimestamp(timestamp).strftime("%B %d %I:%M %p")


def get_timeStarted():
	return datetime.datetime.strptime(
		timeStarted.split(".")[0], "%Y-%m-%dT%H:%M:%S"
	).strftime("%B %d %Y,  %I:%M %p")


def winstreakAddPlusSign(value):
	if str(value).startswith("-") or value == 0:
		return value
	else:
		return "+" + str(value)


def get_BestCardStats():
	json_dict = json.loads(str(cardData).replace("'", '"'))
	listedCards = ""
	json_dict.pop("$type")
	sorted_dict = dict(
		sorted(json_dict.items(), key=lambda item: item[1], reverse=True)
	)
	for key, value in sorted_dict.items():
		if value > -1:
			cardName = "".join(
				" " + char if char.isupper() else char.strip() for char in key
			).strip()
			listedCards = (
				listedCards + cardName + ": " + str(winstreakAddPlusSign(value)) + "\n"
			)

	return listedCards


def get_WorstCardStats():
	json_dict = json.loads(str(cardData).replace("'", '"'))
	listedCards = ""
	json_dict.pop("$type")
	sorted_dict = dict(sorted(json_dict.items(), key=lambda item: item[1]))
	for key, value in sorted_dict.items():
		if value < 0:
			cardName = "".join(
				" " + char if char.isupper() else char.strip() for char in key
			).strip()
			listedCards = listedCards + cardName + ": " + str(value) + "\n"

	return listedCards


def get_Concedes():
	return concedes


def get_opponentConcedes():
	return opponentConcedes


def get_Snaps():
	return snaps


def get_conquestPGPlayed():
	return conquestPGPlayed


def get_conquestPGStreak():
	return conquestPGStreak


def get_conquestSilverPlayed():
	return conquestSilverPlayed


def get_conquestSilverStreak():
	return conquestSilverStreak


def get_conquestGoldPlayed():
	return conquestGoldPlayed


def get_conquestGoldStreak():
	return conquestGoldStreak


def get_conquestInfinityPlayed():
	return conquestInfinityPlayed


def get_conquestInfinityStreak():
	return conquestInfinityStreak


def get_TotalGoldSpent():
	return totalGoldSpent


def get_TotalCreditsSpent():
	return totalCreditsSpent


def get_TotalCollectorsTokensSpent():
	return totalCollectorsTokensSpent


def get_BattlePassesBought():
	return battlePassesBought


def get_CollectionLvl():
	return collectionLvl


def get_AvatarsOwned():
	return avatarsOwned


def get_TitlesOwned():
	return titlesOwned


def get_CardBacksOwned():
	return cardBacksOwned


def get_CardsOwned():
	return cardsOwned


def get_CardSplits():
	return cardSplits


def get_Variants():
	return variants


def get_CardUnlockHistory():
	# Extract the claimed cards dictionary
	claimed_cards = cardUnlockHistory
	def cardUnlockFilter(c):
		d = c
		return c != '$type'

	filteredHistory = filter(cardUnlockFilter, claimed_cards)
	# sortedCardUnlockHistory = sorted(filteredHistory, key=lambda item: int(item), reverse=False)
	
	# Process the claimed cards into a list of formatted strings
	card_list = []

	# sorted_cards = sorted(claimed_cards, key=lambda item: int(item[0]))

	for cardUnlockRank in filteredHistory:
		# calculatedLvl = int(level)
		if cardUnlockRank == '$type':
			continue
		currentCard = claimed_cards[cardUnlockRank]

		cardName = ''.join(' ' + char if char.isupper() else char for char in currentCard['CardDefId']).strip()
		rarity = currentCard['RarityDefId']
		favorite = 'Yes' if 'Favorite' in currentCard and currentCard['Favorite'] == True else 'No'

		if 'ArtVariantDefId' in currentCard.values():
			cardName += " Variant"
		# I want to create a json object with the rank of the card as the first property, and the card information as the second property
		card = '{"Rank": ' + cardUnlockRank + ', "Card": {"Name": "' + cardName + '", "Rarity": "' + rarity + '", "Favorite": "' + favorite + '"}}'
		card_list.append(json.loads(card))
		# card_list.append(f" {cardUnlockRank} - {cardName}")
	return generate_card_unlock_history(sorted(card_list, key=lambda item: int(item['Rank']), reverse=True))

def generate_card_unlock_history(cards):
	# Number of columns
	num_columns = 3
	# Split cards into columns
	columns = [[] for _ in range(num_columns)]
    
	for i, card in enumerate(cards):
		# Extract the card name and check if it is a favorite
		card_name = card['Card'].get('Name', 'Unknown Card')
		favorite = card['Card'].get('Favorite', False)
        
        # Add HTML formatting for favorite cards
		if favorite == 'Yes':
			card_name = f'<div style="background-color: orange; padding: 5px; margin-bottom: 5px;">{card_name}</div>'
		else:
			card_name = f'<div style="padding: 5px; margin-bottom: 5px;">{card_name}</div>'
        
		if 'ArtVariantDefId' in card['Card']:
			cardName = cardName + " Variant"
		columns[i % num_columns].append(card_name)

    # Create HTML for columns
	html_columns = '<table style="width: 100%; border-collapse: collapse;"><tr>'
	for col in columns:
		html_columns += '<td class="variant-column" style="vertical-align: top; padding: 10px;">'
		html_columns += "".join(col)  # Join with empty string as col now contains HTML divs
		html_columns += '</td>'
	html_columns += '</tr></table>'

	return html_columns
 # for i, card in enumerate(cards):
	# 	columns[i % num_columns].append(card['Card'])

	# # Create HTML for columns
	# html_columns = '<table style="width: 100%;"><tr>'
	# for col in columns:
	# 	html_columns += '<td class="variant-column" style="vertical-align: top;">'
	# 	html_columns += "<br>".join(col)
	# 	html_columns += '</td>'
	# html_columns += '</tr></table>'

	# return html_columns


# def get_CardUnlockHistory():
# 	json_dict = json.loads(str(cardUnlockHistory).replace("'", "\"").replace("True", "\"True\""))
# 	json_dict.pop('$type')
# 	sorted_dict = dict(sorted(json_dict.items(), key=lambda item: int(item[0])))
# 	result = ''

# 	for level in sorted_dict:
# 		calculatedLvl = level
# 		levelB = 4
# 		levelC = 109
# 		cardName = sorted_dict[level]['CardDefId']

# 		if (int(level) > 1 and int(level) < 4):
# 			calculatedLvl = int(level) - 1
# 		if (int(level) == 4):
# 			calculatedLvl = level
# 		if (int(level) > 4):
# 			current = int(level) - levelB
# 			calculatedLvl = levelB + (2 * current)
# 		if (int(level) > 109):
# 			current = int(level) - levelC
# 			calculatedLvl = calculatedLvl + (2 * current)

# 		cardName = ''.join(' ' + char if char.isupper() else char.strip() for char in cardName).strip()

# 		if 'ArtVariantDefId' in sorted_dict[level]:
# 			cardName = cardName + " Variant"
# 		result = result + str(calculatedLvl) + ": " + cardName + "\n"
# 	return result

reload_file()
