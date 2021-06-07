from enum import Enum
from filepath.constants import *


class StrImagePosition(Enum):
    WINDOWS_TITLE = (305, 68, 975, 100)


class FilePaths(Enum):
    TEST_SRC_FOLDER_PATH = 'test_screen_caps\\'
    TEST_CURR_SCREEN_CAP_PATH = 'test_screen_caps\\current_cap.png'
    ADB_EXE_PATH = 'adb\\adb.exe'
    TESSERACT_EXE_PATH = 'tesseract\\tesseract.exe'
    TESSDATA_CHI_SIM_PATH = 'tessdata\\chi_sim.traineddata'
    SAVE_FOLDER_PATH = 'save\\'


class BuffsImageAndProps(Enum):
    ENHANCED_GATHER_BLUE = ['resource\\buffs\\enhanced_gathering_blue.png',
                            (1280, 720), (0, 0, 0, 0), 0.70, 25, BOOSTS]
    ENHANCED_GATHER_PURPLE = ['resource\\buffs\\enhanced_gathering_purple.png',
                              (1280, 720), (0, 0, 0, 0), 0.70, 25, BOOSTS]


class ItemsImageAndProps(Enum):
    ENHANCED_GATHER_BLUE = ['resource\\items\\enhanced_gathering_blue.png',
                            (1280, 720), (0, 0, 0, 0), 0.70, 25, BOOSTS]
    ENHANCED_GATHER_PURPLE = ['resource\\items\\enhanced_gathering_blue.png',
                              (1280, 720), (0, 0, 0, 0), 0.70, 25, BOOSTS]


class ImagePathAndProps(Enum):
    MAP_BUTTON_IMG_PATH = ['resource\\map_button.png',
                           (1280, 720), (10, 602, 113, 709), 0.98, 25, HOME]
    HOME_BUTTON_IMG_PATH = ['resource\\home_button.png',
                            (1280, 720), (10, 602, 113, 709), 0.98, 25, MAP]
    GREEN_HOME_BUTTON_IMG_PATH = ['resource\\green_home_button.png',
                                  (1280, 720), (0, 0, 0, 0), 0.70, 25, GREEN_HOME]
    WINDOW_IMG_PATH = ['resource\\window.png',
                       (1280, 720), (1065, 56, 1128, 112), 0.70, 25, WINDOW]
    WINDOW_TITLE_MARK_IMG_PATH = ['resource\\window_title_mark.png',
                                  (1280, 720), (1065, 56, 1128, 112), 0.70, 25, WINDOW_TITLE]
    BUILDING_TITLE_MARK_IMG_PATH = ['resource\\building_title_left.png',
                                    (1280, 720), (0, 0, 0, 0), 0.70, 25, BUILDING_TITLE]
    BUILDING_INFO_BUTTON_IMG_PATH = ['resource\\building_info_button.png',
                                     (1280, 720), (0, 0, 0, 0), 0.80, 25, BUILDING_INFO]
    MENU_OPENED_IMAGE_PATH = ['resource\\menu_opened.png',
                              (1280, 720), (0, 0, 0, 0), 0.90, 25, MENU_OPENED_IMAGE]
    MENU_BUTTON_IMAGE_PATH = ['resource\\menu_button.png',
                              (1280, 720), (1204, 646, 1257, 693), 0.90, 25, MENU_IMAGE]
    QUEST_CLAIM_BUTTON_IMAGE_PATH = ['resource\\quests_claim_button.png',
                                     (1280, 720), (0, 0, 0, 0), 0.90, 25, CLAIM_BUTTON]
    BARRACKS_BUTTON_IMAGE_PATH = ['resource\\barracks_button.png',
                                  (1280, 720), (0, 0, 0, 0), 0.90, 25, BARRACKS_BUTTON]
    ARCHER_RANGE_BUTTON_IMAGE_PATH = ['resource\\archery_range_button.png',
                                      (1280, 720), (0, 0, 0, 0), 0.90, 25, ARCHER_RANGE_BUTTON]
    STABLE_BUTTON_IMAGE_PATH = ['resource\\stable_button.png',
                                (1280, 720), (0, 0, 0, 0), 0.90, 25, STABLE_BUTTON]
    SIEGE_WORKSHOP_BUTTON_IMAGE_PATH = ['resource\\siege_workshop_button.png',
                                        (1280, 720), (0, 0, 0, 0), 0.90, 25, SIEGE_WORKSHOP_BUTTON]
    TRAINING_UPGRADE_BUTTON_IMAGE_PATH = ['resource\\training_upgrade_button.png',
                                          (1280, 720), (0, 0, 0, 0), 0.90, 25, TRAINING_UPGRADE_BUTTON]
    TRAIN_BUTTON_IMAGE_PATH = ['resource\\train_button.png',
                               (1280, 720), (0, 0, 0, 0), 0.90, 25, TRAIN_BUTTON]
    UPGRADE_BUTTON_IMAGE_PATH = ['resource\\upgrade_button.png',
                                 (1280, 720), (0, 0, 0, 0), 0.90, 25, UPGRADE_BUTTON]
    SPEED_UP_BUTTON_IMAGE_PATH = ['resource\\speed_up_button.png',
                                  (1280, 720), (0, 0, 0, 0), 0.90, 25, SPEED_UP]
    DECREASING_BUTTON_IMAGE_PATH = ['resource\\decreasing_button.png',
                                    (1280, 720), (0, 0, 0, 0), 0.90, 25, DECREASING]
    INCREASING_BUTTON_IMAGE_PATH = ['resource\\increasing_button.png',
                                    (1280, 720), (0, 0, 0, 0), 0.90, 25, INCREASING]
    LOCK_BUTTON_IMAGE_PATH = ['resource\\lock_button.png',
                                    (1280, 720), (0, 0, 0, 0), 0.90, 25, LOCK]
    RESOURCE_SEARCH_BUTTON_IMAGE_PATH = ['resource\\resource_search_button.png',
                                         (1280, 720), (0, 0, 0, 0), 0.90, 25, RESOURCE_SEARCH]
    RESOURCE_GATHER_BUTTON_IMAGE_PATH = ['resource\\resource_gather_button.png',
                                         (1280, 720), (0, 0, 0, 0), 0.90, 25, RESOURCE_GATHER]
    NEW_TROOPS_BUTTON_IMAGE_PATH = ['resource\\new_troops_button.png',
                                    (1280, 720), (0, 0, 0, 0), 0.90, 25, NEW_TROOPS]
    TROOPS_MATCH_BUTTON_IMAGE_PATH = ['resource\\troops_match_button.png',
                                      (1280, 720), (0, 0, 0, 0), 0.90, 25, TROOPS_MATCH]
    VERIFICATION_CHEST_BUTTON_IMAGE_PATH = ['resource\\verification_chest_button.png',
                                            (1280, 720), (0, 0, 0, 0), 0.90, 25, VERIFICATION_CHEST]
    VERIFICATION_VERIFY_BUTTON_IMAGE_PATH = ['resource\\verification_verify_button.png',
                                             (1280, 720), (0, 0, 0, 0), 0.90, 25, VERIFICATION_VERIFY]
    VERIFICATION_CLOSE_REFRESH_OK_BUTTON_IMAGE_PATH = ['resource\\verification_close_refresh_ok_button.png',
                                                       (1280, 720), (0, 0, 0, 0), 0.90, 25,
                                                       VERIFICATION_CLOSE_REFRESH_OK]
    GIFTS_CLAIM_BUTTON_IMAGE_PATH = ['resource\\alliance_gifts_claim_button.png',
                                     (1280, 720), (0, 0, 0, 0), 0.90, 25, GIFTS_CLAIM]
    TECH_RECOMMEND_IMAGE_PATH = ['resource\\alliance_tech_recommend.png',
                                 (1280, 720), (0, 0, 0, 0), 0.90, 25, TECH_RECOMMEND]
    TECH_DONATE_BUTTON_IMAGE_PATH = ['resource\\alliance_tech_donate.png',
                                     (1280, 720), (0, 0, 0, 0), 0.90, 25, TECH_DONATE]
    MATERIALS_PRODUCTION_BUTTON_IMAGE_PATH = ['resource\\materials_production_button.png',
                                              (1280, 720), (0, 0, 0, 0), 0.90, 25, MATERIALS_PRODUCTION]
    TAVERN_BUTTON_BUTTON_IMAGE_PATH = ['resource\\tavern_button.png',
                                       (1280, 720), (0, 0, 0, 0), 0.90, 25, TAVERN_BUTTON]
    CHEST_OPEN_BUTTON_IMAGE_PATH = ['resource\\chest_open_button.png',
                                    (1280, 720), (0, 0, 0, 0), 0.90, 25, CHEST_OPEN]
    CHEST_CONFIRM_BUTTON_IMAGE_PATH = ['resource\\chest_confirm_button.png',
                                       (1280, 720), (0, 0, 0, 0), 0.90, 25, CHEST_CONFIRM]
    ATTACK_BUTTON_POS_IMAGE_PATH = ['resource\\attack_button.png',
                                       (1280, 720), (0, 0, 0, 0), 0.90, 25, ATTACK_BUTTON]
    HOLD_POS_CHECKED_IMAGE_PATH = ['resource\\hold_posistion_checked.png',
                                    (1280, 720), (0, 0, 0, 0), 0.90, 25, HOLD_POS_CHECKED]
    HOLD_POS_UNCHECK_IMAGE_PATH = ['resource\\hold_position_unchecked.png',
                                   (1280, 720), (0, 0, 0, 0), 0.90, 25, HOLD_POS_UNCHECK]
    UNSELECT_BLUE_ONE_SAVE_BUTTON_IMAGE_PATH = ['resource\\unselect_save_blue_one.png',
                                   (1280, 720), (0, 0, 0, 0), 0.95, 25,  UNSELECT_BLUE_ONE]
    SELECTED_BLUE_ONE_SAVE_BUTTON_IMAGE_PATH = ['resource\\selected_save_blue_one.png',
                                                (1280, 720), (0, 0, 0, 0), 0.95, 25, SELECTED_BLUE_ONE]
    SAVE_SWITCH_BUTTON_IMAGE_PATH = ['resource\\switch_save.png',
                                                (1280, 720), (0, 0, 0, 0), 0.90, 25, SAVE_SWITCH]
    VICTORY_MAIL_IMAGE_PATH = ['resource\\victory_mail.png',
                                     (1280, 720), (0, 0, 0, 0), 0.90, 25, VICTORY_MAIL]
    DEFEAT_MAIL_IMAGE_PATH = ['resource\\defeat_mail.png',
                               (1280, 720), (0, 0, 0, 0), 0.90, 25, DEFEAT_MAIL]
    RETURN_BUTTON_IMAGE_PATH = ['resource\\return_button.png',
                              (1280, 720), (0, 0, 0, 0), 0.90, 25, RETURN_BUTTON]
    HOLD_ICON_IMAGE_PATH = ['resource\\hold_icon.png',
                              (1280, 720), (0, 0, 0, 0), 0.90, 25, HOLD_ICON]
    HOLD_ICON_SMALL_IMAGE_PATH = ['resource\\hold_icon_small.png',
                              (1280, 720), (0, 0, 0, 0), 0.90, 25, HOLD_ICON_SMALL]
    MARCH_BAR_IMAGE_PATH = ['resource\\march_bar.png',
                              (1280, 720), (0, 0, 0, 0), 0.90, 25, MARCH_BAR]
    HEAL_ICON_IMAGE_PATH = ['resource\\heal_icon.png',
                              (1280, 720), (0, 0, 0, 0), 0.80, 25, HEAL_ICON]
    DAILY_AP_CLAIM_BUTTON_IMAGE_PATH = ['resource\\daily_ap_claim.png',
                                     (1280, 720), (0, 0, 0, 0), 0.90, 25, DAILY_AP_CLAIM]
    USE_AP_BUTTON_IMAGE_PATH = ['resource\\use_ap.png',
                                     (1280, 720), (0, 0, 0, 0), 0.90, 25, USE_AP]
    SCOUT_BUTTON_IMAGE_PATH = ['resource\\scout_button.png',
                                     (1280, 720), (0, 0, 0, 0), 0.90, 25, SCOUT_BUTTON]
    SCOUT_EXPLORE_BUTTON_IMAGE_PATH = ['resource\\explore_button.png',
                                     (1280, 720), (0, 0, 0, 0), 0.90, 25, EXPLORE_BUTTON]
    SCOUT_EXPLORE2_BUTTON_IMAGE_PATH = ['resource\\explore_button2.png',
                                     (1280, 720), (0, 0, 0, 0), 0.90, 25, EXPLORE_BUTTON2]
    SCOUT_SEND_BUTTON_IMAGE_PATH = ['resource\\scout_send_button.png',
                                     (1280, 720), (0, 0, 0, 0), 0.90, 25, SEND_BUTTON]
    MAIL_EXPLORATION_REPORT_IMAGE_PATH = ['resource\\mail_exploration_report.png',
                                     (1280, 720), (0, 0, 0, 0), 0.90, 25, MAIL_EXPLORATION_REPORT]
    MAIL_SCOUT_BUTTON_IMAGE_PATH = ['resource\\mail_scout_button.png',
                                     (1280, 720), (0, 0, 0, 0), 0.90, 25, MAIL_SCOUT_BUTTON]
    INVESTIGATE_BUTTON_IMAGE_PATH = ['resource\\investigate_button.png',
                                     (1280, 720), (0, 0, 0, 0), 0.90, 25, INVESTIGATE_BUTTON]
    GREAT_BUTTON_IMAGE_PATH = ['resource\\great_button.png',
                                     (1280, 720), (0, 0, 0, 0), 0.90, 25, GREAT_BUTTON]
    SCOUT_IDLE_ICON_IMAGE_PATH = ['resource\\scout_idle_icon.png',
                                     (1280, 720), (0, 0, 0, 0), 0.80, 25, IDLE_ICON]
    SCOUT_ZZ_ICON_IMAGE_PATH = ['resource\\scout_zz_icon.png',
                                     (1280, 720), (0, 0, 0, 0), 0.80, 25, ZZ_ICON]
    MERCHANT_ICON_IMAGE_PATH = ['resource\\merchant_icon.png',
                                     (1280, 720), (0, 0, 0, 0), 0.80, 25, MERCHANT_ICON]
    MERCHANT_FREE_BTN_IMAGE_PATH = ['resource\\merchant_free_btn.png',
                                     (1280, 720), (0, 0, 0, 0), 0.80, 25, MERCHANT_FREE_BTN]
    MERCHANT_BUY_WITH_WOOD_IMAGE_PATH = ['resource\\merchant_buy_with_wood.png',
                                    (1280, 720), (0, 0, 0, 0), 0.80, 25, MERCHANT_BUY_WITH_WOOD]
    MERCHANT_BUY_WITH_FOOD_IMAGE_PATH = ['resource\\merchant_buy_with_food.png',
                                    (1280, 720), (0, 0, 0, 0), 0.80, 25, MERCHANT_BUY_WITH_FOOD]
    HAS_MATCH_QUERY_IMAGE_PATH = ['resource\\has_match_query.png',
                                    (1280, 720), (0, 0, 0, 0), 0.80, 25, HAS_MATCH_QUERY]
    VERIFICATION_VERIFY_TITLE_IMAGE_PATH = ['resource\\verification_verify_title.png',
                                             (1280, 720), (0, 0, 0, 0), 0.90, 25, VERIFICATION_VERIFY_TITLE]

class GuiCheckImagePathAndProps(Enum):
    VERIFICATION_VERIFY_BUTTON_IMAGE_PATH = ['resource\\verification_verify_button.png',
                                             (1280, 720), (0, 0, 0, 0), 0.90, 25, VERIFICATION_VERIFY]
    MAP_BUTTON_IMG_PATH = ['resource\\map_button_0.png',
                           (1280, 720), (10, 602, 113, 709), 0.98, 25, HOME]
    HOME_BUTTON_IMG_PATH = ['resource\\home_button_0.png',
                            (1280, 720), (10, 602, 113, 709), 0.98, 25, MAP]
    WINDOW_IMG_PATH = ['resource\\window.png',
                       (1280, 720), (0, 0, 0, 0), 0.70, 25, WINDOW]


GuiCheckImagePathAndPropsOrdered = [
    # GuiCheckImagePathAndProps.VERIFICATION_CLOSE_REFRESH_OK_BUTTON_IMAGE_PATH,
    GuiCheckImagePathAndProps.VERIFICATION_VERIFY_BUTTON_IMAGE_PATH,
    GuiCheckImagePathAndProps.MAP_BUTTON_IMG_PATH,
    GuiCheckImagePathAndProps.HOME_BUTTON_IMG_PATH,
    GuiCheckImagePathAndProps.WINDOW_IMG_PATH
]