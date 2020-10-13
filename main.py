from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import os
import time
import logging
# TODO: Multiprocess serait cool
# from multiprocessing import Process

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMEDRIVER_PATH = os.path.join(ROOT_DIR, 'chromedriver')

#TODO: ajouter ses identifiant et le lien du forum de class
USERNAME = ""
PASSWORD = ""
FORUM_URL = "https://sitescours.monportail.ulaval.ca/ena/site/forums?idSite=119771"

logging.basicConfig(format='%(asctime)s %(message)s')

options = Options()
options.headless = True
driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)
driver.implicitly_wait(3)
wait = WebDriverWait(driver, 3)
MAX_RETRIES = 3


def wrap(func, *args, **kwargs):
    for _ in range(MAX_RETRIES):
        try:
            response = func(*args, **kwargs)
        except:
            continue
        else:
            break
    else:
        print("Aucun sujet détecté")
        return []
    return response


def login():
    print("start login")

    driver.get("https://monportail.ulaval.ca/")
    driver.find_element_by_class_name('mpo-page-publique__bouton').click()

    for _ in range(MAX_RETRIES):
        try:
            inputs = driver.find_elements_by_xpath('//input')
            inputs[0].send_keys(USERNAME)
            inputs[1].send_keys(PASSWORD)
            driver.find_element_by_id('btnSubmit').click()
        except:
            continue
        else:
            break
    else:
        raise RuntimeError("Bloqué sur la page de connexion")
    print("login finish!")


def goToClassSite():
    print(f'going to {FORUM_URL}')
    driver.get(FORUM_URL)
    time.sleep(1)


def goToForumHome():
    print('going to forum')
    driver.switch_to.default_content()
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "MenuSiteCours_Outils_Item_FORU"))).click()


def selectFrameForum():
    print('search forum frame')
    driver.switch_to.default_content()
    for _ in range(MAX_RETRIES):
        try:
            iframe = wait.until(EC.presence_of_element_located((By.ID, "if1")))
            driver.switch_to.frame(iframe)
        except:
            continue
        else:
            break
    else:
        raise RuntimeError("Ne trouve pas l'accueil du forum")


def viewForum():
    time.sleep(3)
    selectFrameForum()
    for v in range(len(wrap(wait.until, EC.presence_of_all_elements_located((By.CLASS_NAME, 'titre-forum'))))):
        forum = wrap(wait.until, EC.presence_of_all_elements_located((By.CLASS_NAME, 'titre-forum')))
        forum[v].click()
        print(v)
        time.sleep(1)
        for y in range(
                len(wrap(wait.until, EC.presence_of_all_elements_located((By.CLASS_NAME, 'Sujet_Forum_Texte'))))):
            for _ in range(MAX_RETRIES):
                try:
                    sousForum = wait.until((EC.presence_of_all_elements_located((By.CLASS_NAME, 'Sujet_Forum_Texte'))))
                    sousForum[y].click()
                    print("    {}".format(y))
                    time.sleep(1)
                    driver.execute_script("window.history.go(-2)")
                except:
                    continue
                else:
                    break

        time.sleep(1)
        driver.execute_script("window.history.go(-1)")


def forumLoop(iteration):
    for i in range(iteration):
        print(f'star iteration {i}')
        selectFrameForum()
        for _ in range(MAX_RETRIES):
            try:
                wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'titre-forum')))[22].click()
            except:
                continue
            else:
                break
        # wrap(wait.until, EC.presence_of_all_elements_located((By.CLASS_NAME, 'titre-forum')))[22].click()
        # time.sleep(1)
        goToForumHome()


if __name__ == "__main__":
    login()
    goToClassSite()
    goToForumHome()
    logging.warning("start")
    forumLoop(1000)
    # for i in range(500):
    #     try:
    #         viewForum()
    #     except:
    #         logging.warning("error loop")
    #         continue
    # logging.warning("end")

