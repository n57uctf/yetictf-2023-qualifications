package main

import (
	"bufio"
	"encoding/json"
	"errors"
	"fmt"
	"io/ioutil"
	"math"
	"math/rand"
	"net"
	"os"
	"strconv"
	"strings"
	"sync"
	"time"

	log "github.com/sirupsen/logrus"
)

var LISTENADDRESS = os.Getenv("RAKETA_LISTEN_ADDRESS")
var DBFILEPATH = os.Getenv("RAKETA_DB_FILE_PATH")
var ELEVATECOST, _ = strconv.Atoi(os.Getenv("RAKETA_ELEVATE_COST"))
var FLAG = os.Getenv("RAKETA_FLAG")

var GameTexts = map[string]string{
	"welcome": "Welcome to text-based system of Raketa project!" + "\n" +
		"### actions ###" + "\n" +
		"(l/L) login" + "\n" +
		"(s/S) signup" + "\n" +
		"(h/H) help menu" + "\n" +
		"(e/E) exit" + "\n\n",
	"help": "This is help menu of Raketa project." + "\n" +
		"Currently, you are not logged in, due to that" + "\n" +
		"You have no rights to knew what Raketa project is." + "\n" +
		"Firstly, you need to signin if you already have credentials" + "\n" +
		"or signup in case you haven't done this before." + "\n" +
		"### actions ###" + "\n" +
		"(b/B) back" + "\n\n",
	"signupLogin":        "Login: ",
	"signupPassword":     "Password: ",
	"signupLoginError":   "User with that login exists" + "\n",
	"loginLogin":         "Login: ",
	"loginPassword":      "Password: ",
	"loginLoginError":    "No user with that login exists" + "\n",
	"loginPasswordError": "Wrong password" + "\n",
	"error":              "Unexpected error" + "\n",
	"welcomeLogged": "Main menu." + "\n" +
		"Current user: %v." + "\n" +
		"### actions ###" + "\n" +
		"(t/T) get task" + "\n" +
		"(e/E) elevate privileges" + "\n" +
		"(i/I) user info" + "\n" +
		"(h/H) help menu" + "\n" +
		"(l/L) log off" + "\n\n",
	"task": "Your current task:" + "\n" +
		"%v" + "\n" +
		"### actions ###" + "\n" +
		"(c/C) send calculation result" + "\n" +
		"(b/B) back" + "\n\n",
	"userInfo": "User info" + "\n" +
		"Login: %v" + "\n" +
		"Reputation: %v" + "\n" +
		"### actions ###" + "\n" +
		"(b/B) back" + "\n\n",
	"helpLogged": "This is help menu of Raketa project." + "\n" +
		"Raketa project is distrubuted computing platform for rocket science calculations." + "\n" +
		"Most of time, you needed to calculate delta v through Tsiolkovsky rocket equation," + "\n" +
		"and that's why we decided to provide to you some theory:" + "\n" +
		"delta v = Ve * ln( M0 / Mf)," + "\n" +
		"where delta v is change of the velocity of the rocket," + "\n" +
		"Ve (m/s) is effective exhaust velocity," + "\n" +
		"M0 (tonnes) is initial mass of rocket (rocket mass itself + propellants)" + "\n" +
		"Mf (tonnes) is final mass (rocket mass without propellants)" + "\n" +
		"Sometimes, might be, we wont have correct Ve, but would have specific impulse." + "\n" +
		"It might be happening due to that fact, that not of all of our ships in nearby Earth space" + "\n" +
		"In that case you would need to calculate Ve by yourself, and we would provide you with gravity measures" + "\n" +
		"Here's formula needed to calculate" + "\n" +
		"Ve = G0 * Isp" + "\n" +
		"where G0 (m/s^2) is gravity standard (for earth is 9.80665m/s^2)" + "\n" +
		"and Isp (seconds) is specific impulse in seconds" + "\n" +
		"### actions ###" + "\n" +
		"(b/B) back" + "\n\n",
	"elevatePrivileges": "This is menu, where you can change gained reputation for a new rank." + "\n" +
		"Current user: %v" + "\n" +
		"Your current reputation score is: %v" + "\n" +
		"Cost of privileges elevation is: " + strconv.Itoa(ELEVATECOST) + "\n" +
		"### actions ###" + "\n" +
		"(e/E) change reputation to a new rank" + "\n" +
		"(b/B) back" + "\n\n",
	"elevateSuccess": "Successfuly elevated privileges." + "\n" +
		"Spended %v reputation." + "\n" +
		"### actions ###" + "\n" +
		"(b/B) back" + "\n\n",
	"welcomeElevated": "Main menu." + "\n" +
		"Current user: %v." + "\n" +
		"### actions ###" + "\n" +
		"(t/T) get task" + "\n" +
		"(e/E) elevate privileges" + "\n" +
		"(f/F) get flag" + "\n" +
		"(i/I) user info" + "\n" +
		"(h/H) help menu" + "\n" +
		"(l/L) log off" + "\n\n",
	"bye": "Bye" + "\n\n",
}

var DBMutex sync.Mutex

var ErrBadLogin = errors.New("bad login")
var ErrBadPassword = errors.New("bad password")

type User struct {
	Login      string  `json:"login"`
	Password   string  `json:"password"`
	Reputation int     `json:"reputation"`
	Task       string  `json"task"`
	TaskResult float64 `json:"task_result"`
	Elevated   bool    `json:"elevated"`
}

func InitUser(login string, password string) User {
	var result User
	result.Login = login
	result.Password = password
	result.Reputation = 0
	result.Task = "Ve = 1000m/s" + "\n" +
		"M0 = 100t" + "\n" +
		"Mf = 10t" + "\n" +
		"delta V - ?"
	result.TaskResult = 1000 * math.Log(100/10)
	result.Elevated = false
	return result
}

func GenerateTask() (string, float64) {
	r := rand.New(rand.NewSource(time.Now().UnixNano()))
	var task string
	var taskResult float64
	if r.Intn(2) == 0 {
		Ve := 1000 + r.Intn(1000)
		M0 := 100 + r.Intn(10)
		Mf := 10 + r.Intn(50)
		taskResult = float64(Ve) * math.Log(float64(M0)/float64(Mf))
		task = fmt.Sprintf("Ve = %vm/s\nM0 = %vt\nMf = %vt\ndelta V - ?", strconv.Itoa(Ve), strconv.Itoa(M0), strconv.Itoa(Mf))
		return task, taskResult
	} else {
		G0 := 1 + r.Intn(20)
		Isp := 10 + r.Intn(990)
		M0 := 100 + r.Intn(10)
		Mf := 10 + r.Intn(50)
		taskResult = float64(G0*Isp) * math.Log(float64(M0)/float64(Mf))
		task = fmt.Sprintf("GO = %vm/s^2\nIsp = %vs\nM0 = %vt\nMf = %vt\ndelta V - ?", strconv.Itoa(G0), strconv.Itoa(Isp), strconv.Itoa(M0), strconv.Itoa(Mf))
		return task, taskResult
	}
}

func GetUserByLoginPasswordPair(login string, password string) (User, error) {
	file, err := os.Open(DBFILEPATH)
	if err != nil {
		return User{}, err
	}
	defer file.Close()
	fileContent, _ := ioutil.ReadAll(file)
	var users []User
	json.Unmarshal(fileContent, &users)
	for _, v := range users {
		if v.Login == login {
			if v.Password == password {
				return v, nil
			} else {
				return User{}, ErrBadPassword
			}
		}
	}
	return User{}, ErrBadLogin
}

func CreateUserInDB(login string, password string) error {
	DBMutex.Lock()
	defer DBMutex.Unlock()
	file, err := os.Open(DBFILEPATH)
	if err != nil {
		return err
	}
	fileContent, _ := ioutil.ReadAll(file)
	file.Close()
	var users []User
	json.Unmarshal(fileContent, &users)
	var exists bool = false
	for _, userInDB := range users {
		if userInDB.Login == login {
			exists = true
		}
	}
	if !exists {
		user := InitUser(login, password)
		users = append(users, user)
	} else {
		return ErrBadLogin
	}
	fileContent, _ = json.Marshal(users)
	err = ioutil.WriteFile(DBFILEPATH, fileContent, 0644)
	return err
}

func UpdateUserInDB(user User) error {
	DBMutex.Lock()
	defer DBMutex.Unlock()
	file, err := os.Open(DBFILEPATH)
	if err != nil {
		return err
	}
	defer file.Close()
	fileContent, _ := ioutil.ReadAll(file)
	var users []User
	json.Unmarshal(fileContent, &users)
	for usersIndex, userInDB := range users {
		if userInDB.Login == user.Login && userInDB.Password == user.Password {
			users[usersIndex] = user
		}
	}
	fileContent, _ = json.Marshal(users)
	err = ioutil.WriteFile(DBFILEPATH, fileContent, 0644)
	return err
}

func handleConnection(c net.Conn) {
	log.Info(fmt.Sprintf("Serving %v\n", c.RemoteAddr()))
	var state string = "welcome"
	defer c.Close()
	var user User
	for {
		if state == "welcome" {
			c.Write([]byte(GameTexts["welcome"]))
			message, _ := bufio.NewReader(c).ReadString('\n')
			message = strings.ToLower(strings.TrimSpace(message))
			if len(message) != 0 {
				if message == "l" {
					log.Info(fmt.Sprintf("Connection from %v requested login action", c.RemoteAddr()))
					state = "login"
				} else if message == "s" {
					log.Info(fmt.Sprintf("Connection from %v requested signup action", c.RemoteAddr()))
					state = "signup"
				} else if message == "h" {
					log.Info(fmt.Sprintf("Connection from %v requested help menu", c.RemoteAddr()))
					state = "help"
				} else if message == "e" {
					log.Info(fmt.Sprintf("Connection from %v requested end of connection", c.RemoteAddr()))
					c.Write([]byte(GameTexts["bye"]))
					return
				} else {
					log.Warn(fmt.Sprintf("Received action '%v' from %v", string(message), c.RemoteAddr()))
				}
			}
		} else if state == "login" {
			var login, password string
			c.Write([]byte(GameTexts["loginLogin"]))
			message, _ := bufio.NewReader(c).ReadString('\n')
			message = strings.ToLower(strings.TrimSpace(message))
			if len(message) != 0 {
				login = string(message)
				log.Info(fmt.Sprintf("In login attempt received login '%v' from %v", login, c.RemoteAddr()))
			}
			c.Write([]byte(GameTexts["loginPassword"]))
			message, _ = bufio.NewReader(c).ReadString('\n')
			message = strings.ToLower(strings.TrimSpace(message))
			if len(message) != 0 {
				password = string(message)
				log.Info(fmt.Sprintf("In login attempt received login '%v' with password '%v' from %v", login, password, c.RemoteAddr()))
			}
			var err error
			user, err = GetUserByLoginPasswordPair(login, password)
			if err != nil {
				log.Warn(fmt.Sprintf("Login attempt from %v caused error: %v", c.RemoteAddr(), err))
				switch {
				case errors.Is(err, ErrBadLogin):
					c.Write([]byte(GameTexts["loginLoginError"]))
				case errors.Is(err, ErrBadPassword):
					c.Write([]byte(GameTexts["loginPasswordError"]))
				default:
					c.Write([]byte(GameTexts["error"]))
				}
				state = "welcome"
			} else {
				log.Info(fmt.Sprintf("User %v logged in from address %v", user.Login, c.RemoteAddr()))
				state = "welcomeLogged"
			}
		} else if state == "signup" {
			var login, password string
			c.Write([]byte(GameTexts["signupLogin"]))
			message, _ := bufio.NewReader(c).ReadString('\n')
			message = strings.ToLower(strings.TrimSpace(message))
			if len(message) != 0 {
				login = string(message)
				log.Info(fmt.Sprintf("In signup attempt received login '%v' from %v", login, c.RemoteAddr()))
			}
			c.Write([]byte(GameTexts["signupPassword"]))
			message, _ = bufio.NewReader(c).ReadString('\n')
			message = strings.ToLower(strings.TrimSpace(message))
			if len(message) != 0 {
				password = string(message)
				log.Info(fmt.Sprintf("In signup attempt received login '%v' with password '%v' from %v", login, password, c.RemoteAddr()))
			}
			var err error
			err = CreateUserInDB(login, password)
			if err != nil {
				log.Warn(fmt.Sprintf("Signup attempt from %v caused error: %v", c.RemoteAddr(), err))
				switch {
				case errors.Is(err, ErrBadLogin):
					c.Write([]byte(GameTexts["signupLoginError"]))
				default:
					c.Write([]byte(GameTexts["error"]))
				}
			} else {
				log.Info(fmt.Sprintf("Created new user with login '%v' and password '%v'", login, password))
			}
			state = "welcome"
		} else if state == "help" {
			c.Write([]byte(GameTexts["help"]))
			message, _ := bufio.NewReader(c).ReadString('\n')
			message = strings.ToLower(strings.TrimSpace(message))
			if len(message) != 0 && message == "b" {
				state = "welcome"
			}
		} else if state == "welcomeLogged" {
			if !user.Elevated {
				c.Write([]byte(fmt.Sprintf(GameTexts["welcomeLogged"], user.Login)))
			} else {
				c.Write([]byte(fmt.Sprintf(GameTexts["welcomeElevated"], user.Login)))
			}
			message, _ := bufio.NewReader(c).ReadString('\n')
			message = strings.ToLower(strings.TrimSpace(message))
			if len(message) != 0 {
				if message == "t" {
					log.Info(fmt.Sprintf("User %v requested task action", user.Login))
					state = "task"
				} else if message == "e" {
					log.Info(fmt.Sprintf("User %v requested elevate privileges action", user.Login))
					state = "elevatePrivileges"
				} else if message == "i" {
					log.Info(fmt.Sprintf("User %v requested user info menu", user.Login))
					state = "userInfo"
				} else if message == "h" {
					log.Info(fmt.Sprintf("User %v requested help menu", user.Login))
					state = "helpLogged"
				} else if message == "l" {
					log.Info(fmt.Sprintf("User %v requested log off action", user.Login))
					user = User{}
					state = "welcome"
				} else if message == "f" && user.Elevated {
					log.Info(fmt.Sprintf("User %v requested flag", user.Login))
					c.Write([]byte(FLAG + "\n"))
				} else {
					log.Warn(fmt.Sprintf("Received action '%v' from %v", string(message), user.Login))
				}
			}
		} else if state == "task" {
			c.Write([]byte(fmt.Sprintf(GameTexts["task"], user.Task)))
			message, _ := bufio.NewReader(c).ReadString('\n')
			message = strings.ToLower(strings.TrimSpace(message))
			if len(message) != 0 {
				if message == "c" {
					log.Info(fmt.Sprintf("User %v want to send his calculations", user.Login))
					state = "task"
					c.Write([]byte("Enter result: "))
					message, _ := bufio.NewReader(c).ReadString('\n')
					message = strings.ToLower(strings.TrimSpace(message))
					if len(message) != 0 {
						if s, err := strconv.ParseFloat(message, 64); err == nil {
							if user.TaskResult-1 < s && user.TaskResult+1 > s {
								log.Info(fmt.Sprintf("User %v succesfuly solved his task... +rep!", user.Login))
								user.Reputation++
								task, taskResult := GenerateTask()
								user.Task = task
								user.TaskResult = taskResult
								err = UpdateUserInDB(user)
								if err != nil {
									log.Warn("Error while saving user in db...")
									c.Write([]byte("Error while saving user in db...\n"))
								}
								c.Write([]byte("Correct. +rep.\nFound new task!\n"))
							} else {
								log.Info(fmt.Sprintf("User %v couldn't solve his task with calculated result %v and real result is %v", user.Login, message, user.TaskResult))
								c.Write([]byte("Wrong answer\n"))
							}
						} else {
							log.Warn(fmt.Sprintf("User %v tried to send %v as float64", user.Login, message))
							c.Write([]byte("Couldn't parse this as float"))
						}
					}
				} else if message == "b" {
					log.Info(fmt.Sprintf("User %v requested going back from task menu", user.Login))
					state = "welcomeLogged"
				}
			}
		} else if state == "elevatePrivileges" {
			c.Write([]byte(fmt.Sprintf(GameTexts["elevatePrivileges"], user.Login, user.Reputation)))
			message, _ := bufio.NewReader(c).ReadString('\n')
			message = strings.ToLower(strings.TrimSpace(message))
			if len(message) != 0 {
				if message == "e" {
					log.Info(fmt.Sprintf("User %v requested elevation", user.Login))
					if user.Reputation >= ELEVATECOST {
						state = "welcomeLogged"
						user.Reputation -= ELEVATECOST
						user.Elevated = true
						err := UpdateUserInDB(user)
						if err != nil {
							log.Warn("Error while saving user in db...")
							c.Write([]byte("Error while saving user in db...\n"))
						}
						c.Write([]byte("Elevated privileges.\n"))
					}
				}
				if message == "b" {
					log.Info(fmt.Sprintf("User %v requested going back from elevation privileges menu", user.Login))
					state = "welcomeLogged"
				}
			}
		} else if state == "userInfo" {
			c.Write([]byte(fmt.Sprintf(GameTexts["userInfo"], user.Login, user.Reputation)))
			message, _ := bufio.NewReader(c).ReadString('\n')
			message = strings.ToLower(strings.TrimSpace(message))
			if len(message) != 0 {
				if message == "b" {
					log.Info(fmt.Sprintf("User %v requested going back from user info menu", user.Login))
					state = "welcomeLogged"
				}
			}
		} else if state == "helpLogged" {
			c.Write([]byte(fmt.Sprintf(GameTexts["helpLogged"])))
			message, _ := bufio.NewReader(c).ReadString('\n')
			message = strings.ToLower(strings.TrimSpace(message))
			if len(message) != 0 {
				if message == "b" {
					log.Info(fmt.Sprintf("User %v requested going back from help menu", user.Login))
					state = "welcomeLogged"
				}
			}
		}
	}
}

func IsFileExists(filename string) bool {
	info, err := os.Stat(filename)
	if os.IsNotExist(err) {
		return false
	}
	return !info.IsDir()
}

func main() {
	log.SetFormatter(&log.TextFormatter{
		DisableColors: false,
		FullTimestamp: true,
	})
	log.SetLevel(log.TraceLevel)
	log.SetOutput(os.Stdout)
	log.Info(fmt.Sprintf("Starting server on addr: %v...", LISTENADDRESS))

	if !IsFileExists(DBFILEPATH) {
		os.Create(DBFILEPATH)
	}

	ln, _ := net.Listen("tcp", LISTENADDRESS)
	defer ln.Close()
	for {
		conn, err := ln.Accept()
		if err != nil {
			log.Warn(err)
		}
		go handleConnection(conn)
	}
}
