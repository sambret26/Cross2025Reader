# -*- coding: utf-8 -*-
from utils import word_generator, file_reader, category_init
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

async def init(ctx):
    runner_repository.delete_all()
    setting_repository.set_runner_number(0)
    setting_repository.set_reward_number(0)
    setting_repository.set_debug(0) #TODO : Ne pas forcer à l'init
    setting_repository.set_offset_a(42932) #TODO : Ne pas forcer à l'init
    setting_repository.set_offset_b(26301) #TODO : Ne pas forcer à l'init
    setting_repository.set_offset_c(576) #TODO : Ne pas forcer à l'init
    setting_repository.set_number_scratch_m(5) #TODO : Ne pas forcer à l'init
    setting_repository.set_number_scratch_f(3) #TODO : Ne pas forcer à l'init
    category_init.init_categories() #TODO : Ne pas forcer à l'init
    await ctx.send(messages.DB_INIT)

async def test(ctx):
    await ctx.send(messages.OK)

async def clear(ctx, nombre):
    await ctx.channel.purge(limit=nombre+1, check=lambda msg: not msg.pinned)

async def import_file(bot, message):
    file = await message.attachments[0].to_file()
    if not file.filename.endswith(".cap"):
        await message.channel.send(messages.UNKNOWN_EXTENSION)
        return
    await message.attachments[0].save(file_data.GMCAP_FILENAME)
    file_reader.read_file(file_data.GMCAP_FILENAME)
    await message.channel.send(messages.FILE_TREATED)
    #TODO : Update result message (bot)
        