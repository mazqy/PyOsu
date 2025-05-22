caled_size = int(d * scale_factor)
        temp_approach_scaled = pg.transform.smoothscale(temp_approach_circle, (scaled_size, scaled_size))

        screen.blit(temp_approach_scaled, temp_approach_scaled.get_rect(center=(x, y)))
