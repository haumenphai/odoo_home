# -*- coding: utf-8 -*-
{
    'name': "weather",
    'name_vi_VN': "",

    'summary': """
Weather Forecast""",

    'summary_vi_VN': """
App dự báo thời tiết
    	""",

    'description': """
What it does
============
Long description of module's purpose

Key Features
============
1. Feature 1

   * Sub-Feature 1
   * Sub-Feature 2
   
     * Sub-sub-feature 1
     * Sub-sub-feature 2

2. Feature 2

   * Sub-Feature 1
   * Sub-Feature 2

Editions Supported
==================
1. Community Edition
2. Enterprise Edition

    """,

    'description_vi_VN': """
Ứng dụng này làm gì
===================
Mô tả chi tiết về module

Tính năng chính
===============
1. Tính năng 1

   * Tính năng Phụ 1
   * Tính năng Phụ 2
   
     * Tính năng Phụ Chi tiết 1
     * Tính năng Phụ Chi tiết 2

2. Tính năng 2

   * Tính năng Phụ 1
   * Tính năng Phụ 2

Ấn bản được Hỗ trợ
==================
1. Ấn bản Community
2. Ấn bản Enterprise

    """,

    'author': "Viindoo",
    'website': "https://viindoo.com",
    'live_test_url': "https://v13demo-int.erponline.vn",
    'support': "apps.support@viindoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/tvtma/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'datas/data_daily.xml',
        'datas/data_hourly.xml',
        'views/templates.xml',
        'datas/data_city_vietnam.xml',
        'datas/cron_update_weather.xml',
        'views/location_view.xml',
        'datas/data_cities.xml'
        # 'views/templates.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'qweb': [
        # 'static/src/xml/btn_test_123.xml',
    ],
    'images': [
        # 'static/description/main_screenshot.png'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': 99.9,
    'currency': 'EUR',
    'license': 'OPL-1',
}
