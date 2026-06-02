package config

import (
	"os"
	"testing"
)

func TestLoad(t *testing.T) {
	os.Setenv("API_ID", "12345")
	os.Setenv("API_HASH", "test_hash")
	os.Setenv("BOT_TOKEN", "test_token")
	os.Setenv("MONGO_URL", "mongodb://localhost:27017")
	os.Setenv("SESSION", "test_session")

	cfg := Load()

	if cfg.APIID != 12345 {
		t.Errorf("Expected APIID 12345, got %d", cfg.APIID)
	}
	if cfg.APIHash != "test_hash" {
		t.Errorf("Expected APIHash test_hash, got %s", cfg.APIHash)
	}
}
