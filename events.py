def calc_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(event.type,event.button)
            if event.button == 1:
                if rectangle.collidepoint(event.pos):
                    rectangle_draging = True
                    mouse_x, mouse_y = event.pos
                    offset_x = rectangle.x - mouse_x
                    offset_y = rectangle.y - mouse_y
            elif event.button == 4:
                ZOOM+=0.01
            elif event.button == 5:
                ZOOM-=0.01


        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                rectangle_draging = False


        elif event.type == pygame.MOUSEMOTION:
            if rectangle_draging:
                mouse_x, mouse_y = event.pos
                rectangle.x = mouse_x + offset_x
                rectangle.y = mouse_y + offset_y

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                TRANSLATE[1]+=1
            elif event.key == pygame.K_DOWN:
                TRANSLATE[1]-=1
            elif event.key == pygame.K_LEFT:
                TRANSLATE[0]+=1
            elif event.key == pygame.K_RIGHT:
                TRANSLATE[0]-=1
