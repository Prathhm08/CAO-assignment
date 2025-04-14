import pygame
import sys
import time

pygame.init()
WIDTH, HEIGHT = 1200, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Non-Restoring Division - Blackboard Style")
font = pygame.font.SysFont("consolas", 26)
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


def bin_add(a, b):
    result = int(a, 2) + int(b, 2)
    return bin(result % (1 << len(a)))[2:].zfill(len(a))


def bin_sub(a, b):
    result = int(a, 2) - int(b, 2)
    if result < 0:
        result += 1 << len(a)
    return bin(result)[2:].zfill(len(a))


def draw_title():
    screen.fill((20, 20, 20))
    title = font.render("Non-Restoring Division Algorithm", True, (255, 255, 255))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))

    headers = ["Step", "A", "Q", "Operation", "Note"]
    positions = [50, 150, 350, 500, 750]
    for i, header in enumerate(headers):
        h_text = small_font.render(header, True, (200, 200, 200))
        screen.blit(h_text, (positions[i], 80))
    pygame.display.update()


def draw_step_header(step_num, y_offset):
    step_text = f"Step {step_num}"
    label = small_font.render(step_text, True, (0, 255, 0))
    pygame.draw.line(screen, (100, 100, 100), (40, y_offset), (1150, y_offset), 2)
    screen.blit(label, (50, y_offset - 30))
    pygame.display.update()


def log_step(substep, A, Q, op, note, y_offset, draw_link=False):
    if draw_link:
        draw_connection_line(A, Q, y_offset)
    values = [str(substep), A, Q, op, note]
    positions = [50, 150, 350, 500, 750]
    for i, val in enumerate(values):
        v_text = small_font.render(val, True, (255, 255, 255))
        screen.blit(v_text, (positions[i], y_offset))
    pygame.display.update()
    wait(1.1)


def draw_connection_line(A, Q, y_offset):
    msb_a_x = 155 + 10 * 0  # A starts at x=150, MSB is at char index 0
    lsb_q_x = 365 + 10 * (len(Q) - 1)  # Q starts at x=350

    mid_y = y_offset - 8
    top_y = mid_y - 7
    bottom_y = top_y + 12

    pygame.draw.line(screen, (0, 255, 255), (msb_a_x, top_y), (msb_a_x, mid_y), 2)
    pygame.draw.line(screen, (0, 255, 255), (msb_a_x, mid_y), (lsb_q_x, mid_y), 2)
    pygame.draw.line(screen, (0, 255, 255), (lsb_q_x, mid_y), (lsb_q_x, bottom_y), 2)

    arrow_height = 6
    arrow_width = 3
    arrow_points = [
        (lsb_q_x - arrow_width, bottom_y),
        (lsb_q_x + arrow_width, bottom_y),
        (lsb_q_x, bottom_y + arrow_height),
    ]
    pygame.draw.polygon(screen, (0, 255, 255), arrow_points)
    wait(0.2)


def non_restoring_division(dividend, divisor):
    n = 4
    A = "00000"
    Q = dividend.zfill(n)
    M = divisor.zfill(5)

    draw_title()
    y = 120
    log_step("0", A, Q, "INIT", "Initial state", y)

    for step in range(1, n + 1):
        y += 80
        draw_step_header(step, y - 20)

        # Substep 1: Shift left AQ
        AQ = A + Q
        AQ = AQ[1:] + "0"
        A, Q = AQ[:5], AQ[5:]
        log_step(f"{step}.1", A, Q, "Shift Left", "A and Q shifted", y)

        y += 40
        # Substep 2: A +/- M depending on sign of A
        if A[0] == "0":
            A_temp = bin_sub(A, M)
            op_note = "A ≥ 0 → A - M"
            operation = "A - M"
        else:
            A_temp = bin_add(A, M)
            op_note = "A < 0 → A + M"
            operation = "A + M"
        log_step(f"{step}.2", A_temp, Q, operation, op_note, y)

        y += 40
        # Substep 3: Set Q0
        if A_temp[0] == "0":
            Q = Q[:-1] + "1"
            note = "A ≥ 0 → Q0 ← 1"
        else:
            Q = Q[:-1] + "0"
            note = "A < 0 → Q0 ← 0"
        A = A_temp
        log_step(f"{step}.3", A, Q, "Set Q0", note, y, draw_link=True)

    # Final correction if A < 0
    if A[0] == "1":
        y += 60
        A = bin_add(A, M)
        log_step("F", A, Q, "Restore A", "A was negative → A + M", y)

    y += 60
    result_text = f"Final Quotient: {Q}, Remainder: {A}"
    result_render = small_font.render(result_text, True, (255, 255, 0))
    screen.blit(result_render, (50, y))

    y += 22
    dec_result_text = f"(Decimal) Dividend: {int(dividend,2)} Divisor: {int(divisor,2)} Quotient: {int(Q,2)}, Remainder: {int(A,2)}"
    dec_result_render = small_font.render(dec_result_text, True, (255, 255, 0))
    screen.blit(dec_result_render, (50, y))

    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        clock.tick(60)


if __name__ == "__main__":
    # Run with 4-bit inputs
    non_restoring_division("1011", "0011")  # 12 ÷ 3
