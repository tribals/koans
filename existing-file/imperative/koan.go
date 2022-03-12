package main

import (
	"errors"
	"fmt"
	"os"
)

func main() {
	path := os.Args[1]
	text, err := readFile(path)

	if err != nil {
		os.Exit(1)
	}

	fmt.Print(text)
}

func readFile(path string) ([]byte, error) {
	text, err := os.ReadFile(path)

	if err != nil {
		return nil, errors.New("Domain error")
	}

	return text, nil
}
