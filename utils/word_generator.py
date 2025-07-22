import xml.etree.ElementTree as ET
import zipfile
import shutil
import os

from repositories.RunnerRepository import RunnerRepository
from repositories.SettingRepository import SettingRepository
from repositories.CategoryRepository import CategoryRepository
from constants import file_data

runner_repository = RunnerRepository()
setting_repository = SettingRepository()
category_repository = CategoryRepository()

def create_word_file():
    old_text_list = []
    new_text_list = []
    rewards = get_rewards()
    for reward in rewards:
        sex = reward.sex if reward.sex != "M" else "H"
        old_text_list.append("R" + reward.category + sex)
        new_text_list.append(str(reward.ranking))
        old_text_list.append("L" + reward.category + sex)
        new_text_list.append(reward.last_name)
        old_text_list.append("F" + reward.category + sex)
        new_text_list.append(reward.first_name)
        old_text_list.append("T" + reward.category + sex)
        new_text_list.append(reward.time)
    replace_text_in_document(old_text_list, new_text_list)

def replace_text_in_document(old_text_list, new_text_list):
    unzip_docx(file_data.EMPTY_WORD_FILENAME, file_data.TEMP_FILENAME)
    xml_file_path = os.path.join(file_data.TEMP_FILENAME, 'word/document.xml')
    for old, new in zip(old_text_list, new_text_list):
        replace_flag_in_xml(xml_file_path, old, new)
    zip_dir(file_data.TEMP_FILENAME, file_data.FINAL_WORD_FILENAME)
    shutil.rmtree(file_data.TEMP_FILENAME)

def unzip_docx(docx_path, extract_to):
    with zipfile.ZipFile(docx_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def zip_dir(directory, zip_file):
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, directory)
                zipf.write(file_path, arcname)

def replace_flag_in_xml(file_path, flag, value):
    tree = ET.parse(file_path)
    root = tree.getroot()
    for elem in root.iter():
        if elem.text and flag in elem.text:
            elem.text = elem.text.replace(flag, value if value != None else "")
    tree.write(file_path)

def get_rewards():
    number_scratch_m = setting_repository.get_number_scratch_m()
    number_scratch_f = setting_repository.get_number_scratch_f()
    rewards = []
    get_rewards_in_scratch(rewards, 'M', number_scratch_m)
    get_rewards_in_scratch(rewards, 'F', number_scratch_f)
    for category in category_repository.get_by_sex('F'):
        get_rewards_in_category(rewards, category.category, 'F', number_scratch_f)
    for category in category_repository.get_by_sex('M'):
        get_rewards_in_category(rewards, category.category, 'M', number_scratch_m)
    bib_number_rewarded = [reward.bib_number for reward in rewards]
    runner = runner_repository.get_first_oriol(bib_number_rewarded, 'F')
    add_runner_in_rewards(rewards, runner, "O", 'F')
    runner = runner_repository.get_first_oriol(bib_number_rewarded, 'M')
    add_runner_in_rewards(rewards, runner, "O", 'M')
    return rewards

def get_rewards_in_scratch(rewards, sex, number):
    for i in range(1, number+1):
        category = "S" + str(i)
        runner = runner_repository.get_reward_in_scratch(i, sex)
        add_runner_in_rewards(rewards, runner, category, sex)

def get_rewards_in_category(rewards, category, sex, skip):
    runner = runner_repository.get_reward_in_category(category, sex, skip)
    add_runner_in_rewards(rewards, runner, category, sex)

def add_runner_in_rewards(rewards, runner, category, sex):
    if runner:
        reward = Reward(category, sex, runner.ranking, runner.last_name, runner.first_name, runner.bib_number, runner.get_time())
    else:
        reward = Reward(category, sex)
    rewards.append(reward)

class Reward():
    
    def __init__(self, category: str, sex: str, ranking: int = None, last_name: str = None, first_name: str = None, bib_number: int = None, time: str = None):
        self.category: str = category
        self.sex: str = sex
        self.ranking: int = ranking
        self.last_name: str = last_name
        self.first_name: str = first_name
        self.bib_number: int = bib_number
        self.time: str = time