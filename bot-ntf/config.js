require('dotenv').config();

module.exports = {
    BOT_TOKEN: process.env.BOT_TOKEN,
    ADMIN_ID: parseInt(process.env.ADMIN_ID) || 0,

    CASES: {
        common: {
            name: "Обычный кейс",
            price: 100,
            items: [
                { name: "Обычная NFT", rarity: "common", probability: 0.6 },
                { name: "Редкая NFT", rarity: "rare", probability: 0.3 },
                { name: "Эпическая NFT", rarity: "epic", probability: 0.09 },
                { name: "Легендарная NFT", rarity: "legendary", probability: 0.01 }
            ]
        },
        premium: {
            name: "Премиум кейс",
            price: 500,
            items: [
                { name: "Редкая NFT", rarity: "rare", probability: 0.5 },
                { name: "Эпическая NFT", rarity: "epic", probability: 0.35 },
                { name: "Легендарная NFT", rarity: "legendary", probability: 0.15 }
            ]
        }
    },

    EARN_OPTIONS: {
        ads: { reward: 50, cooldown: 3600000 }, // 1 hour
        task: { reward: 100, cooldown: 7200000 }, // 2 hours
        daily: { reward: 200, cooldown: 86400000 } // 24 hours
    }
};