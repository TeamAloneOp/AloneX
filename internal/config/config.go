package config

import (
	"log"
	"os"
	"strconv"
	"strings"

	"github.com/joho/godotenv"
)

type Config struct {
	APIID           int
	APIHash         string
	BotToken        string
	MongoURL        string
	LoggerID        int64
	OwnerID         int64
	Session1        string
	SupportChannel  string
	SupportChat     string
	AutoEnd         bool
	AutoLeave       bool
	VideoPlay       bool
	QueueLimit      int
	DurationLimit   int
	PlaylistLimit   int
	YoutubeAPIKey   string
	DefaultThumb    string
	PingImg         string
	StartImg        string
}

func Load() *Config {
	err := godotenv.Load()
	if err != nil {
		log.Println("Warning: .env file not found")
	}

	return &Config{
		APIID:          getEnvInt("API_ID", 17596251),
		APIHash:        getEnv("API_HASH", "e58343b4c0193e293e391daf97603fcd"),
		BotToken:       getEnv("BOT_TOKEN", ""),
		MongoURL:       getEnv("MONGO_URL", ""),
		LoggerID:       getEnvInt64("LOGGER_ID", 0),
		OwnerID:        getEnvInt64("OWNER_ID", 0),
		Session1:       getEnv("SESSION", ""),
		SupportChannel: getEnv("SUPPORT_CHANNEL", "https://t.me/AloneUpdates"),
		SupportChat:    getEnv("SUPPORT_CHAT", "https://t.me/AloneBotSupport"),
		AutoEnd:        getEnvBool("AUTO_END", false),
		AutoLeave:      getEnvBool("AUTO_LEAVE", false),
		VideoPlay:      getEnvBool("VIDEO_PLAY", true),
		QueueLimit:     getEnvInt("QUEUE_LIMIT", 50),
		DurationLimit:  getEnvInt("DURATION_LIMIT", 5400),
		PlaylistLimit:  getEnvInt("PLAYLIST_LIMIT", 20),
		YoutubeAPIKey:  getEnv("YOUTUBE_API_KEY", "INFLEX68575028D"),
		DefaultThumb:   getEnv("DEFAULT_THUMB", "https://te.legra.ph/file/3e40a408286d4eda24191.jpg"),
		PingImg:        getEnv("PING_IMG", "https://files.catbox.moe/haagg2.png"),
		StartImg:       getEnv("START_IMG", "https://files.catbox.moe/zvziwk.jpg"),
	}
}

func (c *Config) Check() {
	var missing []string
	if c.APIID == 0 {
		missing = append(missing, "API_ID")
	}
	if c.APIHash == "" {
		missing = append(missing, "API_HASH")
	}
	if c.BotToken == "" {
		missing = append(missing, "BOT_TOKEN")
	}
	if c.MongoURL == "" {
		missing = append(missing, "MONGO_URL")
	}
	if c.Session1 == "" {
		missing = append(missing, "SESSION")
	}

	if len(missing) > 0 {
		log.Fatalf("Missing required environment variables: %s", strings.Join(missing, ", "))
	}
}

func getEnv(key, fallback string) string {
	if value, ok := os.LookupEnv(key); ok {
		return value
	}
	return fallback
}

func getEnvInt(key string, fallback int) int {
	if value, ok := os.LookupEnv(key); ok {
		i, err := strconv.Atoi(value)
		if err != nil {
			return fallback
		}
		return i
	}
	return fallback
}

func getEnvInt64(key string, fallback int64) int64 {
	if value, ok := os.LookupEnv(key); ok {
		i, err := strconv.ParseInt(value, 10, 64)
		if err != nil {
			return fallback
		}
		return i
	}
	return fallback
}

func getEnvBool(key string, fallback bool) bool {
	if value, ok := os.LookupEnv(key); ok {
		b, err := strconv.ParseBool(value)
		if err != nil {
			return fallback
		}
		return b
	}
	return fallback
}
