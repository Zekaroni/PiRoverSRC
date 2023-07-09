#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <linux/input.h>

int main()
{
    int fd = open("/dev/input/event18", O_RDONLY);
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
        {
        printf("ID: %d, Value: %d\n", ev.code, ev.value);
        }
    }
    close(fd);
    return 0;
}