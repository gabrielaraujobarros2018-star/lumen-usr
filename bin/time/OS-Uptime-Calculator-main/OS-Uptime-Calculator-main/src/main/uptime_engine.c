// uptime_engine.c
// Simple uptime calculation engine - reads from kernel /proc/uptime
// Compile with:  gcc -O2 -Wall -o uptime-engine uptime_engine.c
//               strip uptime-engine     (optional)

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <errno.h>
#include <stdbool.h>

#define PROC_UPTIME_PATH    "/proc/uptime"
#define BUFFER_SIZE         128

typedef struct {
    double uptime_seconds;      // total uptime (most accurate)
    unsigned long days;
    unsigned long hours;
    unsigned long minutes;
    unsigned long seconds;
    unsigned long milliseconds; // fractional part in ms
    bool valid;
} UptimeInfo;

static bool parse_uptime_line(const char *line, UptimeInfo *info) {
    char *endptr;
    double uptime, idle;

    // Format of /proc/uptime:  "uptime_in_seconds  idle_in_seconds\n"
    uptime = strtod(line, &endptr);
    if (endptr == line || *endptr == '\0') {
        return false;
    }

    // Skip whitespace
    while (*endptr == ' ' || *endptr == '\t') endptr++;

    idle = strtod(endptr, NULL);

    // Basic sanity check
    if (uptime < 0.0 || idle < 0.0 || idle > uptime + 1.0) {
        return false;
    }

    info->uptime_seconds   = uptime;
    info->valid            = true;

    // Integer breakdown
    unsigned long total_sec = (unsigned long)uptime;

    info->days         = total_sec / (24 * 3600);
    total_sec         %= (24 * 3600);
    info->hours        = total_sec / 3600;
    total_sec         %= 3600;
    info->minutes      = total_sec / 60;
    info->seconds      = total_sec % 60;

    // Fractional part → milliseconds
    double frac = uptime - (double)total_sec;
    info->milliseconds = (unsigned long)(frac * 1000.0 + 0.5); // round

    return true;
}

bool get_kernel_uptime(UptimeInfo *info) {
    if (!info) return false;

    *info = (UptimeInfo){0};

    FILE *f = fopen(PROC_UPTIME_PATH, "re");
    if (!f) {
        fprintf(stderr, "Cannot open %s: %s\n", PROC_UPTIME_PATH, strerror(errno));
        return false;
    }

    char buffer[BUFFER_SIZE];
    if (!fgets(buffer, sizeof(buffer), f)) {
        fclose(f);
        fprintf(stderr, "Read error from %s\n", PROC_UPTIME_PATH);
        return false;
    }

    fclose(f);

    // Remove trailing newline if present
    size_t len = strlen(buffer);
    if (len > 0 && buffer[len-1] == '\n') {
        buffer[len-1] = '\0';
    }

    return parse_uptime_line(buffer, info);
}

// ────────────────────────────────────────────────
//  Human-friendly output helpers
// ────────────────────────────────────────────────

void print_uptime_human(const UptimeInfo *info) {
    if (!info || !info->valid) {
        printf("Uptime: <error>\n");
        return;
    }

    printf("Uptime: ");

    bool first = true;

    if (info->days > 0) {
        printf("%lu day%s", info->days, info->days > 1 ? "s" : "");
        first = false;
    }

    if (info->hours > 0 || !first) {
        if (!first) printf(", ");
        printf("%lu hour%s", info->hours, info->hours > 1 ? "s" : "");
        first = false;
    }

    if (info->minutes > 0 || !first) {
        if (!first) printf(", ");
        printf("%lu minute%s", info->minutes, info->minutes > 1 ? "s" : "");
        first = false;
    }

    if (!first) printf(" and ");
    printf("%lu.%03lu seconds\n", info->seconds, info->milliseconds);
}

void print_uptime_json(const UptimeInfo *info) {
    if (!info || !info->valid) {
        puts("{\"error\":true}");
        return;
    }

    printf("{\n"
           "  \"uptime_seconds\": %.3f,\n"
           "  \"days\": %lu,\n"
           "  \"hours\": %lu,\n"
           "  \"minutes\": %lu,\n"
           "  \"seconds\": %lu,\n"
           "  \"milliseconds\": %lu,\n"
           "  \"human\": \"%lu days, %lu:%02lu:%02lu\"\n"
           "}\n",
           info->uptime_seconds,
           info->days, info->hours, info->minutes, info->seconds, info->milliseconds,
           info->days, info->hours, info->minutes, info->seconds);
}

int main(void) {
    UptimeInfo info = {0};

    if (!get_kernel_uptime(&info)) {
        return EXIT_FAILURE;
    }

    // Choose your preferred output style:
    // 1. Human readable
    print_uptime_human(&info);

    // 2. JSON (uncomment if you want machine-readable output)
    // print_uptime_json(&info);

    // 3. Just seconds (most precise)
    // printf("%.6f\n", info.uptime_seconds);

    return EXIT_SUCCESS;
}
