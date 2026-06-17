#define _DEFAULT_SOURCE
#define MG_IMPLEMENTATION
#include "minigamepad.h"

#ifdef _WIN32
#include <windows.h>
#else
#include <unistd.h>
#endif

void sleep_ms(int ms) {
#ifdef _WIN32
    Sleep((DWORD)ms);
#else
    usleep((useconds_t)(ms * 1000));
#endif
}

int main(void) {
    mg_gamepads gamepads;
    mg_gamepads_init(&gamepads);

    printf("Minigamepad Rumble Example\n");
    printf("Connect a controller...\n");

    while (1) {
        mg_gamepad* gamepad;
        
        mg_gamepads_poll(&gamepads);

        for (gamepad = gamepads.list.head; gamepad; gamepad = gamepad->next) {
            if (gamepad->connected) {
                printf("Rumbling gamepad: %s\n", gamepad->name);
                
                /* Rumble: Low freq 50%, High freq 50% */
                mg_gamepad_rumble(gamepad, 0.5f, 0.5f);
                
                /* Wait 1 second */
                sleep_ms(1000);
                
                /* Stop rumble */
                mg_gamepad_rumble(gamepad, 0.0f, 0.0f);
                printf("Stopped rumble for: %s\n", gamepad->name);

                /* Wait 1 second before next action */
                sleep_ms(1000);
            }
        }
        
        /* Small sleep to avoid high CPU usage if no controllers connected */
        sleep_ms(10);
    }

    mg_gamepads_free(&gamepads);
    return 0;
}
