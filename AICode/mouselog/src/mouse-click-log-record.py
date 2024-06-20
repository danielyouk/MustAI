from pynput import mouse

# def on_move(x, y):
#     print('Pointer moved to {0}'.format((x, y)))

def on_click(x, y, button, pressed):
    # Distinguish between left and right clicks
    if button == mouse.Button.left:
        click_type = 'Left click'
    elif button == mouse.Button.right:
        click_type = 'Right click'
    else:
        click_type = 'Other click'

    print('{0} {1} at {2}'.format(click_type, 'Pressed' if pressed else 'Released', (x, y)))

# def on_scroll(x, y, dx, dy):
#     print('Scrolled {0} at {1}'.format('down' if dy < 0 else 'up', (x, y)))

listener = mouse.Listener(
    # on_move=on_move,
    on_click=on_click,
    # on_scroll=on_scroll
)
listener.start()

try:
    while True:  # keep the script running
        pass
except KeyboardInterrupt:
    print("Stopped listener")