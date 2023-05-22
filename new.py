# session ={'name':'david', 'cart_item':{'value':True}, 'feet':'yes'}
# for key,val in session['cart_item'].items():
#     print(key)



a = {
'all_total_price': 50000.0, 
'all_total_quantity': 4, 
'cart_item': {
    'bottom005': {'code': 'bottom005', 
                  'image': 'Hypergram Techfit Zebra Short leggings.webp', 
                  'name': 'Hypergram Techfit Zebra Short leggings', 
                  'price': 18000, 
                  'quantity': 1, 
                  'total_price': 18000}, 
    'bottom008': {'code': 'bottom008', 
                  'image': 'Nike I.A.I.R Fleece Shorts.webp', 
                  'name': 'Nike I.A.I.R Fleece Shorts', 
                  'price': 18000, 
                  'quantity': 1,
                  'total_price': 18000}, 
    'top001': {'code': 'top001', 
               'image': 'Big Kids Boys Graphic Training Top.webp', 
               'name': 'Big Kids Boys Graphic Training Top', 
               'price': 10000, 
               'quantity': 1, 
               'total_price': 10000}, 
    'und002': {'code': 'und002', 
               'image': 'Defacto Boy REGULAR FIT Underwear Knitted Boxer.jpg', 
               'name': 'Defacto Boy REGULAR FIT Underwear Knitted Boxer', 
               'price': 4000, 
               'quantity': 1, 
               'total_price': 4000}
    }, 
'email': 'daviderivon@gmail.com', 
'loggedin': True, 
'username': 'rivondave'
}
value = a['cart_item']

new_dict = {'one':{'second':'first', 'third':'second', 'fourth':'third'}, 'two':'second', 'three':'third'}
new_dict_list = list(new_dict.keys())
length = len(new_dict_list)-1
count = 0
while count <= length:
    print(new_dict_list[count])
    count=count+1


def encrypt(char):
    length = len(char)
    list = []
    for i in char:
        value = ord(i)
        value = value/length
        list.append(value)
    list = str(list)
    return list

print(encrypt('dave3#'))
# print(ord('i'))