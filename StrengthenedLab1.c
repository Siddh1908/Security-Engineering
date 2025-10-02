#include <wiringPi.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#pragma pack(1)   

// TODO: Define GPIO pin for LED
// The numbers following the LED stand for the wiringPi numbering scheme, On a Raspberry Pi 4: WiringPi 2 (GPIO 27) → Physical pin 13; 
#define RED_LED 2

struct {
    char username[8];       
    char password[8];       
    int flag;
    char system_api_key[32]; 
} data;


int main() {
    //TODO: Setup wiringPi (see test1.c for reference)
    wiringPiSetup();
    pinMode(RED_LED, OUTPUT);
    digitalWrite(RED_LED, LOW); 
    data.flag = 0;
    printf("===Initializing System Password===");
    // Initialize system password (protected secret)
    // TODO: Either prompt for system password and use gets() to take system password as an input or Set data.system_api_key to a password of your choice bel>
    snprintf(data.system_api_key, sizeof(data.system_api_key), "SUPER_SECRET_API_KEY_12345");
    printf("System key is loaded in memory (not normally visible to users).\n\n");

    printf("=== VaultApp Login ===\n");
    
    // Prompt for username
    printf("Enter Username:\n");
    // TODO: Use gets() to read into data.username
    scanf("%8s",data.username);
    //  printf("test 1");
    // TODO: Prompt for password
    printf("Enter Password\n");
    // TODO: Use gets() to read into data.password
    scanf("%8s",data.password);
    // TODO: Print current state and addresses of username, password, and flag
    printf("Username: %s, Address: %p \n", data.username, &data.username);
    printf("Password: %s, Address: %p \n", data.password, &data.password);
    printf("Flag: %d, Address: %p \n", data.flag, &data.flag);
    // TODO: Add logic
    // If flag != 0 → COMPROMISED
    //   Print system_password and turn RED LED ON
    // Else → SAFE
    //   Print "System password protected" 
    printf( "This is our flag value %d\n", data.flag);

    if (data.flag != 0) {
        printf("System Compromised \n");
        printf("Password: %s \n", data.password);
        digitalWrite(RED_LED, HIGH); }
    else {
        printf("System is Safe \n");
        printf("System Password Protected \n"); }

    return 0;
}
