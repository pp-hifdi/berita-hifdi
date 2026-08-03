// Template — salin file ini jadi config.local.js lalu isi nilai asli.
// JANGAN commit config.local.js.
module.exports = {
  BOTS: [
    { name: "ummanitarian", token: "PASTE_BOT_TOKEN_DARI_BOTFATHER",
      folder: "C:\\path\\to\\ummanitarian-insight", group: "GROUP_ID@g.us" },
    { name: "fmi", token: "PASTE_BOT_TOKEN_DARI_BOTFATHER",
      folder: "C:\\path\\to\\berita-fmi", group: "GROUP_ID@g.us" },
    { name: "hifdi", token: "PASTE_BOT_TOKEN_DARI_BOTFATHER",
      folder: "C:\\path\\to\\berita-hifdi", group: "GROUP_ID@g.us" },
  ],
  ALLOWED_CHAT_IDS: [/* Telegram user ID pemilik, dari /id */],
  JOB_TIMEOUT_MIN: 25,
  OPENWA: {
    url: "http://localhost:2785",
    key: "PASTE_OPENWA_API_KEY",
    session: "PASTE_OPENWA_SESSION_ID",
  },
};
