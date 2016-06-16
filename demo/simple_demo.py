import pyscreenshot as ImageGrab
from pymouse import PyMouse
from pykeyboard import PyKeyboard


g_k = PyKeyboard()
g_m = PyMouse()

print("Press Keyboard: Return Key.")
g_k.press_key(g_k.return_key)

print("Move Mouse: (0, 0)")
g_m.move(0, 0)


image = ImageGrab.grab()
print("Print Image Pixel.")
print(image.getpixel((0, 0)))
