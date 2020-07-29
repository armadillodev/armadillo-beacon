package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"math/rand"
	"net/http"
	"time"
)

//const url_base = "http://164.90.183.80/api/data/bike"
const url_base = "http://localhost:8000/api/data/"

func bikeData() []byte {
	requestBody, err := json.Marshal(map[string]int{
		"current": rand.Intn(30) + 10,
		"voltage": rand.Intn(30) + 10,
		"rpm":     rand.Intn(30) + 10,
	})

	if err != nil {
		log.Fatalln(err)
	}

	return requestBody
}

func ovenData() []byte {
	requestBody, err := json.Marshal(map[string]int{
		"temperature": rand.Intn(30) + 10,
	})

	if err != nil {
		log.Fatalln(err)
	}

	return requestBody
}

func microgridData() []byte {
	requestBody, err := json.Marshal(map[string]int{
		"temperature": rand.Intn(30) + 10,
		"power":       rand.Intn(30) + 10,
	})

	if err != nil {
		log.Fatalln(err)
	}

	return requestBody
}

func postData(bikeId int, route string, req []byte) {
	url := fmt.Sprintf("%s/%s/%v", url_base, route, bikeId)

	resp, err := http.Post(url, "application/json", bytes.NewBuffer(req))
	if err != nil {
		log.Fatalln(err)
	}

	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Fatalln(err)
	}

	log.Println(string(body))
}

func postAllData() {
	go postData(1, "bike", bikeData())
	go postData(2, "bike", bikeData())
	go postData(3, "bike", bikeData())
	go postData(1, "oven", ovenData())
	go postData(1, "microgrid", microgridData())
	//go postData(4)
	//go postData(5)
	//go postData(6)
	//go postData(7)
	//go postData(8)
}

func main() {
	log.Println("URL:>", url_base)

	for {
		postAllData()
		time.Sleep(1 * time.Second)
	}
}
