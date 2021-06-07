from enum import Enum


class TrainingAndUpgradeLevel(Enum):
    T1 = 0
    T2 = 1
    T3 = 2
    T4 = 3
    T5 = 4
    UPGRADE_ALL = 5
    DISABLED = -1


class BotConfig:
    def __init__(self, config={}):
        self.stopDoRound = config.get('stopDoRound', 1)
        self.enableStop = config.get('enableStop', False)

        self.action_wait_time = config.get('action_wait_time', 1)

        # Break
        self.enableBreak = config.get('enableBreak', True)
        self.breakTime = config.get('breakTime', 60 * 3)
        self.terminate = config.get("terminate", False)
        self.breakDoRound = config.get('breakDoRound', 1)

        self.hasBuildingPos = config.get('hasBuildingPos', False)

        # Mystery Merchant
        self.enableMysteryMerchant = config.get('enableMysteryMerchant', False)

        # Collecting
        self.enableCollecting = config.get('enableCollecting', True)

        # Producing
        self.enableMaterialProduce = config.get('enableMaterialProduce', True)
        self.materialDoRound = config.get('materialDoRound', 1)

        # Tavern
        self.enableTavern = config.get('enableTavern', True)

        # Training
        self.enableTraining = config.get('enableTraining', True)

        self.trainBarracksTrainingLevel = config.get('trainBarracksTrainingLevel',
                                                     TrainingAndUpgradeLevel.T1.value)
        self.trainBarracksUpgradeLevel = config.get('trainBarracksUpgradeLevel',
                                                    TrainingAndUpgradeLevel.T1.value)

        self.trainArcheryRangeTrainingLevel = config.get('trainArcheryRangeTrainingLevel',
                                                         TrainingAndUpgradeLevel.T1.value)
        self.trainArcheryRangeUpgradeLevel = config.get('trainArcheryRangeUpgradeLevel',
                                                        TrainingAndUpgradeLevel.T1.value)

        self.trainStableTrainingLevel = config.get('trainStableTrainingLevel',
                                                   TrainingAndUpgradeLevel.T1.value)
        self.trainStableUpgradeLevel = config.get('trainArcheryRangeUpgradeLevel',
                                                  TrainingAndUpgradeLevel.T1.value)

        self.trainSiegeWorkshopTrainingLevel = config.get('trainSiegeWorkshopTrainingLevel',
                                                          TrainingAndUpgradeLevel.T1.value)
        self.trainSiegeWorkshopUpgradeLevel = config.get('trainSiegeWorkshopUpgradeLevel',
                                                         TrainingAndUpgradeLevel.T1.value)

        # Vip Chest
        self.enableVipClaimChest = config.get('enableVipClaimChest', True)
        self.vipDoRound = config.get('vipDoRound', 1)

        # Quest
        self.claimQuests = config.get('claimQuests', True)
        self.questDoRound = config.get('questDoRound', 1)

        # Alliance
        self.allianceAction = config.get('allianceAction', True)
        self.allianceDoRound = config.get('allianceDoRound', 1)

        # Barbarians
        self.attackBarbarians = config.get('attackBarbarians', False)
        self.numberOfAttack = config.get('numberOfAttack', 1)
        self.barbariansBaseLevel = config.get('barbariansBaseLevel', 1)
        self.barbariansMinLevel = config.get('barbariansMinLevel', 1)
        self.barbariansMaxLevel = config.get('barbariansMaxLevel', 99)
        self.holdPosition = config.get('holdPosition', True)
        self.healTroopsBeforeAttack = config.get('healTroopsBeforeAttack', True)
        self.useDailyAPRecovery = config.get('useDailyAPRecovery', False)
        self.useNormalAPRecovery = config.get('useNormalAPRecovery', False)
        self.timeout = config.get('timeout', 300)

        # Gather resource
        self.useGatheringBoosts = config.get('useGatheringBoosts', False)
        self.gatherResource = config.get('gatherResource', True)
        self.gatherResourceNoSecondaryCommander = config.get('gatherResourceNoSecondaryCommander', True)
        self.gatherResourceRatioFood = config.get('gatherResourceRatioFood', 1)
        self.gatherResourceRatioWood = config.get('gatherResourceRatioWood', 1)
        self.gatherResourceRatioStone = config.get('gatherResourceRatioStone', 1)
        self.gatherResourceRatioGold = config.get('gatherResourceRatioGold', 1)
        self.holdOneQuerySpace = config.get('holdOneQuerySpace', False)

        # Scout
        self.enableScout = config.get('enableScout', False)
        self.enableInvestigation = config.get('enableInvestigation', True)

