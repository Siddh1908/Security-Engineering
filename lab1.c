#include <wiringPi.h>
#include <stdio.h>
#pragma pack(1)   

// TODO: Define GPIO pin for LED
// The numbers following the LED stand for the wiringPi numbering scheme, On a Raspberry Pi 4: WiringPi 2 (GPIO 27) → Physical pin 13; 


struct {
    char username[8];       
    char password[8];       
    int flag;               
    char system_api_key[32]; 
} data;

int main() {
    //TODO: Setup wiringPi (see test1.c for reference)

    data.flag = 0;
    printf("===Initializing System Password===")
    // Initialize system password (protected secret)
    // TODO: Either prompt for system password and use gets() to take system password as an input or Set data.system_api_key to a password of your choice below
   // snprintf(data.system_api_key, sizeof(data.system_api_key), "SUPER_SECRET_API_KEY_12345");
    printf("System key is loaded in memory (not normally visible to users).\n\n");

    printf("=== VaultApp Login ===\n");
    
    // Prompt for username
    printf("Enter Username:\n");
    // TODO: Use gets() to read into data.username

    // TODO: Prompt for password
    // TODO: Use gets() to read into data.password
    
    // TODO: Print current state and addresses of username, password, and flag

    // TODO: Add logic
    // If flag != 0 → COMPROMISED
    //   Print system_password and turn RED LED ON
    // Else → SAFE
    //   Print "System password protected" 

    return 0;
}
