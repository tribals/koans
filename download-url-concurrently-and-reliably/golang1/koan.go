// Copyright М. Жуков (2023)

package main

import (
	"context"
	"fmt"
	"net/http"
	"time"
)

func download(ctx context.Context, url string) (*http.Response, error) {
	client := &http.Client{Timeout: 2 * time.Second}
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		return nil, err
	}
	req = req.WithContext(ctx)
	return client.Do(req)
}

func downloadWithRetry(ctx context.Context, url string, timeout time.Duration, sleep_time time.Duration) error {
	endTime := time.NewTimer(timeout)

	ctx, cancel := context.WithTimeout(ctx, timeout)
	defer cancel()

	for {
		if resp, err := download(ctx, url); err == nil {
			// TODO: put your check here
			if resp.StatusCode == http.StatusBadGateway {
				return nil
			}
			fmt.Println("Result is not good enough. Repeat")
		}
		sleepTimer := time.NewTimer(sleep_time)
		select {
		case <-endTime.C:
			return fmt.Errorf("global timeout reached")
		case <-ctx.Done():
			return fmt.Errorf("global context reached")
		case <-sleepTimer.C:
			fmt.Println("Wake up and try again")
		}
	}
}

func main() {
	ctx := context.Background()
	if err := downloadWithRetry(ctx, "https://yandex.ru", 20*time.Second, 3*time.Second); err != nil {
		fmt.Println("Error: ", err.Error())
		return
	}
	fmt.Println("Success")
}
