from enum import Enum


class StrImagePosition(Enum):
    WINDOWS_TITLE = (305, 68, 975, 100)


class FilePaths(Enum):
    TEST_SRC_FOLDER_PATH = 'test_screen_caps\\'
    TEST_CURR_SCREEN_CAP_PATH = 'test_screen_caps\\current_cap.png'
    ADB_EXE_PATH = 'adb\\adb.exe'
    TESSERACT_EXE_PATH = 'tesseract\\tesseract.exe'
    TESSDATA_CHI_SIM_PATH = 'tessdata\\chi_sim.traineddata'
    BUILDING_POS_FOLDER_PATH = 'building_pos\\'


class ImagePathAndProps(Enum):
    MAP_BUTTON_IMG_PATH = ['resource\\map_button.png',
                           (1280, 720), (10, 602, 113, 709), 0.70, 25, 'HOME']
    HOME_BUTTON_IMG_PATH = ['resource\\home_button.png',
                            (1280, 720), (10, 602, 113, 709), 0.70, 25, 'MAP']
    GREEN_HOME_BUTTON_IMG_PATH = ['resource\\green_home_button.png',
                                  (1280, 720), (0, 0, 0, 0), 0.70, 25, 'GREEN_HOME']
    WINDOW_IMG_PATH = ['resource\\window.png',
                       (1280, 720), (1065, 56, 1128, 112), 0.70, 25, 'WINDOW']
    WINDOW_TITLE_MARK_IMG_PATH = ['resource\\window_title_mark.png',
                                  (1280, 720), (1065, 56, 1128, 112), 0.70, 25, 'WINDOW_TITLE']
    BUILDING_TITLE_MARK_IMG_PATH = ['resource\\building_title_left.png',
                                    (1280, 720), (0, 0, 0, 0), 0.70, 25, 'BUILDING_TITLE']
    BUILDING_INFO_BUTTON_IMG_PATH = ['resource\\building_info_button.png',
                                     (1280, 720), (0, 0, 0, 0), 0.80, 25, 'BUILDING_INFO']
    MENU_OPENED_IMAGE_PATH = ['resource\\menu_opened.png',
                              (1280, 720), (0, 0, 0, 0), 0.90, 25, 'MENU_OPENED_IMAGE_PATH']
    MENU_BUTTON_IMAGE_PATH = ['resource\\menu_button.png',
                              (1280, 720), (1204, 646, 1257, 693), 0.90, 25, 'BUILDING_INFO']
    QUEST_CLAIM_BUTTON_IMAGE_PATH = ['resource\\quests_claim_button.png',
                                     (1280, 720), (0, 0, 0, 0), 0.90, 25, 'CLAIM_BUTTON']
    BARRACKS_BUTTON_IMAGE_PATH = ['resource\\barracks_button.png',
                                  (1280, 720), (0, 0, 0, 0), 0.90, 25, 'BARRACKS_BUTTON']
    ARCHER_RANGE_BUTTON_IMAGE_PATH = ['resource\\archery_range_button.png',
                                      (1280, 720), (0, 0, 0, 0), 0.90, 25, 'ARCHER_RANGE_BUTTON']
    STABLE_BUTTON_IMAGE_PATH = ['resource\\stable_button.png',
                                (1280, 720), (0, 0, 0, 0), 0.90, 25, 'STABLE_BUTTON']
    SIEGE_WORKSHOP_BUTTON_IMAGE_PATH = ['resource\\siege_workshop_button.png',
                                        (1280, 720), (0, 0, 0, 0), 0.90, 25, 'SIEGE_WORKSHOP_BUTTON']
    TRAINING_UPGRADE_BUTTON_IMAGE_PATH = ['resource\\training_upgrade_button.png',
                                          (1280, 720), (0, 0, 0, 0), 0.90, 25, 'TRAINING_UPGRADE_BUTTON']
    TRAIN_BUTTON_IMAGE_PATH = ['resource\\train_button.png',
                               (1280, 720), (0, 0, 0, 0), 0.90, 25, 'TRAIN_BUTTON']
    UPGRADE_BUTTON_IMAGE_PATH = ['resource\\upgrade_button.png',
                               (1280, 720), (0, 0, 0, 0), 0.90, 25, 'UPGRADE_BUTTON']
    SPEED_UP_BUTTON_IMAGE_PATH = ['resource\\speed_up_button.png',
                                  (1280, 720), (0, 0, 0, 0), 0.90, 25, 'SPEED_UP']
    DECREASING_BUTTON_IMAGE_PATH = ['resource\\decreasing_button.png',
                                    (1280, 720), (0, 0, 0, 0), 0.90, 25, 'DECREASING']
    INCREASING_BUTTON_IMAGE_PATH = ['resource\\increasing_button.png',
                                    (1280, 720), (0, 0, 0, 0), 0.90, 25, 'INCREASING']
    RESOURCE_SEARCH_BUTTON_IMAGE_PATH = ['resource\\resource_search_button.png',
                                         (1280, 720), (0, 0, 0, 0), 0.90, 25, 'RESOURCE_SEARCH']
    RESOURCE_GATHER_BUTTON_IMAGE_PATH = ['resource\\resource_gather_button.png',
                                         (1280, 720), (0, 0, 0, 0), 0.90, 25, 'RESOURCE_GATHER']
    NEW_TROOPS_BUTTON_IMAGE_PATH = ['resource\\new_troops_button.png',
                                    (1280, 720), (0, 0, 0, 0), 0.90, 25, 'NEW_TROOPS']
    TROOPS_MATCH_BUTTON_IMAGE_PATH = ['resource\\troops_match_button.png',
                                      (1280, 720), (0, 0, 0, 0), 0.90, 25, 'TROOPS_MATCH']
    VERIFICATION_CHEST_BUTTON_IMAGE_PATH = ['resource\\verification_chest_button.png',
                                            (1280, 720), (0, 0, 0, 0), 0.90, 25, 'VERIFICATION_CHEST']
    VERIFICATION_VERIFY_BUTTON_IMAGE_PATH = ['resource\\verification_verify_button.png',
                                             (1280, 720), (0, 0, 0, 0), 0.90, 25, 'VERIFICATION_VERIFY']
    VERIFICATION_CLOSE_REFRESH_OK_BUTTON_IMAGE_PATH = ['resource\\verification_close_refresh_ok_button.png',
                                                       (1280, 720), (0, 0, 0, 0), 0.90, 25,
                                                       ' VERIFICATION_CLOSE_REFRESH_OK']
    GIFTS_CLAIM_BUTTON_IMAGE_PATH = ['resource\\alliance_gifts_claim_button.png',
                          (1280, 720), (0, 0, 0, 0), 0.90, 25, 'GIFTS_CLAIM']
    TECH_RECOMMEND_IMAGE_PATH = ['resource\\alliance_tech_recommend.png',
                          (1280, 720), (0, 0, 0, 0), 0.90, 25, 'TECH_RECOMMEND']
    TECH_DONATE_BUTTON_IMAGE_PATH = ['resource\\alliance_tech_donate.png',
                          (1280, 720), (0, 0, 0, 0), 0.90, 25, 'TECH_DONATE']
    MATERIALS_PRODUCTION_BUTTON_IMAGE_PATH = ['resource\\materials_production_button.png',
                          (1280, 720), (0, 0, 0, 0), 0.90, 25, 'MATERIALS_PRODUCTION']
    TAVERN_BUTTON_BUTTON_IMAGE_PATH = ['resource\\tavern_button.png',
                          (1280, 720), (0, 0, 0, 0), 0.90, 25, 'TAVERN_BUTTON']
    CHEST_OPEN_BUTTON_IMAGE_PATH = ['resource\\chest_open_button.png',
                          (1280, 720), (0, 0, 0, 0), 0.90, 25, 'CHEST_OPEN']
    CHEST_CONFIRM_BUTTON_IMAGE_PATH = ['resource\\chest_confirm_button.png',
                          (1280, 720), (0, 0, 0, 0), 0.90, 25, 'CHEST_CONFIRM']


class GuiCheckImagePathAndProps(Enum):
    VERIFICATION_CLOSE_REFRESH_OK_BUTTON_IMAGE_PATH = ['resource\\verification_close_refresh_ok_button.png',
                                                       (1280, 720), (0, 0, 0, 0), 0.90, 25,
                                                       'VERIFICATION_CLOSE_REFRESH_OK']
    VERIFICATION_VERIFY_BUTTON_IMAGE_PATH = ['resource\\verification_verify_button.png',
                                             (1280, 720), (0, 0, 0, 0), 0.90, 25, 'VERIFICATION_VERIFY']

    # VERIFICATION_CHEST_BUTTON_IMAGE_PATH = ['resource\\verification_chest_button.png',
    #                                         (1280, 720), (0, 0, 0, 0), 0.90, 25, 'VERIFICATION_CHEST']
    MAP_BUTTON_IMG_PATH = ['resource\\map_button_0.png',
                           (1280, 720), (10, 602, 113, 709), 0.90, 25, 'HOME']
    HOME_BUTTON_IMG_PATH = ['resource\\home_button_0.png',
                            (1280, 720), (10, 602, 113, 709), 0.90, 25, 'MAP']
    WINDOW_IMG_PATH = ['resource\\window.png',
                       (1280, 720), (0, 0, 0, 0), 0.70, 25, 'WINDOW']
