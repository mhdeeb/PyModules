from time import perf_counter

import pygame

from Vector import Vector2
from Cart import Cart
from Ball import Ball

if __name__ == '__main__':
    # Initialize pygame
    pygame.init()
    width, height = 1920, 500
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Dynamic Collision")
    clock = pygame.time.Clock()
    font_size = 20
    font = pygame.font.SysFont("Courier New", font_size, True)
    center = Vector2(width // 2, height // 2)
    running = True

    console = True  # Set to False to disable console output
    cart_bounce = False  # Set to True to enable bouncing off the cart

    r = 50  # Ball radius
    d = 300  # Cart width / 2
    cart = Cart(origin=Vector2(center.x, height - 40), width=int(2 * d), height=2 * r, color="red")
    ball = Ball(center=Vector2(center.x, height - 2 * (20 + r) + r + 2), radius=r - 2, color="blue")
    dt = 1 / 120  # Time step

    v0 = 200
    cart.velocity = Vector2(0, 0)
    ball.velocity = Vector2(-v0, 0)
    ball.mass = 1
    cart.mass = 5
    e = 0.8  # Coefficient of restitution

    # Collision Response Coefficients
    c1 = (ball.mass - e * cart.mass) / (ball.mass + cart.mass)
    c2 = (1 + e) * cart.mass / (ball.mass + cart.mass)
    c3 = (1 + e) * ball.mass / (ball.mass + cart.mass)
    c4 = (cart.mass - e * ball.mass) / (ball.mass + cart.mass)

    t0 = perf_counter()  # t0
    collisions = 0  # Collision Counter

    while running:
        window.fill('black')

        # Check for Collision
        if not ball.radius <= (ball.points[0] - cart.points[0]).x <= cart.width - ball.radius:
            if (ball.points[0] - cart.points[0]).x <= ball.radius:
                site = 'A'
                ball.points[0].x = cart.points[0].x + ball.radius
            else:
                site = 'B'
                ball.points[0].x = cart.points[0].x + cart.width - ball.radius

            # Collision Response
            temp_v = ball.velocity.x
            ball.velocity.x = temp_v * c1 + cart.velocity.x * c2
            cart.velocity.x = temp_v * c3 + cart.velocity.x * c4

            collisions += 1

            if console:
                print(
                    f"\n{collisions}th collision at {site}:\n"
                    f"Time: {perf_counter() - t0:>5.2f}s\n"
                    f"{'Ball Velocity:':<23}{ball.velocity:>10.2f}\n"
                    f"{'Cart Velocity:':<23}{cart.velocity:>10.2f}\n"
                    f"{'Total Momentum:':<23}{ball.momentum() + cart.momentum():>10.2f}\n"
                    f"Total Kinetic Energy:{ball.kinetic_energy() + cart.kinetic_energy():>24.2f}"
                )

        if cart_bounce:
            if cart.points[0].x <= 1:
                cart.velocity.x = abs(cart.velocity.x)
            elif cart.points[0].x + cart.width + 1 >= width:
                cart.velocity.x = -abs(cart.velocity.x)

        ball.move(dt)
        cart.move(dt)

        cart.draw(window)
        ball.draw(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        window.blit(font.render(f"Collisions: {collisions}", True, "white"), (10, font_size))
        window.blit(font.render(f"Time: {perf_counter() - t0:>5.2f}s", True, "white"), (10, font_size * 2))
        window.blit(font.render(f"{'Ball Velocity:':<23}{ball.velocity:>10.2f}", True, "white"), (10, font_size * 3))
        window.blit(font.render(f"{'Cart Velocity:':<23}{cart.velocity:>10.2f}", True, "white"), (10, font_size * 4))
        window.blit(font.render(f"{'Total Momentum:':<23}{ball.momentum() + cart.momentum():>10.2f}",
                                True, "white"), (10, font_size * 5))
        window.blit(font.render(f"Total Kinetic Energy:"
                                f"{ball.kinetic_energy() + cart.kinetic_energy():>24.2f}",
                                True, "white"), (10, font_size * 6))
        pygame.display.set_caption(f"Dynamic Collision - {round(clock.get_fps(), 2)} fps")

        clock.tick(120)
        pygame.display.update()

pygame.quit()
quit()
