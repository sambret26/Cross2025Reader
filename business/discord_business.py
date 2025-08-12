import time

from utils import word_generator, file_reader, category_init, rewards
from repositories.SettingRepository import SettingRepository
from repositories.RunnerRepository import RunnerRepository
from constants import messages, file_data
from mail_sender import mail_service

setting_repository = SettingRepository()
runner_repository = RunnerRepository()

async def mail(ctx):
    word_generator.create_word_file()
    mail_service.send_mail()
    await ctx.send(messages.MAIL_SEND)

async def delete(ctx):
    runner_repository.delete_all()
    await ctx.send(messages.DB_DELETE)

async def init(ctx):
    runner_repository.delete_all()
    setting_repository.set_debug(0)
    setting_repository.set_offset_a(42932)
    setting_repository.set_offset_b(26301)
    setting_repository.set_offset_c(576)
    setting_repository.set_number_scratch_m(5)
    setting_repository.set_number_scratch_f(3)
    setting_repository.set_debug_channel(1361128278189936800)
    setting_repository.set_mail_sended(0)
    category_init.init_categories()
    await ctx.send(messages.DB_INIT)

async def debug(ctx, arg):
    if arg.lower() in ["on", "1"]:
        setting_repository.set_debug(1)
        await ctx.send(messages.DEBUG_ON)
    elif arg.lower() in ["off", "0"]:
        setting_repository.set_debug(0)
        await ctx.send(messages.DEBUG_OFF)
    else:
        await ctx.send(messages.DEBUG_KO)

async def offset(ctx, args):
    if len(args) < 3:
        await ctx.send(messages.OFFSET_KO)
        return
    try:
        offset_a = int(args[0])
        offset_b = int(args[1])
        offset_c = int(args[2])
    except ValueError:
        await ctx.send(messages.OFFSET_KO)
        return
    setting_repository.set_offset_a(offset_a)
    setting_repository.set_offset_b(offset_b)
    setting_repository.set_offset_c(offset_c)
    await ctx.send(messages.OFFSET_OK
        .replace("O_A", str(offset_a))
        .replace("O_B", str(offset_b))
        .replace("O_C", str(offset_c))
    )

async def setmail(ctx, arg):
    if arg.lower() in ["on", "1"]:
        setting_repository.set_mail_sended(1)
        await ctx.send(messages.MAIL_ON)
    elif arg.lower() in ["off", "0"]:
        setting_repository.set_mail_sended(0)
        await ctx.send(messages.MAIL_OFF)
    else:
        await ctx.send(messages.MAIL_KO)

async def test(ctx):
    await ctx.send(messages.OK)

async def clear(ctx, nombre):
    await ctx.channel.purge(limit=nombre+1, check=lambda msg: not msg.pinned)

async def cmd(ctx):
    await ctx.send(messages.CMD)

async def import_file(bot, message):
    file = await message.attachments[0].to_file()
    if not file.filename.endswith(".cap"):
        await message.channel.send(messages.UNKNOWN_EXTENSION)
        return
    await message.attachments[0].save(file_data.GMCAP_FILENAME)
    start = time.time()
    await file_reader.read_file(bot, file_data.GMCAP_FILENAME)
    end = time.time()
    duration = round(end - start, 2)
    await message.channel.send(messages.FILE_TREATED + " en " + str(duration) + " secondes")
    rewards.update_rewards()
        