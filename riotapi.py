import os
import requests
from typing import Optional, Literal, List, Any
from merakiapi import GetItemById, SummarizeItem, SummarizeChampion, GetChampionByName


Continent = Literal["AMERICAS", "ASIA", "EUROPE"]


RIOT_API_KEY = os.environ.get("RIOT_API_KEY")


def GetAccount(continent: Continent, game_name: str, tag_line: str) -> Optional[Any]:
    continent = continent.upper()
    response = requests.get(f"https://{continent}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}?api_key={RIOT_API_KEY}")
    if response.status_code == 200:
        return response.json()


def GetMatchIds(continent: Continent, puuid: str) -> Optional[List[str]]:
    continent = continent.upper()
    response = requests.get(f"https://{continent}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=20&api_key={RIOT_API_KEY}")
    if response.status_code == 200:
        return response.json()


def GetMatch(continent: Continent, match_id: str) -> Optional[Any]:
    continent = continent.upper()
    response = requests.get(f"https://{continent}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={RIOT_API_KEY}")
    if response.status_code == 200:
        return response.json()


def GetParticipant(match: Any, puuid: str) -> Optional[Any]:
    for participant in match["info"]["participants"]:
        if participant["puuid"] == puuid:
            return participant


USER_FIELDS = [
    "championName", "teamPosition", "teamId", "assists", "baronKills",
    "bountyLevel", "champExperience", "champLevel", "damageDealtToBuildings",
    "damageDealtToObjectives", "damageDealtToTurrets", "damageSelfMitigated",
    "deaths", "detectorWardsPlaced", "doubleKills", "dragonKills",
    "firstBloodAssist", "firstBloodKill", "firstTowerAssist", "firstTowerKill",
    "gameEndedInSurrender", "goldEarned", "goldSpent", "inhibitorKills",
    "inhibitorTakedowns", "inhibitorsLost", "item0", "item1", "item2",
    "item3", "item4", "item5", "item6", "largestKillingSpree",
    "largestMultiKill", "longestTimeSpentLiving", "magicDamageDealt",
    "magicDamageDealtToChampions", "magicDamageTaken", "neutralMinionsKilled",
    "objectivesStolen", "objectivesStolenAssists", "pentaKills",
    "physicalDamageDealt", "physicalDamageDealtToChampions", "physicalDamageTaken",
    "quadraKills", "sightWardsBoughtInGame", "spell1Casts", "spell2Casts",
    "spell3Casts", "spell4Casts", "summoner1Casts", "summoner2Casts",
    "teamEarlySurrendered", "puuid", "kills"
]


USER_CHALLENGE_FIELDS = [
    "12AssistStreakCount", "baronBuffGoldAdvantageOverThreshold",
    "controlWardTimeCoverageInRiverOrEnemyHalf", "earliestBaron",
    "earliestDragonTakedown", "earliestElderDragon",
    "earlyLaningPhaseGoldExpAdvantage", "fasterSupportQuestCompletion",
    "fastestLegendary", "hadAfkTeammate", "highestChampionDamage",
    "highestCrowdControlScore", "highestWardKills", "junglerKillsEarlyJungle",
    "killsOnLanersEarlyJungleAsJungler", "laningPhaseGoldExpAdvantage",
    "legendaryCount", "maxCsAdvantageOnLaneOpponent",
    "maxLevelLeadLaneOpponent", "mostWardsDestroyedOneSweeper",
    "mythicItemUsed", "playedChampSelectPosition", "soloTurretsLategame",
    "takedownsFirst25Minutes", "teleportTakedowns",
    "thirdInhibitorDestroyedTime", "threeWardsOneSweeperCount",
    "visionScoreAdvantageLaneOpponent", "InfernalScalePickup",
    "fistBumpParticipation", "voidMonsterKill", "abilityUses",
    "acesBefore15Minutes", "alliedJungleMonsterKills", "baronTakedowns",
    "blastConeOppositeOpponentCount", "bountyGold", "buffsStolen",
    "completeSupportQuestInTime", "controlWardsPlaced", "damagePerMinute",
    "damageTakenOnTeamPercentage", "dancedWithRiftHerald", "deathsByEnemyChamps",
    "dodgeSkillShotsSmallWindow", "doubleAces", "dragonTakedowns",
    "legendaryItemUsedList", "effectiveHealAndShielding",
    "elderDragonKillsWithOpposingSoul", "elderDragonMultikills",
    "enemyChampionImmobilizations", "enemyJungleMonsterKills",
    "epicMonsterKillsNearEnemyJungler", "epicMonsterKillsWithin30SecondsOfSpawn",
    "epicMonsterSteals", "epicMonsterStolenWithoutSmite", "firstTurretKilled",
    "firstTurretKilledTime", "flawlessAces", "fullTeamTakedown", "gameLength",
    "getTakedownsInAllLanesEarlyJungleAsLaner", "goldPerMinute",
    "hadOpenNexus", "immobilizeAndKillWithAlly", "initialBuffCount",
    "initialCrabCount", "jungleCsBefore10Minutes",
    "junglerTakedownsNearDamagedEpicMonster", "kda", "killAfterHiddenWithAlly",
    "killedChampTookFullTeamDamageSurvived", "killingSprees",
    "killParticipation", "killsNearEnemyTurret",
    "killsOnOtherLanesEarlyJungleAsLaner", "killsOnRecentlyHealedByAramPack",
    "killsUnderOwnTurret", "killsWithHelpFromEpicMonster",
    "knockEnemyIntoTeamAndKill", "kTurretsDestroyedBeforePlatesFall",
    "landSkillShotsEarlyGame", "laneMinionsFirst10Minutes", "lostAnInhibitor",
    "maxKillDeficit", "mejaisFullStackInTime", "moreEnemyJungleThanOpponent",
    "multiKillOneSpell", "multikills", "multikillsAfterAggressiveFlash",
    "multiTurretRiftHeraldCount", "outerTurretExecutesBefore10Minutes",
    "outnumberedKills", "outnumberedNexusKill", "perfectDragonSoulsTaken",
    "perfectGame", "pickKillWithAlly", "poroExplosions", "quickCleanse",
    "quickFirstTurret", "quickSoloKills", "riftHeraldTakedowns",
    "saveAllyFromDeath", "scuttleCrabKills", "shortestTimeToAceFromFirstTakedown",
    "skillshotsDodged", "skillshotsHit", "snowballsHit", "soloBaronKills",
    "SWARM_DefeatAatrox", "SWARM_DefeatBriar", "SWARM_DefeatMiniBosses",
    "SWARM_EvolveWeapon", "SWARM_Have3Passives", "SWARM_KillEnemy",
    "SWARM_PickupGold", "SWARM_ReachLevel50", "SWARM_Survive15Min",
    "SWARM_WinWith5EvolvedWeapons", "soloKills", "stealthWardsPlaced",
    "survivedSingleDigitHpCount", "survivedThreeImmobilizesInFight",
    "takedownOnFirstTurret", "takedowns", "takedownsAfterGainingLevelAdvantage",
    "takedownsBeforeJungleMinionSpawn", "takedownsFirstXMinutes",
    "takedownsInAlcove", "takedownsInEnemyFountain", "teamBaronKills",
    "teamDamagePercentage", "teamElderDragonKills", "teamRiftHeraldKills",
    "tookLargeDamageSurvived", "turretPlatesTaken",
    "turretsTakenWithRiftHerald", "turretTakedowns",
    "twentyMinionsIn3SecondsCount", "twoWardsOneSweeperCount",
    "unseenRecalls", "visionScorePerMinute", "wardsGuarded",
    "wardTakedowns", "wardTakedownsBefore20Min"
]


ITEM_KEYS = ["item0", "item1", "item2", "item3", "item4", "item5", "item6"]


def SummarizeParticipant(participant_data: Any) -> Any:
    participant = {field: participant_data.get(field) for field in USER_FIELDS}
    participant["challenges"] = {field: participant_data["challenges"].get(field) for field in USER_CHALLENGE_FIELDS}
    return participant


def SummarizeMatch(match, puuid: str) -> Any:
    participants = []
    for participant_data in match["info"]["participants"]:
        participants.append(
            SummarizeParticipant(participant_data)
        )

    user = next((participant for participant in participants if participant["puuid"] == puuid), None)
    if user:
        champion_info = GetChampionByName(user["championName"])
        if champion_info:
            user["championInfo"] = SummarizeChampion(champion_info)

        for key in ITEM_KEYS:
            if key in user:
                item = GetItemById(user[key])
                if item:
                    user[key] = SummarizeItem(item)

    return {
        "user": user,
        "players": [{
            "championName": participant["championName"],
            "teamPosition": participant["teamPosition"],
            "teamId": participant["teamId"],
            "puuid": participant["puuid"]
        } for participant in participants]
    }