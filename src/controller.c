#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <linux/input.h>

int DEADZONE = 10;

int main()
{
    int fd = open("/dev/input/event25", O_RDONLY);
    if (fd < 0)
    {
        printf("E Controller not found\n");
        return 1;
    }

    while (1)
    {
        struct input_event ev;
        ssize_t bytesRead = read(fd, &ev, sizeof(struct input_event));
        if (bytesRead < sizeof(struct input_event))
        {
            printf("E Failed to read inputs\n");
            break;
        }

        if (ev.type == EV_KEY || ev.type == EV_ABS)
        {   if (ev.code == 0 || ev.code == 1 || ev.code == 3 || ev.code ==4)
            {
                if (ev.value > (127 + DEADZONE) || ev.value < (127 - DEADZONE))
                {
                    printf("%d, %d\n", ev.code, ev.value);
                }
            }
            else if (ev.code == 2 || ev.code == 5)
            {
                printf("%d, %d\n", ev.code, ev.value);
            }
            else
            {
                printf("%d, %d\n", ev.code, ev.value);
            }
        }
    }
    close(fd);
    return 0;
}