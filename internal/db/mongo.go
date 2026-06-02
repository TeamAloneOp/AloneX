package db

import (
	"context"
	"log"
	"time"

	"go.mongodb.org/mongo-driver/v2/bson"
	"go.mongodb.org/mongo-driver/v2/mongo"
	"go.mongodb.org/mongo-driver/v2/mongo/options"
)

type MongoDB struct {
	client *mongo.Client
	db     *mongo.Database
}

func NewMongoDB(uri string) (*MongoDB, error) {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	client, err := mongo.Connect(options.Client().ApplyURI(uri))
	if err != nil {
		return nil, err
	}

	err = client.Ping(ctx, nil)
	if err != nil {
		return nil, err
	}

	return &MongoDB{
		client: client,
		db:     client.Database("Anon"),
	}, nil
}

func (m *MongoDB) GetSudoers(ctx context.Context) ([]int64, error) {
	collection := m.db.Collection("cache")
	var result struct {
		UserIDs []int64 `bson:"user_ids"`
	}
	err := collection.FindOne(ctx, bson.M{"_id": "sudoers"}).Decode(&result)
	if err == mongo.ErrNoDocuments {
		return []int64{}, nil
	}
	return result.UserIDs, err
}

func (m *MongoDB) IsBlacklisted(ctx context.Context, id int64) (bool, error) {
	collection := m.db.Collection("cache")

	// Check blacklisted users
	var userResult struct {
		UserIDs []int64 `bson:"user_ids"`
	}
	err := collection.FindOne(ctx, bson.M{"_id": "bl_users"}).Decode(&userResult)
	if err == nil {
		for _, v := range userResult.UserIDs {
			if v == id {
				return true, nil
			}
		}
	}

	// Check blacklisted chats
	var chatResult struct {
		ChatIDs []int64 `bson:"chat_ids"`
	}
	err = collection.FindOne(ctx, bson.M{"_id": "bl_chats"}).Decode(&chatResult)
	if err == nil {
		for _, v := range chatResult.ChatIDs {
			if v == id {
				return true, nil
			}
		}
	}

	return false, nil
}

func (m *MongoDB) GetAssistant(ctx context.Context, chatID int64) (int, error) {
	collection := m.db.Collection("assistant")
	var result struct {
		Num int `bson:"num"`
	}
	err := collection.FindOne(ctx, bson.M{"_id": chatID}).Decode(&result)
	if err == mongo.ErrNoDocuments {
		return 1, nil // Default assistant
	}
	return result.Num, err
}

func (m *MongoDB) AddChat(ctx context.Context, chatID int64) error {
	collection := m.db.Collection("chats")
	_, err := collection.UpdateOne(
		ctx,
		bson.M{"_id": chatID},
		bson.M{"$set": bson.M{"_id": chatID}},
		options.UpdateOne().SetUpsert(true),
	)
	return err
}

func (m *MongoDB) Close(ctx context.Context) {
	if err := m.client.Disconnect(ctx); err != nil {
		log.Printf("Error disconnecting from MongoDB: %v", err)
	}
}
