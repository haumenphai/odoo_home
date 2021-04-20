# from posix import PRIO_PGRP
# s = """val city1 = City("An Giang", 10.505692, 105.187835)
    # val city2 = City("Bà Rịa - Vũng Tàu", 10.595672, 107.280819)
    # val city3 = City("Bắc Giang", 21.348277, 106.419683)
    # val city5 = City("Bắc Kạn",22.158279, 105.834988)
    # val city6 = City("Bạc Liêu",9.290564, 105.723258)
    # val city7 = City("Bắc Ninh",21.176431, 106.066296)
    # val city8 = City("Bến Tre",10.242779, 106.375542)
    # val city9 = City("Bình Định",14.234785, 109.060661)
    # val city10 = City("Quy Nhơn", 13.782983, 109.219595)
    # val city11 = City("Bình Dương",11.231885, 106.651751)
    # val city12 = City("Bình Phước",11.737477, 106.886652)
    # val city13 = City("Bình Thuận",11.146585, 108.140489)
    # val city14 = City("Bình Thuận",11.146585, 108.140489)
    # val city15 = City("Phan Thiết",10.976763, 108.264234)
    # val city16 = City("Cà Mau",9.152193, 105.195944)
    # val city17 = City("Cao Bằng",22.666056, 106.261639)
    # val city18 = City("Đắk Lắk",12.904440, 108.194657)
    # val city19 = City("Buôn Ma Thuột",12.665681, 108.037672)
    # val city20 = City("Đắk Nông",12.163664, 107.697490)
    # val city21 = City("Điện Biên",21.405930, 103.031860)
    # val city22 = City("Đồng Nai",11.005057, 107.194666)
    # val city23 = City("Đồng Tháp",10.620775, 105.649945)
    # val city24 = City("Gia Lai",13.866409, 108.238006)
    # val city25 = City("Hà Giang",22.801670, 104.978710)
    # val city26 = City("Hà Nam",20.533542, 105.990965)
    # val city27 = City("Hà Tĩnh",18.345682, 105.892674)
    # val city28 = City("Hải Dương",20.936427, 106.320123)
    # val city29 = City("Hậu Giang",9.796628, 105.616896)
    # val city30 = City("Hòa Bình",20.823456, 105.340450)
    # val city31 = City("Hưng Yên",20.813912, 106.053285)
    # val city32 = City("Khánh Hòa",12.281003, 109.001859)
    # val city33 = City("Nha Trang",12.238856, 109.196738)
    # val city34 = City("Cam Ranh", 11.961326, 109.183134)
    # val city35 = City("Kiên Giang",9.977782, 105.177661)
    # val city36 = City("Phú Quốc", 10.270375, 103.978402)
    # val city37 = City("Kon Tum",14.343897, 108.013156)
    # val city38 = City("Lai Châu",22.377852, 103.472007)
    # val city39 = City("Lâm Đồng",11.802784, 108.186967)
    # val city40 = City("Lạng Sơn",21.850850, 106.766057)
    # val city41 = City("Lào Cai",22.480529, 103.975550)
    # val city42 = City("Long An",10.754750, 106.258419)
    # val city43 = City("Nam Định",20.429578, 106.168227)
    # val city44 = City("Nghệ An",19.054224, 105.443204)
    # val city45 = City("Ninh Bình",20.246968, 105.970130)
    # val city46 = City("Ninh Thuận",11.653204, 108.945638)
    # val city47 = City("Phú Thọ",21.307744, 105.142054)
    # val city48 = City("Quảng Bình",17.519365, 106.403920)
    # val city49 = City("Đồng Hới", 17.465428, 106.597157)
    # val city50 = City("Quảng Nam",15.568581, 108.053969)
    # val city51 = City("Quảng Ngãi",15.138031, 108.839256)
    # val city52 = City("Quảng Ninh",21.151432, 107.361547)
    # val city53 = City("Quảng Trị",16.754080, 106.948277)
    # val city54 = City("Sóc Trăng",9.604323, 105.972606)
    # val city55 = City("Sơn La",21.224137, 104.080017)
    # val city56 = City("Tây Ninh",11.369395, 106.130511)
    # val city57 = City("Thái Bình",20.444413, 106.344995)
    # val city58 = City("Thái Nguyên",21.667392, 105.814665)
    # val city59 = City("Thanh Hóa",19.806599, 105.781912)
    # val city60 = City("Thừa Thiên Huế",16.326467, 107.511859)
    # val city61 = City("Tiền Giang",10.424552, 106.342102)
    # val city62 = City("Trà Vinh",9.940881, 106.338847)
    # val city63 = City("Tuyên Quang",21.775941, 105.230417)
    # val city64 = City("Vĩnh Long",10.244117, 105.953169)
    # val city65 = City("Vĩnh Phúc",21.373817, 105.561682)
    # val city66 = City("Yên Bái",21.779274, 104.576700)
    # val city67 = City("Phú Yên",13.203781, 109.114554)
    # val city68 = City("Cần Thơ",10.038749, 105.756540)
    # val city69 = City("Đà Nẵng",16.046341, 108.203873)
    # val city70 = City("Hải Phòng",20.855917, 106.694626)
    # val city71 = City("Hà Nội",21.020496, 105.833263)
    # val city4 = City("TP HCM",10.817871, 106.630455)
# """
#
# line = s.split("\n")
# i = 0
# for o in line:
    # if o == '': continue
    # i +=1
    # # print('item:', o)
    # k = o.find('"')
    # # print(o[k:999999])
    #
    # z = o[k:9999999999].replace('"', "").replace(')','')
    #
    # m = z.split(',')
    #
    #
    # city_name = m[0]
    # lat = m[1]
    # lon = m[2]
    #
    #
    # result = f"""
    # <record id="city{i}" model="weather.forecast">
        # <field name="name">{city_name}</field>
        # <field name="lat">{lat}</field>
        # <field name="lon">{lon}</field>
    # </record>
    # """
    #
    # print(result)
    #
    #

i = 1
while True:
    i += 1
    
    s = f"""
    <field name="daily_ids" eval="[(6, 0, [
               ref('weather.city{i}_1_d'), ref('weather.city{i}_2_d'),
               ref('weather.city{i}_3_d'), ref('weather.city{i}_4_d'),
               ref('weather.city{i}_5_d'), ref('weather.city{i}_6_d')
        ])]"/>
"""
    
    print(s)
    
    
    if i == 71: break







