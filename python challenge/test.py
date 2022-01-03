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

width, height = im.size

# for i in range(width-2):
#
#     im2.putpixel((int(i/4), 0), im.getpixel((i,0)))
#     im2.putpixel((int(i / 4), 1), im.getpixel((i+1, 0)))
#     im2.putpixel((int(i / 4), 2), im.getpixel((i+1, 0)))
#     im2.putpixel((int(i / 4), 3), im.getpixel((i+2, 0)))
#
# s = 0
# i = 100
# while i > 0:
#     s += i + i-1 + i-1 + i-2
#
#     i-=2
#
# im3 = Image.new('RGB', (100,100))
#
# shift = 0
# shift2 = 0
# for i in range(25):
#
#     cropped = im2.crop((i*100, 0, i*100+100, 4))
#     cropped= ImageChops.offset(cropped, shift, 0)
#     im3.paste(cropped, (0,i*4))
#     shift+=2+2*shift2
#     shift2+=1

# for j in range(100): # y
#     for i in range(25): # x
#
#         im2.putpixel((i*4,j), im.getpixel((j*100+i*4, 0)))
#         im2.putpixel((i * 4 + 1, j), im.getpixel((j * 100+i*4 + 1, 0)))
#         im2.putpixel((i * 4 + 2, j), im.getpixel((j * 100 +i*4+ 1, 0)))
#         im2.putpixel((i * 4 + 3, j), im.getpixel((j * 100 +i*4+ 2, 0)))
#
# im2.save('asd.png')

# bit.html you took the wrong curve

for j in range(100)[::-1][::2]: # y
    row = im.crop((j*100, 0, j*100+100, 1))
    row2 = im.crop(((j-1) * 100, 0, (j-1) * 100 + 100, 1))
    row3 = im.crop(((j-1) * 100, 0, (j-1) * 100 + 100, 1))
    print(row.size)
    im2.paste(row, (0,j))
    im2.paste(row2, (0, j+1))
    im2.paste(row2, (0, j+2))
    im2.paste(row3, (0, j+3))


im2.save('asd.png')