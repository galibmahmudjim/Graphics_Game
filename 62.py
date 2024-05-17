

def get_text_width(text, font=GLUT_STROKE_ROMAN, scale=1, spacing=0):
    width = 0
    for ch in text:
        width += glutStrokeWidth(font, ord(ch)) * scale + spacing
    return width

def draw_bold_text(x, y, text, font=GLUT_STROKE_ROMAN, scale=0.3, thickness=3, spacing=10):
    glPushMatrix()
    glTranslatef(x, y, 0)
    glScalef(scale, scale, scale)
    for dx in range(-thickness, thickness+1):
        for dy in range(-thickness, thickness+1):
            if dx != 0 or dy != 0:
                glPushMatrix()
                glTranslatef(dx, dy, 0)
                for ch in text:
                    glutStrokeCharacter(font, ord(ch))
                    glTranslatef(spacing, 0, 0)
                glPopMatrix()
    glColor3f(1, 1, 1)  # Set text color to white
    for ch in text:
        glutStrokeCharacter(font, ord(ch))
        glTranslatef(spacing, 0, 0)
    glPopMatrix()

def render_homepage():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Text properties
    text1 = "Press SPACE to Start"
    text2 = "Welcome to My Awesome Game!"
    scale = 0.3
    thickness = 2
    spacing = 10

    # Calculate centered positions
    text1_width = get_text_width(text1, GLUT_STROKE_ROMAN, scale, spacing)
    text2_width = get_text_width(text2, GLUT_STROKE_ROMAN, scale, spacing)
    x1 = (W - text1_width) / 2 / scale
    x2 = (W - text2_width) / 2 / scale
    y1 = 300 / scale
    y2 = 350 / scale

    # Set the text color to red
    glColor3f(1, 0, 0)
    draw_bold_text(x1, y1, text1, GLUT_STROKE_ROMAN, scale, thickness, spacing)

    # Set the text color to green
    glColor3f(0, 1, 0)
    draw_bold_text(x2, y2, text2, GLUT_STROKE_ROMAN, scale, thickness, spacing)

    glfw.swap_buffers(window)
