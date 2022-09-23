import os
import discord
from discord.ext import commands
import random
import datetime
#from replit import db
#from keep_alive import keep_alive

#TOKEN = os.environ['TOKEN']


intents = discord.Intents.all()
client = commands.Bot(command_prefix='-', intents=intents)


cheaters = []


#эта функция проверяет прошли сутки с момента предыдущего вызова или нет
def check_time(author):
  curr = datetime.datetime.now().strftime('%s')
  try:
    last = db["huytimes"][author]
  except KeyError:
    return True

  #найти разность двух таймштампов и если она больше 1 то можно играть
  difference = (float(curr) - float(last))/(60*60*24) 

  if difference >= 1:
    return True
  else:
    return False


#эта функция решает на сколько увеличить хуй
def randHuy():
  
  chances = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 9, 9, 10]

  if random.random() <= 0.2:
    randHuy = random.choice(chances) * -1
  else:
    randHuy = random.choice(chances)

  return randHuy
  




    

@client.event #sets custom status
async def on_ready():
  #channel = client.get_channel(464164962353414155) 
  await client.change_presence(status=discord.Status.online,
                               activity=discord.Activity(type=discord.ActivityType.playing,
                                                         name="СЫН БЛЯДИ")) # в параметр name то что хочешь
  #await channel.send("ебальники стянули папа в здании")


@client.event
async def on_member_update(before, after):
  try:
    print(after.activity.name)
  except:
    pass
  role = discord.utils.get(after.guild.roles, name="↓↓↓ чувырла опущенная играет в тарков ↓↓↓")
  games = ["Escape from Tarkov"]

  if after.activity and after.activity.name in games:
    await after.add_roles(role)

    # only add the rest if you want them to have the role for the duration of them
    # playing a game
  elif before.activity and before.activity.name in games and not after.activity:
    if role in after.roles: # check they already have the role, as to not throw an error
      await after.remove_roles(role)



@client.event  
async def on_message(message):
    message.content = message.content.lower() #все ловеркейс

    if message.author == client.user:  # если автор сообщения сам бот то игнорировать
        return

    if message.content.startswith("ку"):
      if str(message.author) == "TheDors#1704":
        await message.channel.send("ку даничка мой любименький")
      else:
        await message.channel.send("ку")

    await client.process_commands(message) #on_message fix



@client.command()
async def ктоя(ctx):

    await ctx.send(str(random.choice(db["mats"])))


@client.command()
async def ктоон(ctx, mention):
  try:
    if mention == "<@953419458062479451>": 
      await ctx.send(ctx.author.mention + " ТЫ ЧЕ ОХУЕЛ СВИНЬЯ!")
    else:
      await ctx.send(mention + " ТЫ " + random.choice(db["mats"]))
  except:
    await ctx.send("нужно упоминание челика")




@client.command()
async def нахуй(ctx):
    author = ctx.author.mention
    huy = ['иди', 'сходи', 'гуляй', 'пиздуй', 'уебывай']
    await ctx.send(author + " " + random.choice(huy) + " нахуй")




@client.command()
async def все(ctx):
  output = ""
  for i in range(len(db["mats"])):
    output = output + str(db["mats"][i]) + " \n"

  await ctx.send(output)






@client.command()
async def добавь(ctx, *args):

  #сделать все полученные аргументы в единую переменную
  #ибо каждое слово после команды будет отдельным аргументом
  text = ""
  for arg in args:
    text = text + str(arg) + " "

  if text in db["mats"]:
    await ctx.send("ты че еблан это уже есть")
  else:
    db["mats"].append(text.upper())
    await ctx.send(text + " добавлено")







@client.command()
async def удали(ctx, *args):

  text = ""
  for arg in args:
    text = text + str(arg) + " "

  if text.upper() in db["mats"]:
    index = db["mats"].index(text.upper())
    del db["mats"][index]
    await ctx.send(text + " удалено")

  else:
    await ctx.send("отсоси нет такой хуйни")
  

  
#ДОБАВИЛ ИЗНАЧАЛЬНЫЕ МАТЮКИ В ДАТАБЕЙС
# db["mats"] = []
# for i in range (len(mat)):
#   db["mats"].append(mat[i])

#ПРОВЕРИЛ
#print(db["mats"])





#регистрация в игру в хуй
@client.command()
async def huyreg(ctx): 
  if str(ctx.author) not in db["huy"]:
    db["huy"][str(ctx.author)] = 0
    await ctx.send("Ты зарегистрирован в игре в хуй\n Длина твоего монстра - " + str(db["huy"][str(ctx.author)]))
  else:
    await ctx.send("Ты уже зарегистрирован в игре в хуй")

@client.command()
async def huyunreg(ctx):
  if str(ctx.author) in db["huy"]:
    del db["huy"][str(ctx.author)]
    del db["huytimes"][str(ctx.author)]
    await ctx.send("Ты вышел из игры")
  else:
    await ctx.send("Ты не был зарегистрирован")

@client.command()
async def huyplayers(ctx):

  output = ""

  #this basically sorts the dictionary idk
  huys_sorted = sorted(db["huy"].items(), key=lambda x: x[1], reverse=True)

  #tuples where first element is key and second is value
  for i in huys_sorted:
    output = output + i[0] + " длина хуя - " + str(i[1]) + " см\n"
    
  await ctx.send(output)



@client.command()
async def podkrutka(ctx, mention):
  
  user = mention
  user = user.replace("<","")
  user = user.replace(">","")
  user = user.replace("@","")
  
  if str(ctx.message.author) == "Yarman53#9098": 
    if user in cheaters:
      cheaters.remove(user)
      await ctx.send(mention + " человечность восстановлена")
    else:
      cheaters.append(user)
      await ctx.send(mention + " ты теперь играешь с софтом")
  else:
    await ctx.send("Пашол нахуй)")



@client.command()
async def huy(ctx):
  
  if str(ctx.author) in db["huy"].keys(): #если чел зареган
    
    huy = db["huy"][str(ctx.author)] #хранит длину хуя

    if str(ctx.author.id) in cheaters:   #если чел с подкруткой то тупа добавить 10
      db["huy"][str(ctx.author)] = huy + 10
      await ctx.send(str(ctx.author) + " твой хуй увеличился на 10\nДлина твоего хуя - " + str(db["huy"][str(ctx.author)]) + " см")

      
    else:   #если чел без подкрутки то стандартная процедура
      
      if check_time(str(ctx.author)): #если прошли сутки то
        uvelich = randHuy() #хранит то что выбрала функция
        
        db["huy"][str(ctx.author)] = huy + uvelich
        
        db["huytimes"][str(ctx.author)] = datetime.datetime.now().strftime('%s')
  
        if uvelich > 0:
          await ctx.send(str(ctx.author) + " твой хуй увеличился на " + str(uvelich) + "\nДлина твоего хуя - " + str(db["huy"][str(ctx.author)]) + " см")
        else: 
          await ctx.send(str(ctx.author) + " твой хуй скоротился на " + str(uvelich)[1:] + "\nДлина твоего хуя - " + str(db["huy"][str(ctx.author)]) + " см")
        
      else: #если не прошли сутки
        await ctx.send(str(ctx.author) + " ты сегодня уже играл\nДлина твоего шланга - " + str(huy) + " см")



      
  else: #если не зареган
    await ctx.send(str(ctx.author) + " У тебя еще нет хуя :\\")
    del db["huytimes"][str(ctx.author)]



  

#kill 1 in shell to fix ban

#keep_alive()
client.run(OTUzNDE5NDU4MDYyNDc5NDUx.YjETEA.IQ1ArqAiyiZxKebHAYZ8Vljq-Yw)
