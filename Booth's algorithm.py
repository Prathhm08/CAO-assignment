import pygame
import sys
import time
import math


# -------- Utility Functions -------- #
def twos_complement(bin_str):
    n = len(bin_str)
    return bin((1 << n) - int(bin_str, 2))[2:].zfill(n)


def binary_add(a, b):
    result = bin(int(a, 2) + int(b, 2))[2:]
    return result[-len(a) :].zfill(len(a))


def binary_sub(a, b):
    return binary_add(a, twos_complement(b))


def arithmetic_right_shift(A, Q, Q_1):
    combined = A + Q + Q_1
    shifted = combined[0] + combined[:-1]
    return shifted[: len(A)], shifted[len(A) : -1], shifted[-1]


# -------- Pygame Setup -------- #
pygame.init()
WIDTH, HEIGHT = 1200, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Booth's Algorithm Visualization")
font = pygame.font.SysFont("consolas", 28)
small_font = pygame.font.SysFont("consolas", 22)
clock = pygame.time.Clock()


def wait(seconds):
    start = time.time()
    while time.time() - start < seconds:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        clock.tick(60)


# -------- Draw Functions -------- #
def draw_registers(step, A, Q, Q_1, msg):
    row_y = 80 + step * 80  # Starting lower + more compact rows

    # Draw table cells
    pygame.draw.rect(screen, (255, 255, 255), (50, row_y, 90, 45), 1)  # A
    pygame.draw.rect(screen, (255, 255, 255), (140, row_y, 90, 45), 1)  # Q
    pygame.draw.rect(screen, (255, 255, 255), (230, row_y, 90, 45), 1)  # Q-1
    pygame.draw.rect(screen, (255, 255, 255), (320, row_y, 620, 45), 1)  # Operation

    # Draw text inside cells
    A_text = font.render(A, True, (0, 255, 0))
    Q_text = font.render(Q, True, (0, 200, 255))
    Q1_text = font.render(Q_1, True, (255, 200, 0))
    Msg_text = small_font.render(msg, True, (255, 255, 255))

    screen.blit(A_text, (60, row_y + 10))
    screen.blit(Q_text, (150, row_y + 10))
    screen.blit(Q1_text, (240, row_y + 10))
    screen.blit(Msg_text, (330, row_y + 12))

    pygame.display.update()
    wait(1.2)


def draw_column_headers():
    header_font = pygame.font.SysFont("consolas", 26, bold=True)
    labels = ["A", "Q", "Q-1", "Operation"]
    positions = [90, 180, 250, 550]
    for label, x in zip(labels, positions):
        label_surface = header_font.render(label, True, (255, 255, 255))
        screen.blit(label_surface, (x, 40))
    pygame.display.update()


def draw_arrows(y, num_bits=8, default_angle_deg=70):
    arrow_color = (255, 100, 100)
    default_arrow_length = 30
    arrowhead_size = 10  # Increased for better visibility
    spacing = 140 // num_bits
    start_x = 70

    for i in range(num_bits):
        # Use 40° angle and longer arrow every 4th
        angle_deg = 40 if (i + 1) % 4 == 0 else default_angle_deg
        arrow_length = 40 if (i + 1) % 4 == 0 else default_arrow_length
        angle_rad = math.radians(angle_deg)

        dx = arrow_length * math.cos(angle_rad)
        dy = arrow_length * math.sin(angle_rad)

        x_start = start_x + i * spacing + (i // 4) * 25
        x_end = x_start + dx
        y_end = y + dy

        # Draw slanted line
        pygame.draw.line(screen, arrow_color, (x_start, y), (x_end, y_end), 2)

        # Draw larger arrowhead
        pygame.draw.polygon(
            screen,
            arrow_color,
            [
                (x_end, y_end),
                (
                    x_end - arrowhead_size * math.cos(angle_rad - math.radians(30)),
                    y_end - arrowhead_size * math.sin(angle_rad - math.radians(30)),
                ),
                (
                    x_end - arrowhead_size * math.cos(angle_rad + math.radians(30)),
                    y_end - arrowhead_size * math.sin(angle_rad + math.radians(30)),
                ),
            ],
        )

    pygame.display.update()
    wait(0.2)


def twos_complement_to_decimal_8(binary_str):
    # Check if it's negative
    if binary_str[0] == "1":
        # 2's complement: invert + add 1
        inverted = "".join("1" if b == "0" else "0" for b in binary_str)
        decimal_value = int(inverted, 2) + 1
        return -decimal_value
    else:
        # Positive number
        return int(binary_str, 2)


def twos_complement_to_decimal_4(binary_str):
    # Check if it's negative
    if binary_str[0] == "1":
        # 2's complement: invert + add 1
        inverted = "".join("1" if b == "0" else "0" for b in binary_str)
        decimal_value = int(inverted, 2) + 1
        return -decimal_value
    else:
        # Positive number
        return int(binary_str, 2)


# -------- Booth’s Algorithm -------- #
def booths_algorithm(multiplicand, multiplier):
    screen.fill((30, 30, 30))
    draw_column_headers()

    M = multiplicand.zfill(4)
    Q = multiplier.zfill(4)
    A = "0000"
    Q_1 = "0"
    count = 4
    step = 0

    draw_registers(step, A, Q, Q_1, "Initial State")

    for _ in range(count):
        step += 1
        msg = ""

        if Q[-1] + Q_1 == "10":
            A = binary_sub(A, M)
            msg = "Q[0]Q-1 = 10 → A = A - M"
        elif Q[-1] + Q_1 == "01":
            A = binary_add(A, M)
            msg = "Q[0]Q-1 = 01 → A = A + M"
        else:
            msg = "Q[0]Q-1 = 00 or 11 → No Operation"

        draw_registers(step, A, Q, Q_1, msg)

        # Shift all (A, Q, Q-1) right
        A, Q, Q_1 = arithmetic_right_shift(A, Q, Q_1)
        step += 1
        draw_arrows(15 + step * 80 + 30, num_bits=len(A + Q))
        draw_registers(step, A, Q, Q_1, "ASR → Arithmetic Shift Right")

    step += 1
    draw_registers(
        step,
        A,
        Q,
        Q_1,
        f"Final Product: {A + Q} (Decimal : {twos_complement_to_decimal_4(multiplicand)} X {twos_complement_to_decimal_4(multiplier)} = {twos_complement_to_decimal_8(A + Q)})",
    )

    # Keep window open
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    sys.exit()


# -------- Inputs -------- #
if __name__ == "__main__":
    # multiplicand = input("Enter 4-bit multiplicand (e.g., 1101): ")
    # multiplier = input("Enter 4-bit multiplier   (e.g., 0011): ")
    # booths_algorithm(multiplicand, multiplier)
    booths_algorithm("1101", "0111")
