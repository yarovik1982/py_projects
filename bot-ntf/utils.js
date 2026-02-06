const config = require('./config');

function openCase(caseType) {
   const caseData = config.CASES[caseType];
   const items = caseData.items;

   const rand = Math.random();
   let cumulativeProb = 0;

   for (const item of items) {
      cumulativeProb += item.probability;
      if (rand <= cumulativeProb) {
         return item;
      }
   }

   return items[items.length - 1];
}

function formatBalance(balance) {
   return `💰 Баланс: ${balance} монет`;
}

function formatInventory(items) {
   if (!items || items.length === 0) {
      return "🎒 Ваш инвентарь пуст";
   }

   let inventoryText = "🎒 Ваш инвентарь:\n\n";

   const rarityEmojis = {
      common: '🟦',
      rare: '🟩',
      epic: '🟪',
      legendary: '🟧'
   };

   items.forEach((item, index) => {
      inventoryText += `${rarityEmojis[item.rarity] || '⚪'} ${item.item_name} (${item.rarity})\n`;
   });

   return inventoryText;
}

function getCooldownTime(lastUsed, cooldownMs) {
   if (!lastUsed) return 0;

   const now = new Date();
   const lastUsedTime = new Date(lastUsed);
   const timePassed = now - lastUsedTime;
   const timeLeft = cooldownMs - timePassed;

   return timeLeft > 0 ? timeLeft : 0;
}

function formatTime(ms) {
   const hours = Math.floor(ms / (1000 * 60 * 60));
   const minutes = Math.floor((ms % (1000 * 60 * 60)) / (1000 * 60));

   if (hours > 0) {
      return `${hours}ч ${minutes}м`;
   }
   return `${minutes}м`;
}

module.exports = {
   openCase,
   formatBalance,
   formatInventory,
   getCooldownTime,
   formatTime
};