const { Telegraf, session } = require('telegraf');
const config = require('./config');
const db = require('./database');
const keyboards = require('./keyboards');
const utils = require('./utils');

const bot = new Telegraf(config.BOT_TOKEN);

// Middleware
bot.use(session());

// Команда /start
bot.start(async (ctx) => {
   const user = ctx.from;
   await db.createUser(user.id, user.username);

   const welcomeText = `
👋 Привет, ${user.first_name}!

🎮 Добро пожаловать в NFT Case Bot!

✨ Здесь ты можешь:
• 🎁 Открывать кейсы с NFT
• 💎 Зарабатывать монеты
• 🎒 Коллекционировать уникальные предметы

💰 На старте ты получаешь 1000 монет!
  `;

   await ctx.reply(welcomeText, keyboards.mainMenu());
});

// Обработка текстовых сообщений
bot.hears('🎁 Открыть кейсы', async (ctx) => {
   await ctx.reply('🎁 Выберите кейс для открытия:', keyboards.casesMenu());
});

bot.hears('💰 Баланс', async (ctx) => {
   const user = await db.getUser(ctx.from.id);
   await ctx.reply(utils.formatBalance(user.balance), keyboards.mainMenu());
});

bot.hears('🎒 Инвентарь', async (ctx) => {
   const items = await db.getInventory(ctx.from.id);
   await ctx.reply(utils.formatInventory(items), keyboards.mainMenu());
});

bot.hears('💎 Заработать', async (ctx) => {
   await ctx.reply('💎 Выберите способ заработка:', keyboards.earnMenu());
});

bot.hears('📊 Статистика', async (ctx) => {
   const user = await db.getUser(ctx.from.id);
   const items = await db.getInventory(ctx.from.id);

   const statsText = `
📊 Ваша статистика:

💰 Баланс: ${user.balance} монет
🎒 Предметов: ${items.length}
📅 Дата регистрации: ${new Date(user.created_at).toLocaleDateString()}
  `;

   await ctx.reply(statsText, keyboards.mainMenu());
});

// Обработка inline кнопок
bot.action(/case_(.+)/, async (ctx) => {
   const caseType = ctx.match[1];
   const userId = ctx.from.id;

   const user = await db.getUser(userId);
   const casePrice = caseType === 'common' ? 100 : 500;

   if (user.balance < casePrice) {
      await ctx.editMessageText(
         `❌ Недостаточно монет! Нужно ${casePrice} монет.`,
         keyboards.backButton()
      );
      return;
   }

   // Списываем монеты
   await db.updateBalance(userId, -casePrice);
   await db.addTransaction(userId, -casePrice, 'purchase', `Покупка кейса ${caseType}`);

   // Открываем кейс
   const item = utils.openCase(caseType);

   // Добавляем в инвентарь
   await db.addToInventory(userId, item.name, item.rarity);

   // Эмодзи для редкостей
   const rarityEmojis = {
      common: '🟦',
      rare: '🟩',
      epic: '🟪',
      legendary: '🟧'
   };

   const resultText = `
🎉 Поздравляем!

${rarityEmojis[item.rarity]} Вы получили: ${item.name}
📊 Редкость: ${item.rarity.toUpperCase()}

💰 Баланс: ${user.balance - casePrice} монет
  `;

   await ctx.editMessageText(resultText, keyboards.backButton());
});

bot.action(/earn_(.+)/, async (ctx) => {
   const action = ctx.match[1];
   const userId = ctx.from.id;
   const earnConfig = config.EARN_OPTIONS[action];

   if (!earnConfig) {
      await ctx.answerCbQuery('❌ Неизвестное действие');
      return;
   }

   // Проверка кулдауна
   const lastUsed = await db.getCooldown(userId, action);
   const cooldownLeft = utils.getCooldownTime(lastUsed, earnConfig.cooldown);

   if (cooldownLeft > 0) {
      await ctx.answerCbQuery(`⏰ Доступно через: ${utils.formatTime(cooldownLeft)}`);
      return;
   }

   // Начисляем награду
   await db.updateBalance(userId, earnConfig.reward);
   await db.addTransaction(userId, earnConfig.reward, 'earn', `Заработок: ${action}`);
   await db.setCooldown(userId, action);

   const user = await db.getUser(userId);

   await ctx.editMessageText(
      `🎉 +${earnConfig.reward} монет!\n\n${utils.formatBalance(user.balance)}`,
      keyboards.backButton()
   );
});

bot.action('back_main', async (ctx) => {
   await ctx.editMessageText('🔙 Возвращаемся в главное меню:', keyboards.mainMenu());
});

// Обработка ошибок
bot.catch((err, ctx) => {
   console.error(`Error for ${ctx.updateType}:`, err);
   ctx.reply('❌ Произошла ошибка. Попробуйте позже.');
});

// Запуск бота
bot.launch().then(() => {
   console.log('🤖 Бот запущен!');
});

// Graceful shutdown
process.once('SIGINT', () => bot.stop('SIGINT'));
process.once('SIGTERM', () => bot.stop('SIGTERM'));