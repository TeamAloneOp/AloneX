package bot

import (
	"context"
	"fmt"
	"strings"
	"time"

	"github.com/gotd/td/telegram/message"
	"github.com/gotd/td/tg"
)

type Handlers struct {
	sender *message.Sender
}

func NewHandlers(api *tg.Client) *Handlers {
	h := &Handlers{}
	if api != nil {
		h.sender = message.NewSender(api)
	}
	return h
}

func (h *Handlers) SetSender(api *tg.Client) {
	h.sender = message.NewSender(api)
}

func (h *Handlers) Handle(ctx context.Context, u tg.UpdatesClass) error {
	switch updates := u.(type) {
	case *tg.Updates:
		for _, u := range updates.Updates {
			if err := h.handleUpdate(ctx, u); err != nil {
				return err
			}
		}
	case *tg.UpdateShortMessage:
		// Handle short message
	case *tg.UpdateShortChatMessage:
		// Handle short chat message
	case *tg.UpdatesCombined:
		for _, u := range updates.Updates {
			if err := h.handleUpdate(ctx, u); err != nil {
				return err
			}
		}
	case *tg.UpdateShort:
		return h.handleUpdate(ctx, updates.Update)
	}
	return nil
}

func (h *Handlers) handleUpdate(ctx context.Context, u tg.UpdateClass) error {
	switch update := u.(type) {
	case *tg.UpdateNewMessage:
		msg, ok := update.Message.(*tg.Message)
		if !ok || msg.Out {
			return nil
		}

		if strings.HasPrefix(msg.Message, "/start") {
			return h.handleStart(ctx, msg)
		} else if strings.HasPrefix(msg.Message, "/ping") {
			return h.handlePing(ctx, msg)
		}
	}
	return nil
}

func (h *Handlers) handleStart(ctx context.Context, msg *tg.Message) error {
	peer := &tg.InputPeerUser{
		UserID:     msg.PeerID.(*tg.PeerUser).UserID,
		AccessHash: 0, // In a real app, you'd get this from your peer storage
	}

	text := "Welcome to AloneX Music Bot (Go Edition)!\n\nUse /ping to check the latency."
	_, err := h.sender.To(peer).Text(ctx, text)
	return err
}

func (h *Handlers) handlePing(ctx context.Context, msg *tg.Message) error {
	start := time.Now()
	peer := &tg.InputPeerUser{
		UserID:     msg.PeerID.(*tg.PeerUser).UserID,
		AccessHash: 0,
	}

	latency := time.Since(start).Milliseconds()
	text := fmt.Sprintf("🏓 Pong!\nLatency: %dms", latency)

	_, err := h.sender.To(peer).Text(ctx, text)
	return err
}
