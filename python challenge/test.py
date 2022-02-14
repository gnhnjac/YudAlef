# cow.html
# a = '1'
# print(0,len(a))
# for j in range(1,31):
#     a2 = ''

#     current = a[0]
#     amount = 0

#     for letter in a:
#         if letter == current:
#             amount+=1
#         else:
#             a2 += str(amount) + current
#             amount = 1
#             current = letter

#     a2 += str(amount) + current

#     print(j,len(a2))
#     a = a2

# 5808.html
# from PIL import Image

# img = Image.open('cave.jpg')

# new = Image.new(mode="RGB", size=(img.size[0],img.size[1]))

# for i in range(img.size[0])[::2]:
#     for j in range(img.size[1])[::2]:
#         new.putpixel((int(i/2), int(j/2)), img.getpixel((i,j)))

# new.show()

# evil.html
#
# with open('evil2.gfx', 'rb') as f1:
#
#     decoded = f1.read()
#
#     r1 = decoded[::5]
#
#     with open('evil25.jpg', 'wb') as f2:
#         f2.write(r1)

# http://www.pythonchallenge.com/pc/return/disproportional.html

# import PIL
# import xmlrpc.client
#
# with xmlrpc.client.ServerProxy("http://www.pythonchallenge.com/pc/phonebook.php") as proxy:
#     print(proxy.system.listMethods())
#     print(proxy.system.methodHelp('phone'))
#     print(proxy.system.getCapabilities())
#     print(proxy.phone('Bert'))

# http://www.pythonchallenge.com/pc/return/italy.html ( huge:file)

from PIL import Image, ImageChops

im = Image.open('wire.png')

im2 = Image.new('RGB', (100,100))

# bit.html you took the wrong curve
#
# x = 50
# y = 50
#
# stage = 'up'
#
# lst = []
# for i in range(1,100):
#     lst.append(i)
#     lst.append(i)
#
# line_ind = 0
# for i in lst:
#     for j in range(i):
#         if stage == 'up':
#             im2.putpixel((x,y),im.getpixel((9999-line_ind,0)))
#             y-=1
#         elif stage =='left':
#             im2.putpixel((x, y), im.getpixel((9999-line_ind,0)))
#             x-=1
#         elif stage =='down':
#             im2.putpixel((x, y), im.getpixel((9999-line_ind,0)))
#             y+=1
#         elif stage =='right':
#             im2.putpixel((x, y), im.getpixel((9999-line_ind,0)))
#             x+=1
#         line_ind+=1
#     print(i,stage)
#
#     if stage == 'up':
#         stage = 'left'
#     elif stage == 'left':
#         stage = 'down'
#     elif stage == 'down':
#         stage = 'right'
#     elif stage == 'right':
#         stage = 'up'
# print(line_ind)
# im2.save('asd.png')

# http://www.pythonchallehugenge.com/pc/return/cat.html

# cat's name is uzi, ill hear from him later!!!

