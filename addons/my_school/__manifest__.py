# -*- coding: utf-8 -*-
{
    'name': "my_school",
    'name_vi_VN': "",

    'summary': """
Short (1 phrase/line) summary of the module's purpose, used as
subtitle on modules listing or apps.openerp.com""",

    'summary_vi_VN': """
Mô tả ngắn gọn bằng tiếng Việt (1 câu, 1 dòng) về mục đích của module
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
    'depends': ['base','mail'],

    # always loaded
     'data': [
        'security/school_group.xml',
        'security/school_rule.xml',
        'views/views.xml',
        'views/view_hoc_sinh.xml',
        'views/view_base.xml',
        'views/view_giao_vien.xml',
        'views/view_mon_hoc.xml',
        'views/view_models_test.xml',
        'views/templates.xml',
        'views/school_menus.xml',
        'datas/data_lop_hoc.xml',
        'datas/data_hoc_sinh_test.xml',
        'datas/data_mon_hoc.xml',
        'datas/data_cron.xml',
        'security/ir.model.access.csv',
        'views/reports.xml',
        'datas/school.giaovien.csv',
        'datas/data_person_test.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'qweb': [
        'static/src/xml/add_button_tree_view.xml'
    ],
    'images' : [
    	# 'static/description/main_screenshot.png'
    	],
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': 99.9,
    'currency': 'EUR',
    'license': 'OPL-1',
}