package bot

import (
	"context"
	"fmt"
	"log"

	"github.com/gotd/td/telegram"
	"github.com/gotd/td/tg"
	"github.com/AloneXMusic/AloneXMusic-Go/internal/config"
)

type Client struct {
	tgClient *telegram.Client
	api      *tg.Client
	isBot    bool
}

func NewClient(cfg *config.Config, session string, isBot bool, handler telegram.UpdateHandler) (*Client, error) {
	opts := telegram.Options{}
	if handler != nil {
		opts.UpdateHandler = handler
	}
	client := telegram.NewClient(cfg.APIID, cfg.APIHash, opts)

	return &Client{
		tgClient: client,
		api:      tg.NewClient(client),
		isBot:    isBot,
	}, nil
}

func (c *Client) Start(ctx context.Context, token string) error {
	if !c.isBot {
		// For userbot, we would need a different flow or session storage
		// This is a simplified version
		log.Println("Starting Userbot...")
	} else {
		log.Println("Starting Bot...")
	}

	return c.tgClient.Run(ctx, func(ctx context.Context) error {
		if c.isBot {
			if _, err := c.tgClient.Auth().Bot(ctx, token); err != nil {
				return fmt.Errorf("bot auth: %w", err)
			}
		} else {
			// Userbot auth logic would go here
		}

		status, err := c.tgClient.Auth().Status(ctx)
		if err != nil {
			return fmt.Errorf("auth status: %w", err)
		}

		if !status.Authorized {
			if c.isBot {
				return fmt.Errorf("bot not authorized")
			}
			// For userbot, manual auth or session loading is required
		}

		log.Println("Client started and authorized")
		return nil
	})
}

func (c *Client) API() *tg.Client {
	return c.api
}
