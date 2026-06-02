package main

import (
	"context"
	"log"
	"os"
	"os/signal"
	"syscall"

	"github.com/AloneXMusic/AloneXMusic-Go/internal/bot"
	"github.com/AloneXMusic/AloneXMusic-Go/internal/config"
	"github.com/AloneXMusic/AloneXMusic-Go/internal/db"
)

func main() {
	cfg := config.Load()
	cfg.Check()

	ctx, cancel := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
	defer cancel()

	database, err := db.NewMongoDB(cfg.MongoURL)
	if err != nil {
		log.Fatalf("Failed to connect to MongoDB: %v", err)
	}
	defer database.Close(context.Background())

	h := bot.NewHandlers(nil) // We'll set the sender later
	b, err := bot.NewClient(cfg, "", true, h)
	if err != nil {
		log.Fatalf("Failed to create bot client: %v", err)
	}
	h.SetSender(b.API())

	go func() {
		if err := b.Start(ctx, cfg.BotToken); err != nil {
			log.Fatalf("Bot failed: %v", err)
		}
	}()

	log.Println("AloneX Music Bot (Go) is running...")
	<-ctx.Done()
	log.Println("Shutting down...")
}
