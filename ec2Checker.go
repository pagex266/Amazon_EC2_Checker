package main

// Used imports
import (
  "bufio"
  "net"
  "regexp"
  "fmt"
  "os"
)

/*
 * check(e)
 * Takes in an error variable.
 * checks if error is valid quits if there is an error
 */
func check(e error) {
  if (e != nil) {
    panic(e)
  }
}

/*
 * isEC2(name)
  * Takes in a string.
  * Uses a regex to determine if the paratmeter has an ec2 addresses.
  * Return true if there is a match.
 */
func isEC2(name string) bool {
  match, err := regexp.MatchString("ec2-(.*)", name)
  check(err)

  if (match) {
    return true
  } else {
    return false
  }
}
/*
 * lookupName(ip)
 * Takes in a string
 * Uses the net package to find the name the domain names the ipv4 addresses maps to.
 */
func lookupName(ip string) {
  names, err := net.LookupAddr(ip)
  if (err == nil) {
    for _, name := range names {
      if (isEC2(name)) {
        fmt.Printf("%s\t-> [+] %s\n", ip, name)
      }
    }
  }
}

/*
 * main()
 *  Checks Parameters
 *  Itterates through json file to find ipv4 addresses
 *
 */
func main() {
    // Make sure an argument exists
    if (len(os.Args) != 2) {
      fmt.Printf("ERROR: ip-ranges.json must be the one and only argument.\n")
    } else {
      // Make sure the argumet is ip-ranges.json
      if (os.Args[1] != "ip-ranges.json") {
        // Print an error message
        fmt.Printf("ERROR: ip-ranges.json must be the one and only argument.\n")
      } else {

        // Open the JSON file and check for errors
        file, err := os.Open(os.Args[1])
        check(err)

        defer file.Close()

        // Make a regex for valid ipv4 addresses and make sure it compiles
        regex, err := regexp.Compile("([0-9]+).([0-9]+).([0-9]+).([0-9]+)")
        check(err)


        // itterate through arrays.
        scanner := bufio.NewScanner(file)
        for scanner.Scan() {
          if (regex.MatchString(scanner.Text())) {
            lookupName(regex.FindString(scanner.Text()))
          }
        }
      }
    }
}
