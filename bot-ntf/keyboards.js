const { Markup } = require('telegraf');

function mainMenu() {
   return Markup.keyboard([
      ['🎁 Открыть кейсы', '💰 Баланс'],
      ['🎒 Инвентарь', '💎 Заработать'],
      ['📊 Статистика']
   ]).resize();
}

function casesMenu() {
   return Markup.inlineKeyboard([
      [
         Markup.button.callback('🟦 Обычный кейс (100 монет)', 'case_common'),
         Markup.button.callback('🟪 Премиум кейс (500 монет)', 'case_premium')
      ],
      [Markup.button.callback('🔙 Назад', 'back_main')]
   ]);
}

function earnMenu() {
   return Markup.inlineKeyboard([
      [Markup.button.callback('📹 Посмотреть рекламу (+50 монет)', 'earn_ads')],
      [Markup.button.callback('📱 Выполнить задание (+100 монет)', 'earn_task')],
      [Markup.button.callback('🎁 Ежедневный бонус (+200 монет)', 'earn_daily')],
      [Markup.button.callback('🔙 Назад', 'back_main')]
   ]);
}

function backButton() {
   return Markup.inlineKeyboard([
      [Markup.button.callback('🔙 Назад', 'back_main')]
   ]);
}

module.exports = {
   mainMenu,
   casesMenu,
   earnMenu,
   backButton
};