from io import BytesIO
import aiofiles

from repositories.RunnerRepository import RunnerRepository
from repositories.SettingRepository import SettingRepository
from models.Runner import Runner

runner_repository = RunnerRepository()
setting_repository = SettingRepository()

def get_offset():
    offset_a = setting_repository.get_offset_a()
    offset_b = setting_repository.get_offset_b()
    offset_c = setting_repository.get_offset_c()
    return (offset_a, offset_b, offset_c)

async def read_file(bot, filename):
    runner_map = runner_repository.get_runner_map()
    runners_to_insert = []
    offsets = get_offset()

    async with aiofiles.open(filename, 'rb') as f:
        content = await f.read()

    with BytesIO(content) as file:
        eat_until(file, [b'\x00']*100)
        eat_zero(file)
        number = read_int_with_fix_length(file, 2)
        already_debugged = False
        for _ in range(number):
            already_debugged = await read_runner(bot, file, runner_map, runners_to_insert, offsets, already_debugged)
    runner_repository.insert_runners(runners_to_insert)

async def read_runner(bot, file, runner_map, runners_to_insert, offsets, already_debugged):
    last_name = read_with_length(file).upper()
    first_name = read_with_length(file).title()
    sex = get_sex(eat_int_n(file, 1))
    file.read(1)
    bib_number = read_int_with_fix_length(file, 2)
    file.read(2)
    category = get_category(eat_int_n(file, 1))
    file.read(1)
    read_with_length(file) # Licence
    read_int_with_fix_length(file, 2)
    skip(file, 4) # Adresse / complément / code / ville
    a = read_int_with_fix_length(file, 2)
    b = read_int_with_fix_length(file, 2)
    c = read_int_with_fix_length(file, 2)
    runner_time = await find_hour(bot, a, b, c, offsets, already_debugged)
    if runner_time:
        already_debugged = True
    file.read(66) # Le 9i : inverse de authorisation diffusion
    skip(file, 2)
    file.read(8)
    skip(file, 5) # Etat / Pays / tel / palmares / ?
    file.read(2) # Certificat médical / Partant
    disqualified = eat_int_n(file, 1)
    give_up = eat_int_n(file, 1)
    file.read(16)
    ranking = read_int_with_fix_length(file, 2)
    category_ranking = read_int_with_fix_length(file, 2)
    sex_ranking = read_int_with_fix_length(file, 2)
    skip(file, 2) # Club / Course
    file.read(1) # Demande d'envoie des classements
    organism = read_with_length(file)
    skip(file, 3) # sponsor / mail / Pass comp
    file.read(6) # 4*?  / Cotisation payée / Invité
    read_with_length(file) # Nationalité
    file.read(3)
    read_with_length(file) # Identifiant GM-CAP
    #file.read(1026)
    eat_zero(file)
    file.read(1) # Attention !! Différent en fonction des fichiers
    eat_zero(file) # Attention !! Différent en fonction des fichiers
    oriol = (organism.title() == "Oriol")
    out = give_up == 1 or disqualified == 1
    if runner_time != None and ranking != 0:
        runner = Runner(last_name, first_name, sex, ranking, category, category_ranking, sex_ranking, bib_number, runner_time, oriol, True, out )
    else:
        runner = Runner(last_name, first_name, sex, 0, category, 0, 0, bib_number, "", oriol, False, out)
    name = last_name + "_" + first_name
    if name in runner_map:
        runner_in_db = runner_map[name]
        if(runner.is_different(runner_in_db)):
            runner.id = runner_in_db.id
            runner_repository.update(runner)
    else:
        runners_to_insert.append(runner)
    return already_debugged

def skip(file, iteration):
    for _ in range(iteration):
        read_with_length(file)

def eat_until(file, target):
    join_target = b''.join(target)
    new_target = bytearray(join_target)
    buffer = bytearray(len(target))
    while True:
        byte = file.read(1)
        if not byte:
            break
        buffer.pop(0)
        buffer.append(byte[0])
        if buffer == new_target:
            break

def eat_zero(file):
    while True:
        byte = file.read(1)
        if not byte:
            return -1
        if byte != b'\x00':
            file.seek(-1, 1)
            break

def read_int_with_fix_length(file, length):
    value = 0
    for compt in range(length):
        value += eat_int_n(file, 1) * (16**(compt*2))
    return value

def read_with_length(file):
    length = ord(file.read(1))
    return eat_n(file, length)

def eat_int_n(file, n):
    value = ""
    for _ in range(n):
        byte = file.read(1)
        if not byte:
            return -1
        value += str(ord(byte))
    return int(value)

def eat_n(file, n):
    value = ""
    for _ in range(n):
        byte = file.read(1)
        if not byte:
            return -1
        value += chr(ord(byte))
    return value

async def find_hour(bot, a, b, c, offsets, already_debugged):
    if a==0 and b==0 and c==0:
        return None
    offset_a, offset_b, offset_c = offsets
    if a==offset_a and b==offset_b and c==offset_c :
        return None
    if not already_debugged and setting_repository.get_debug():
        channel = bot.get_channel(setting_repository.get_debug_channel())
        await channel.send("Debug : " + str(a) + " " + str(b) + " " + str(c))
        already_debugged = True
    heures = 0
    minutes = 0
    if a < offset_a:
        secondes = 65536+a-offset_a
    else:
        secondes = a-offset_a
    if b > offset_b:
        secondes = secondes + 65536*(b-offset_b-1)
    if c < offset_c:
        milisecondes = 1000+c-offset_c
        secondes = secondes - 1
    else :
        milisecondes = c-offset_c
    while(secondes > 59):
        secondes = secondes - 60
        minutes = minutes + 1 
    while(minutes > 59):
        minutes = minutes - 60
        heures = heures + 1
    return(f'{heures:02}:{minutes:02}:{secondes:02}.{milisecondes:03}')

def get_sex(value):
    if value == 0:
        return 'M'
    return 'F'

def get_category(value):
    if value == 40:
        return "J"
    if value == 41:
        return "S"
    if value == 42:
        return "35+"
    if value == 43:
        return "45+"
    if value == 44:
        return "55+"
    return "65+"